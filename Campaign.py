import json

class Campaign:
    def __init__(self, name, regionMapIndexes, mapGrid, partyLandmark, partyLocation, availableEncounterIndexes):
        self.name = name
        # 2D array of regions
        self.regionMapIndexes = regionMapIndexes
        # 2D list of dictionaries of map landmarks and conditions
        self.mapGrid = mapGrid
        # landmark object
        self.partyLandmark = partyLandmark
        # tuple of coordinates
        self.partyLocation = partyLocation
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
        xcoord = 0
        ycoord = 0
        for row in self.mapGrid:
            for cell in row:
                if "landmark" in cell:
                    mapObjectID = cell.split("-")
                    # Fixme - only one party is allowed for now
                    if landmarkList[mapObjectID[1]].isParty:
                        self.partyLocation = [xcoord, ycoord]
                        print(self.partyLocation)
                        self.partyLandmark = landmarkList[mapObjectID[1]]
                        print(self.partyLandmark)
                        self.update_available_encounters(landmarkList, regionList)
                        return 1
                xcoord = xcoord + 1
            ycoord = ycoord + 1
        return 0
    
    def update_available_encounters(self, landmarkList, regionList):
        # from landmarks
        self.availableEncounterIndexes = self.partyLandmark.encounterList
        for object in self.mapGrid[self.partyLocation[0]][self.partyLocation[1]]:
            mapObjectID = object.split("-")
            # if another non party landmark is at location of party, add its encounters to list
            if not landmarkList[mapObjectID[1]].isParty:
                self.availableEncounterIndexes = self.availableEncounterIndexes + landmarkList[mapObjectID[1]].encounterList

        # from regions
        self.availableEncounterIndexes = self.availableEncounterIndexes + regionList[self.regionMapIndexes[self.partyLocation[0]][self.partyLocation[1]]].encounterList