import json

class Region:
    def __init__(self, name, worldMapIconFile, encounterListNames):
        ### required
        self.name = name
        self.worldMapIconFile = worldMapIconFile
        # # list of encounters that this region could support (should be large and spread out)
        # # perhaps allow DM to choose an encounter when an encounter is started, perhaps randomize
        self.encounterListNames = encounterListNames
        # ### optional
        # # flavor text
        # self.description = ""
        # # passives that effect players and NPCs constantly in this region
        # self.effectsList = []

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json_data):
        return Region(**json_data)

    def __str__(self):
        return f"{self.name}"