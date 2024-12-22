import json

class Encounter:

    def __init__(self, name, mapGrid):
        ### required
        self.name = name
        # 2D array of MapCells
        self.mapGrid = mapGrid
        ### optional
        self.description = ""

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json_data):
        return Encounter(**json_data)

    def __str__(self):
        return f"{self.name}"