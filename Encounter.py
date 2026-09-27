import json
import random
from MapObject import MapObject
from Character import Character
from PlayerCharacter import PlayerCharacter
from Tangible import Tangible
from Effect import Effect
import Game
import string
from collections import deque

class Encounter:

    def __init__(self, name, footingMap, mapGridJSON, description):
        ### required
        self.name = name
        # 2D array of footings - in object format
        self.footingMap = footingMap
        # 2D array of lists of mapObjects, the rules of which should be enforced in the browser side
        self.mapGridJSON = mapGridJSON
        ### optional
        self.description = description
        ### current encounter only
        # list of map objects whose states will change throughout the encounter
        # stays unserialized
        self.mapObjectList = None
        self.activityChain = deque([])
        self.currentSetupToBeat = 0
        self.currentTotalToBeat = 0
        self.reactionDict = {}

    def to_json(self):
        # Exclude things from serialization
        data = self.__dict__.copy()
        data.pop('mapObjectList', None)
        data.pop('activityChain', deque([]))
        data.pop('currentSetupToBeat', 0)
        data.pop('currentTotalToBeat', 0)
        data.pop('reactionDict', {})
        return data

    @staticmethod
    def from_json(json_data):
        return Encounter(**json_data)

    def __str__(self):
        return f"{self.name}"

    # [
    #     [entityName, mapObject JSON, mapObjectid]
    #     [entityName, mapObject JSON, mapObjectid]
    # ]
    # entityName = charName (A)
    # mapObject JSON = {name: charName, ...}
    # mapObjectid = type-charName-#
    def create_map_object_list(self):

        def get_letter_code(num):
            char = string.ascii_uppercase[num % 26]
            count = (num // 26) + 1
            return char * count

        self.mapObjectList = []
        i = 0
        for row in json.loads(self.mapGridJSON):
            for cellDict in row:
                for mapObjectid in cellDict['objects']:
                    objectName = mapObjectid.split("-")[1]
                    if objectName in Game.assets.allMapObjectsDict:
                        mapObjectToAdd = Game.assets.allMapObjectsDict[objectName]
                        entityName = objectName + " (" + get_letter_code(i) + ")"
                        i += 1
                        # index 0 is entityName, index 1 is JSON for mapObject, index 2 is the string that the map list cell contains
                        self.mapObjectList.append([entityName, mapObjectToAdd.to_json(), mapObjectid])
        self.set_starting_turn_order()
        return self.mapObjectList

    def advance_turn_order(self):
        # rotate list by 1
        self.mapObjectList = self.mapObjectList[1:] + self.mapObjectList[:1]
        self.skip_non_action_entities()

    def end_character_action(self, mapObjectID):
        character = self.get_object_from_object_id(mapObjectID)
        character.actionCount = max(0, int(character.actionCount) - 1)
        if character.actionCount == 0:
            # reset action count to default action count for character
            character.actionCount = Game.assets.CharacterDict[mapObjectID.split("-")[1]].actionCount
            self.advance_turn_order()
        self.update_mapObject_from_id(mapObjectID, character)

    def resolve_action_costs(self, mapObjectID, action):
        character = self.get_object_from_object_id(mapObjectID)
        character.apply_action_costs(action)
        self.update_mapObject_from_id(mapObjectID, character)

    def add_to_activity_chain(self, activity, mapObjectID, activityDataJSON):
        if activity.setupTime < self.currentSetupToBeat:
            self.activityChain.appendleft([activity, mapObjectID, activityDataJSON])
            self.currentSetupToBeat = activity.setupTime
            return
        if activity.setupTime < self.currentTotalToBeat:
            self.activityChain.append([activity, mapObjectID, activityDataJSON])
            self.currentTotalToBeat = activity.setupTime + activity.cooldownTime
            return

    def is_mapObject_in_activityChain(self, mapObjectID):
        for entry in self.activityChain:
            if entry[1] == mapObjectID:
                return True
        return False

    def populate_reaction_dict(self):
        self.reactionDict = {}
        for mapObject in self.mapObjectList:
            if mapObject[2].split("-")[0] == "tangible":
                continue
            character = self.get_object_from_object_id(mapObject[2])
            available_reactions = self.get_character_reactions(character)
            self.reactionDict[mapObject[2]] = available_reactions

    def get_character_reactions(self, character):
        reactionList = []
        for actionName in character.actionListNames:
            baseAction = Game.assets.actionDict[actionName]
            turnAction = baseAction.modify_from_character(character)
            # check if the character can afford the action
            # FIXME increase cost for being a reaction
            if not turnAction.meets_cost_requirements(character):
                continue
            # check if the first activity is quick enough to be considered
            activities = turnAction.activityListNames
            print(f"character: {character.name} action: {actionName} activities: {activities}")
            baseActivity = Game.assets.activityDict[turnAction.activityListNames[0]]
            turnActivity = baseActivity.modify_from_character(character)
            if turnActivity.setupTime < self.currentTotalToBeat:
                reactionList.append(turnAction)

    def resolve_activity_effects(self, activity, mapObjectID, activityDataJSON):
        activityData = json.loads(activityDataJSON)
        mapGrid = json.loads(self.mapGridJSON)
        effectJSONsToApply = []
        for effectName in activity.effectNameList:
                effectJSONsToApply.append(Effect.to_json(Game.assets.effectDict[effectName]))
        # FIXME add activity negation in the chain here
        if activity.type == 'singleTarget':
            for object in activityData['selectedObjects']:
                mapObject = self.get_object_from_object_id(object['id'])
                # add serialized effects
                # FIXME modify effects based on executor stats
                # apply effects immediately
                mapObject.apply_effects(effectJSONsToApply)
                # remove object if health reached zero. otherwise, save changes to object
                if int(mapObject.health) <= 0:
                    self.remove_mapObject_by_id(object['id'])
                else:
                    self.update_mapObject_from_id(object['id'], mapObject)
        elif activity.type == "move":
            newRow = int(activityData['row'])
            newCol = int(activityData['col'])
            # remove object at old location
            for row in mapGrid:
                for cellDict in row:
                    for objectID in cellDict['objects']:
                        if objectID == mapObjectID:
                            cellDict['objects'].remove(objectID)
            # add object to new location
            mapGrid[newRow][newCol]['objects'].append(mapObjectID)
            # reserialize & update mapGrid
            self.mapGridJSON = json.dumps(mapGrid)
        elif activity.type == "AOE":
            for loc in activityData['locations']:
                for objectID in mapGrid[int(loc['row'])][int(loc['col'])]['objects']:
                    print(f"AOE applying effects to {objectID}")
                    mapObject = self.get_object_from_object_id(objectID)
                    # apply effects immediately
                    mapObject.apply_effects(effectJSONsToApply)
                    # remove object if health reached zero. otherwise, save changes to object
                    if int(mapObject.health) <= 0:
                        self.remove_mapObject_by_id(objectID)
                    else:
                        self.update_mapObject_from_id(objectID, mapObject)

    def get_current_character(self):
        return self.get_object_from_object_id(self.mapObjectList[0][2])

    def resolve_activity_chain(self):
        for entry in self.activityChain:
            self.resolve_activity_effects()

    ############ Helpers
    # deserialize object
    def get_object_from_object_id(self, mapObjectID):
        for encounterObject in self.mapObjectList:
            if mapObjectID == encounterObject[2]:
                return self.get_object_from_object_json(encounterObject[1])

    def get_object_from_object_json(self, objectJSON):
        objectType = objectJSON.get("type", "")
        if objectType == "character":
            return Character.from_json(objectJSON)
        elif objectType == "player_character":
            return PlayerCharacter.from_json(objectJSON)
        elif objectType == "tangible":
            return Tangible.from_json(objectJSON)
        else:
            return MapObject.from_json(objectJSON)

    # reserialize object with updates
    def update_mapObject_from_id(self, mapObjectID, mapObject):
        for encounterObject in self.mapObjectList:
            if mapObjectID in encounterObject:
                encounterObject[1] = mapObject.to_json()
                return

    def remove_mapObject_by_id(self, mapObjectID):
        for encounterObject in self.mapObjectList:
            if mapObjectID in encounterObject:
                self.mapObjectList.remove(encounterObject)
                mapGrid = json.loads(self.mapGridJSON)
                # print(f"removing {mapObjectID} from {json.loads(self.mapGridJSON)}")
                for row in mapGrid:
                    for cellDict in row:
                        for objectID in cellDict['objects']:
                            if objectID == mapObjectID:
                                print(f"removed {mapObjectID} from {cellDict['objects']}")
                                cellDict['objects'].remove(objectID)
                                continue
        # reserialize & update mapGrid
        self.mapGridJSON = json.dumps(mapGrid)

    def set_starting_turn_order(self):
        # find the top instinct out of all the mapobjects
        turnsSorted = False
        while turnsSorted == False:
            turnsSorted = True
            # dont iterate the last index, nothing to compare to!
            for i in range(0, len(self.mapObjectList) - 1):
                # FIXME add condition for if they're equal
                if self.mapObjectList[i][1].get("instinct", 0) < self.mapObjectList[i + 1][1].get("instinct", 0):
                    turnsSorted = False
                    newTop = self.mapObjectList[i + 1]
                    self.mapObjectList[i + 1] = self.mapObjectList[i]
                    self.mapObjectList[i] = newTop

    def skip_non_action_entities(self):
        current_next_up = self.get_object_from_object_json(self.mapObjectList[0][1])
        while current_next_up.actionCount == 0:
            # rotate list by 1
            self.mapObjectList = self.mapObjectList[1:] + self.mapObjectList[:1]