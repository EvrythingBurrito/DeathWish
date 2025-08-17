from MapObject import MapObject

class NPC(MapObject):
    def __init__(self, name, health, stamina, mana, actionCount, weight, mapIconImgFile, type, actionListIndexes):
        super().__init__(name, weight, mapIconImgFile)
        self.health = health
        self.stamina = stamina
        self.mana = mana
        self.actionCount = actionCount
        self.type = "npc"
        self.actionListIndexes = actionListIndexes