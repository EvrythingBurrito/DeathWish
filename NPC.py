from MapObject import MapObject

class NPC(MapObject):
    def __init__(self, name, weight, health, mapIconImgFile):
        super().__init__(name, weight, mapIconImgFile)
        self.health = health