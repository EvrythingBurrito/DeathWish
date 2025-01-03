from MapObject import MapObject

class NPC(MapObject):
    def __init__(self, name, health, weight, mapIconImgFile):
        super().__init__(name, health, weight, mapIconImgFile)