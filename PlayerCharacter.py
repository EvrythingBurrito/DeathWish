from Character import Character

class PlayerCharacter(Character):
    def __init__(self, name, health, maxHealth, stamina, maxStamina, mana, maxMana,
                 actionCount, maxActionCount, weight, mapIconImgFile, type, actionListNames,
                 currentEffectJSONList):
        super().__init__(name, health, maxHealth, stamina, maxStamina, mana, maxMana,
                 actionCount, maxActionCount, weight, mapIconImgFile, type, actionListNames,
                 currentEffectJSONList)
        self.type = "player_character"