from MapObject import MapObject

class Tangible(MapObject):
    def __init__(self, name, health, maxHealth, weight, description, mapIconImgFile, type, currentEffectJSONList):
        super().__init__(name, health, maxHealth, weight, mapIconImgFile, currentEffectJSONList)
        self.description = description
        self.type = "tangible"