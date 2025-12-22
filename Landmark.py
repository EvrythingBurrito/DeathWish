import json

class Landmark:
    def __init__(self, name, mapIconImgFile, type, encounterListNames):
        ### required
        self.name = name
        self.mapIconImgFile = mapIconImgFile
        self.type = type
        self.encounterListNames = encounterListNames
        # ### optional
        # # flavor text
        # self.description = ""
        # # passives that effect players and Characters constantly in this Landmark
        # self.effectsList = []

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json_data):
        return Landmark(**json_data)

    def __str__(self):
        return f"{self.name}"