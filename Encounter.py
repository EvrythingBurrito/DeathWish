import json
import random
from MapObject import MapObject
from NPC import NPC
from Effect import Effect

class Encounter:

    def __init__(self, name, footingMapIndexes, mapGridJSON, description):
        ### required
        self.name = name
        # 2D array of footings - in object format
        self.footingMapIndexes = footingMapIndexes
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
    def create_map_object_list(self, allMapObjects):
        self.mapObjectList = []
        for row in json.loads(self.mapGridJSON):
            for cellDict in row:
                for cellObject in cellDict['objects']:
                    if cellObject:
                        if cellObject.split("-")[0] == "npc":
                            mapObjectToAdd = allMapObjects[int(cellObject.split("-")[1])]
                            # make a unique encounter-specific identifier for the mapObject (different than the token id, should be easy to remember for players)
                            nextIDNum = 0
                            for item in self.mapObjectList:
                                if item[0].split("_")[1] == nextIDNum:
                                    nextIDNum += 1
                            entityName = mapObjectToAdd.name + "_" + str(nextIDNum)
                            # index 0 is entity id, index 1 is JSON for mapObject, index 2 is the string that the map list cell contains
                            self.mapObjectList.append([entityName, mapObjectToAdd.to_json(), cellObject])
        # return the list of lists
        return (self.mapObjectList)

    def advance_turn_order(self):
        # rotate list by 1
        self.mapObjectList = self.mapObjectList[1:] + self.mapObjectList[:1]
        # keep rotating until next up is a npc
        while self.mapObjectList[0][2].split("-")[0] != "npc":
            self.mapObjectList = self.mapObjectList[1:] + self.mapObjectList[:1]

    def end_NPC_action(self, mapObjectID):
        npc = self.get_object_from_object_id(mapObjectID)
        npc.actionCount = max(0, int(npc.actionCount) - 1)
        self.update_mapObject_from_id(mapObjectID, npc)
        if npc.actionCount == 0:
            self.advance_turn_order()

    def resolve_activity_effects(self, activity, effectList, mapObjectID, activityDataJSON):
        activityData = json.loads(activityDataJSON)
        mapGrid = json.loads(self.mapGridJSON)
        if activity.type == 'singleTarget':
            for object in activityData['selectedObjects']:
                mapObject = self.get_object_from_object_id(object['id'])
                # add serialized effects
                # FIXME modify effects based on executor stats
                for effectIndex in activity.effectListIndexes:
                    mapObject.currentEffectJSONList.append(Effect.to_json(effectList[effectIndex]))
                # apply effects immediately
                mapObject.apply_effects(effectList)
                # save changes to object
                self.update_mapObject_from_id(object['id'], mapObject)
        elif activity.type == "move":
            print("executing move")
            newRow = int(activityData['row'])
            newCol = int(activityData['col'])
            # remove object at old location
            for row in mapGrid:
                for cellDict in row:
                    for cellObject in cellDict['objects']:
                        if cellObject == mapObjectID:
                            cellDict['objects'].remove(cellObject)
            # add object to new location
            mapGrid[newRow][newCol]['objects'].append(mapObjectID)
            # reserialize & update mapGrid
            self.mapGridJSON = json.dumps(mapGrid)
        elif activity.type == "AOE":
            print(activityData)

    # deserialize object
    def get_object_from_object_id(self, mapObjectID):
        for encounterObject in self.mapObjectList:
            if mapObjectID == encounterObject[2]:
                if mapObjectID.split("-")[0] == "npc":
                    return NPC.from_json(encounterObject[1])
                else:
                    return MapObject.from_json(encounterObject[1])
                
    # reserialize object with updates
    def update_mapObject_from_id(self, mapObjectID, mapObject):
        for encounterObject in self.mapObjectList:
            if mapObjectID in encounterObject:
                encounterObject[1] = mapObject.to_json()

    def get_pre_activity_counters(self, activity, assets):
        preActivityCounters = {}
        for mapObject in self.mapObjectList:
            entityName = mapObject[0]
            character = NPC.from_json(mapObject[1])
            charActionsIndexes = character.actionListIndexes
            for actionIndex in charActionsIndexes:
                action = assets.actionList[actionIndex]
                # check whether the user can afford the action
                if (((action.manaCost) * 2) <= character.mana) and ((action.staminaCost * 2) <= character.stamina):
                    for reactActivity in action.activityListIndexes:
                        # ENTIRE action can fit within the setup time
                        if ((reactActivity.setupTime + reactActivity.cooldownTime) < activity.setupTime):
                            preActivityCounters[entityName] = action.to_json()
        return preActivityCounters
    
    def get_post_activity_counters(self, activity, assets):
        postActivityCounters = []
        for mapObject in self.mapObjectList:
            for actionIndex in mapObject.actionListIndexes:
                action = assets.actionList[actionIndex]
                # check whether the user can afford the action (FIXME costs will have an extra reaction cost)
                if ((action.manaCost * 1.0) <= mapObject.mana) and ((action.staminaCost * 1.0) <= mapObject.stamina):
                    for reactActivity in action.activityListIndexes:
                        # ENTIRE action can fit within the cooldown time
                        if ((reactActivity.setupTime + reactActivity.cooldownTime) < activity.cooldownTime):
                            postActivityCounters.append((mapObject, action))
        return postActivityCounters