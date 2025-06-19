import json
import os

# children classes MUST include a "type" field for javascript to create appropriate map tokens
class MapObject:
    def __init__(self, name, weight, mapIconImgFile):
        self.name = name
        self.weight = weight
        self.mapIconImgFile = mapIconImgFile

    def to_json(self):
        return self.__dict__

    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)