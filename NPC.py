from MapObject import MapObject

class NPC(MapObject):
    def __init__(self, name, health, weight, mapIconImgFile, type):
        super().__init__(name, weight, mapIconImgFile)
        self.health = health
        self.type = "npc"