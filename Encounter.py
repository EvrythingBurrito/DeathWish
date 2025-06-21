import json
import random

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
    
    # FIXME should be random, right now it goes from left to right, top to bottom
    def initialize_turn_order(self, NPCList):
        # an ordered list of NPC objects in some starting turn order
        encounterEntities = []
        # an ordered list of those same NPCs but with encounter-specific names which will be displayed
        entityNames = []
        for row in json.loads(self.mapGridJSON):
            for cellDict in row:
                for cellObject in cellDict['objects']:
                    if cellObject:
                        if cellObject.split("-")[0] == "npc":
                            npcToAdd = NPCList[int(cellObject.split("-")[1])]
                            # add the npc type
                            encounterEntities.append(npcToAdd)
                            # make a unique encounter-specific identifier for the NPC (different than the token id, should be easy to remember for players)
                            nextIDNum = 0
                            for name in entityNames:
                                if name.split("_")[1] == nextIDNum:
                                    nextIDNum += 1
                            entityName = npcToAdd.name + "_" + str(nextIDNum)
                            entityNames.append(entityName)
        # return a tuple describing the combat order
        return (encounterEntities, entityNames)
                            