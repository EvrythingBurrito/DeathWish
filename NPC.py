from MapObject import MapObject

class NPC(MapObject):
    def __init__(self, name, health, stamina, mana, actionCount, weight, mapIconImgFile, type, actionListNames):
        super().__init__(name, health, weight, mapIconImgFile, [])
        self.stamina = stamina
        self.mana = mana
        self.actionCount = actionCount
        self.type = "npc"
        self.actionListNames = actionListNames

    def __init__(self, name, health, stamina, mana, actionCount, weight, mapIconImgFile, type, actionListNames, currentEffectJSONList):
        super().__init__(name, health, weight, mapIconImgFile, currentEffectJSONList)
        self.health = health
        self.stamina = stamina
        self.mana = mana
        self.actionCount = actionCount
        self.type = "npc"
        self.actionListNames = actionListNames