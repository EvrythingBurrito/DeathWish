import json

class Landmark:
    def __init__(self, name, mapIconImgFile, type, encounterListIndexes):
        ### required
        self.name = name
        self.mapIconImgFile = mapIconImgFile
        self.type = type
        self.encounterListIndexes = encounterListIndexes
        # ### optional
        # # flavor text
        # self.description = ""
        # # passives that effect players and NPCs constantly in this Landmark
        # self.effectsList = []

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json_data):
        return Landmark(**json_data)

    def __str__(self):
        return f"{self.name}"