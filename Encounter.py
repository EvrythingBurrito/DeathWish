import json

class Encounter:

    def __init__(self, name, mapGridJSON, description):
        ### required
        self.name = name
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