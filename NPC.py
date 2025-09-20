from MapObject import MapObject

class NPC(MapObject):
    def __init__(self, name, health, stamina, mana, actionCount, weight, mapIconImgFile, type, actionListIndexes):
        super().__init__(name, health, weight, mapIconImgFile, [])
        self.stamina = stamina
        self.mana = mana
        self.actionCount = actionCount
        self.type = "npc"
        self.actionListIndexes = actionListIndexes

    def __init__(self, name, health, stamina, mana, actionCount, weight, mapIconImgFile, type, actionListIndexes, currentEffectJSONList):
        super().__init__(name, health, weight, mapIconImgFile, currentEffectJSONList)
        self.health = health
        self.stamina = stamina
        self.mana = mana
        self.actionCount = actionCount
        self.type = "npc"
        self.actionListIndexes = actionListIndexes