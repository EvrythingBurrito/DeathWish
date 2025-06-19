from MapObject import MapObject

class NPC(MapObject):
    def __init__(self, name, health, weight, mapIconImgFile):
        super().__init__(name, weight, mapIconImgFile)
        self.health = health