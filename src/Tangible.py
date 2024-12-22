from MapObject import MapObject

class Tangible(MapObject):
    def __init__(self, name, weight, description, mapIconImgFile):
        super().__init__(name, weight, mapIconImgFile)
        self.description = description