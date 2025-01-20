import json

class Campaign:
    def __init__(self, name, regionMapIndexes, mapGrid):
        self.name = name
        # 2D array of regions
        self.regionMapIndexes = regionMapIndexes
        # 2D list of dictionaries of map landmarks and conditions
        self.mapGrid = mapGrid

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json_data):
        return Campaign(**json_data)

    def __str__(self):
        return f"{self.name}"