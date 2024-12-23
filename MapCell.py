import json

class MapCell:

    def __init__(self, mapObjectList):
        self.mapObjectList = mapObjectList
    
    def delete_mapObject(self, index):
        del self.mapObjectList[index]

    # check that everything can be in this cell
    # FIXME - make it so that certain things can take a fraction of the cell
    def is_legal(self):
        for obj in self.mapObjectList:
            if (obj.needsFullCell == True):
                return False
        return True

    def add_mapObject(self, mapobject):
        self.mapObjectList.append(mapobject)
        newIndex = len(self.mapObjectList)
        if (self.is_legal() == False):
            self.delete_mapObject(newIndex)
            return 0
        return 1

    def to_json(self):
        return {
            "name": self.name,
            "mapGrid": self.mapGrid
        }

    @staticmethod
    def from_json(json_data):
        return MapCell(**json_data)

    def __str__(self):
        return f"{self.name}"