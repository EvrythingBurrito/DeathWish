from MapObject import MapObject

class Tangible(MapObject):
    def __init__(self, name, health, weight, description, mapIconImgFile):
        super().__init__(name, health, weight, mapIconImgFile)
        self.description = description