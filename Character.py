from MapObject import MapObject

class Character(MapObject):
    def __init__(self, name, health, maxHealth, stamina, maxStamina, mana, maxMana,
                 actionCount, maxActionCount, weight, mapIconImgFile, type, actionListNames,
                 currentEffectJSONList):
        super().__init__(name, health, maxHealth, weight, mapIconImgFile, currentEffectJSONList)
        self.stamina = stamina
        self.maxStamina = maxStamina
        self.mana = mana
        self.maxMana = maxMana
        self.actionCount = actionCount
        self.maxActionCount = maxActionCount
        self.type = "character"
        self.actionListNames = actionListNames