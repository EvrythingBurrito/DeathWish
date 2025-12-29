from MapObject import MapObject

class Character(MapObject):
    def __init__(self, name, health, maxHealth, stamina, maxStamina, mana, maxMana,
                 actionCount, maxActionCount, weight, dexterity, strength, instinct, intellect,
                 mapIconImgFile, type, actionListNames,
                 currentEffectJSONList):
        super().__init__(name, health, maxHealth, weight, mapIconImgFile, currentEffectJSONList)
        self.type = "character"
        self.dexterity = dexterity
        self.strength = strength
        self.instinct = instinct
        self.intellect = intellect
        self.stamina = stamina
        self.maxStamina = maxStamina
        self.mana = mana
        self.maxMana = maxMana
        self.actionCount = actionCount
        self.maxActionCount = maxActionCount
        self.actionListNames = actionListNames

    def apply_action_costs(self, action):
        self.stamina -= action.staminaCost
        self.mana -= action.manaCost