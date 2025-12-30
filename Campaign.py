import json
import Game
from PlayerCharacter import PlayerCharacter
from Character import Character

class Campaign:
    def __init__(self, name, regionMapNames, mapGridJSON, availableEncounterNames, activeCharacterDictJSON):
        self.name = name
        # 2D array of regions - in object format
        self.regionMapNames = regionMapNames
        # 2D list of dictionaries of map landmark string ids - in json format
        self.mapGridJSON = mapGridJSON
        # list of encounters currently available
        self.availableEncounterNames = availableEncounterNames
        self.activeCharacterDictJSON = activeCharacterDictJSON

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json_data):
        return Campaign(**json_data)

    def __str__(self):
        return f"{self.name}"
    
    # utility
    def update_party_landmark(self):
        ycoord = 0
        for row in json.loads(self.mapGridJSON):
            xcoord = 0
            for cellDict in row:
                for cellObject in cellDict['objects']:
                    if cellObject:
                        mapObjectID = cellObject.split("-")
                        # Fixme - only one party is allowed for now, just stops when it finds the first landmark that is a party
                        if Game.assets.landmarkDict[mapObjectID[1]].type == "party":
                            partyLocation = [xcoord, ycoord]
                            self.update_available_encounters(partyLocation, mapObjectID[1])
                            return 1
                xcoord = xcoord + 1
            ycoord = ycoord + 1
        return 0
    
    def update_available_encounters(self, partyLocation, partyLandmarkName):
        # first, add party encounters
        self.availableEncounterNames = Game.assets.landmarkDict[partyLandmarkName].encounterListNames
        # second, add encounters from current party region
        # third, add encounters from current party landmark
        cellDict = json.loads(self.mapGridJSON)[partyLocation[1]][partyLocation[0]]
        for object in cellDict['objects']:
            mapObjectID = object.split("-")
            # if another non party landmark is at location of party, add its encounters to list
            if not Game.assets.landmarkDict[mapObjectID[1]].type == "party":
                self.availableEncounterNames.append(Game.assets.landmarkDict[mapObjectID[1]].encounterListNames)

        # from regions
        # self.availableEncounterNames = self.availableEncounterNames + regionList[self.regionMapNames[self.partyLocation[0]][self.partyLocation[1]]].encounterListNames

    def update_character_dict(self, character):
        self.activeCharacterDictJSON[character.name] = character.to_json()

    def get_character_from_dict(self, characterName, type):
        if self.activeCharacterDictJSON.get(characterName, None):
            if type == "player_character":
                return PlayerCharacter.from_json(self.activeCharacterDictJSON[characterName])
            if type == "character":
                return Character.from_json(self.activeCharacterDictJSON[characterName])
        # FIXME add error condition