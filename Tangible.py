from MapObject import MapObject

class Tangible(MapObject):
    def __init__(self, name, health, weight, description, mapIconImgFile, type, currentEffectJSONList):
        super().__init__(name, health, weight, mapIconImgFile, currentEffectJSONList)
        self.description = description
        self.type = "tangible"