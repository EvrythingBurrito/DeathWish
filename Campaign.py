import json

class Campaign:
    def __init__(self, name, regionMapIndexes):
        self.name = name
        # 2D array of regions
        self.regionMapIndexes = regionMapIndexes
        # key: landmark name, value: coordinates on map where it lies
        # self.landmarkCoordinateDict = {}

    def to_json(self):
        print(self.__dict__)
        return self.__dict__

    @staticmethod
    def from_json(json_data):
        return Campaign(**json_data)

    def __str__(self):
        return f"{self.name}"