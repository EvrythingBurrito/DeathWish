import json
import random
from NPC import NPC

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

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json_data):
        return Encounter(**json_data)

    def __str__(self):
        return f"{self.name}"

    # FIXME initiative should be random, right now it goes from left to right, top to bottom
    # [
    #     [entityid, NPC object, mapObjectid]
    #     [entityid, NPC object, mapObjectid]
    # ]
    def create_map_object_list(self, NPCList):
        mapObjectList = []
        for row in json.loads(self.mapGridJSON):
            for cellDict in row:
                for cellObject in cellDict['objects']:
                    if cellObject:
                        if cellObject.split("-")[0] == "npc":
                            npcToAdd = NPCList[int(cellObject.split("-")[1])]
                            # make a unique encounter-specific identifier for the NPC (different than the token id, should be easy to remember for players)
                            nextIDNum = 0
                            for item in mapObjectList:
                                if item[0].split("_")[1] == nextIDNum:
                                    nextIDNum += 1
                            entityName = npcToAdd.name + "_" + str(nextIDNum)
                            # index 0 is entity id, index 1 is JSON for NPC object, index 2 is the string that the map list cell contains
                            mapObjectList.append([entityName, npcToAdd.to_json(), cellObject])
        # return the list of lists
        return (mapObjectList)
                            