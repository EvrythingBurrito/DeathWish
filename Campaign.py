import json

# every init field must be an input to init (serialization)

class Campaign:

    def __init__(self, name, regionMapIndexes, mapGridJSON, availableEncounterIndexes):
        self.name = name
        # 2D array of regions - in object format
        self.regionMapIndexes = regionMapIndexes
        # 2D list of dictionaries of map landmark string ids - in json format
        self.mapGridJSON = mapGridJSON
        # list of encounter indexes currently available
        self.availableEncounterIndexes = availableEncounterIndexes

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json_data):
        return Campaign(**json_data)

    def __str__(self):
        return f"{self.name}"
    
    # utility
    def update_party_landmark(self, landmarkList, regionList):
        ycoord = 0
        for row in json.loads(self.mapGridJSON):
            xcoord = 0
            for cellDict in row:
                for cellObject in cellDict['objects']:
                    if "landmark" in cellObject:
                        mapObjectID = cellObject.split("-")
                        # Fixme - only one party is allowed for now, just stops when it finds the first landmark that is a party
                        if landmarkList[int(mapObjectID[1])].isParty:
                            partyLocation = [xcoord, ycoord]
                            partyLandmarkIndex = int(mapObjectID[1])
                            self.update_available_encounters(partyLocation, partyLandmarkIndex, landmarkList, regionList)
                            return 1
                xcoord = xcoord + 1
            ycoord = ycoord + 1
        return 0
    
    def update_available_encounters(self, partyLocation, partyLandmarkIndex, landmarkList, regionList):
        # first, add party encounters
        self.availableEncounterIndexes = landmarkList[partyLandmarkIndex].encounterListIndexes
        # second, add encounters from current party region
        # third, add encounters from current party landmark
        cellDict = json.loads(self.mapGridJSON)[partyLocation[1]][partyLocation[0]]
        for object in cellDict['objects']:
            mapObjectID = object.split("-")
            print(mapObjectID)
            # if another non party landmark is at location of party, add its encounters to list
            if not landmarkList[int(mapObjectID[1])].isParty:
                self.availableEncounterIndexes = self.availableEncounterIndexes + landmarkList[mapObjectID[1]].encounterListIndexes

        # from regions
        # self.availableEncounterIndexes = self.availableEncounterIndexes + regionList[self.regionMapIndexes[self.partyLocation[0]][self.partyLocation[1]]].encounterListIndexes