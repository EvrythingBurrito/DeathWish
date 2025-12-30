import json
import random
from MapObject import MapObject
from Character import Character
from PlayerCharacter import PlayerCharacter
from Tangible import Tangible
from Effect import Effect
import Game
import string

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

    def to_json(self):
        # Exclude 'mapObjectList' from serialization
        data = self.__dict__.copy()
        data.pop('mapObjectList', None)
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

    def resolve_activity_effects(self, activity, mapObjectID, activityDataJSON):
        activityData = json.loads(activityDataJSON)
        mapGrid = json.loads(self.mapGridJSON)
        effectJSONsToApply = []
        for effectName in activity.effectNameList:
                effectJSONsToApply.append(Effect.to_json(Game.assets.effectDict[effectName]))
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

    # def get_pre_activity_counters(self, activity, assets):
    #     preActivityCounters = {}
    #     for mapObject in self.mapObjectList:
    #         entityName = mapObject[0]
    #         character = Character.from_json(mapObject[1])
    #         for actionName in character.actionListNames:
    #             action = assets.actionList[actionName]
    #             # check whether the user can afford the action
    #             if (((action.manaCost) * 2) <= character.mana) and ((action.staminaCost * 2) <= character.stamina):
    #                 for reactActivityName in action.activityListNames:
    #                     reactActivity = Game.assets.activityDict[reactActivityName]
    #                     # ENTIRE action can fit within the setup time
    #                     if ((reactActivity.setupTime + reactActivity.cooldownTime) < activity.setupTime):
    #                         preActivityCounters[entityName] = action.to_json()
    #     return preActivityCounters
    # 
    # def get_post_activity_counters(self, activity, assets):
    #     postActivityCounters = []
    #     for mapObject in self.mapObjectList:
    #         for actionIndex in mapObject.actionListNames:
    #             action = assets.actionList[actionIndex]
    #             # check whether the user can afford the action (FIXME costs will have an extra reaction cost)
    #             if ((action.manaCost * 1.0) <= mapObject.mana) and ((action.staminaCost * 1.0) <= mapObject.stamina):
    #                 for reactActivityName in action.activityListNames:
    #                     reactActivity = Game.assets.activityDict[reactActivityName]
    #                     # ENTIRE action can fit within the cooldown time
    #                     if ((reactActivity.setupTime + reactActivity.cooldownTime) < activity.cooldownTime):
    #                         postActivityCounters.append((mapObject, action))
    #     return postActivityCounters