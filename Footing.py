import json

class Footing:
    def __init__(self, name, mapIconFile, terrainDifficulty, opacity, solidity):
        ### required
        self.name = name
        self.mapIconFile = mapIconFile
        # % of your movement it takes to move through it
        self.terrainDifficulty = terrainDifficulty
        # % chance to hit reduction while target or self is in it
        self.opacity = opacity
        # negationAmount added to an action taking place across it. 100 is a completely solid space, like a meter-diameter tree
        self.solidity = solidity
        # ### later
        # climbability
        # # flavor text
        # self.description = ""
        # # passives that effect players and Characters in this footing at the start of their turn
        # self.effectsList = []

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json_data):
        return Footing(**json_data)

    def __str__(self):
        return f"{self.name}"