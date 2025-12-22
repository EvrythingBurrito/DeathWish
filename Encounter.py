import json
import random
from MapObject import MapObject
from Character import Character
from Tangible import Tangible
from Effect import Effect
import Game

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

    # FIXME initiative should be speed-based, right now it goes from left to right, top to bottom
    # [
    #     [entityid, mapObject JSON, mapObjectid]
    #     [entityid, mapObject JSON, mapObjectid]
    # ]
    def create_map_object_list(self):
        self.mapObjectList = []
        for row in json.loads(self.mapGridJSON):
            for cellDict in row:
                for cellObject in cellDict['objects']:
                    if cellObject:
                        if cellObject.split("-")[0] == "character" or cellObject.split("-")[0] == "tangible":
                            mapObjectToAdd = Game.assets.allMapObjectsDict[cellObject.split("-")[1]]
                            # make a unique encounter-specific identifier for the mapObject (different than the token id, should be easy to remember for players)
                            nextIDNum = 0
                            entityName = mapObjectToAdd.name + "_" + str(nextIDNum)
                            for item in self.mapObjectList:
                                if item[0] == entityName:
                                    nextIDNum += 1
                                    entityName = mapObjectToAdd.name + "_" + str(nextIDNum)
                            # index 0 is entity id, index 1 is JSON for mapObject, index 2 is the string that the map list cell contains
                            self.mapObjectList.append([entityName, mapObjectToAdd.to_json(), cellObject])
        # return the list of lists
        if self.mapObjectList[0][2].split("-")[0] != "character":
            self.advance_turn_order()
        return (self.mapObjectList)

    def advance_turn_order(self):
        # rotate list by 1
        self.mapObjectList = self.mapObjectList[1:] + self.mapObjectList[:1]
        # keep rotating until next up is a character
        while self.mapObjectList[0][2].split("-")[0] != "character":
            self.mapObjectList = self.mapObjectList[1:] + self.mapObjectList[:1]

    def end_character_action(self, mapObjectID):
        character = self.get_object_from_object_id(mapObjectID)
        character.actionCount = max(0, int(character.actionCount) - 1)
        if character.actionCount == 0:
            # reset action count to default action count for character
            character.actionCount = Game.assets.CharacterDict[mapObjectID.split("-")[1]].actionCount
            self.advance_turn_order()
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

    # deserialize object
    def get_object_from_object_id(self, mapObjectID):
        for encounterObject in self.mapObjectList:
            if mapObjectID == encounterObject[2]:
                if mapObjectID.split("-")[0] == "character":
                    return Character.from_json(encounterObject[1])
                elif mapObjectID.split("-")[0] == "tangible":
                    return Tangible.from_json(encounterObject[1])
                else:
                    return MapObject.from_json(encounterObject[1])
                
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