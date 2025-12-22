from Character import Character

class PlayerCharacter(Character):
    def __init__(self, name, health, stamina, mana, actionCount, weight, mapIconImgFile, type, actionListNames):
        super().__init__(name, health, stamina, mana, actionCount, weight, mapIconImgFile, type, actionListNames)
        self.type = "player_character"

    def __init__(self, name, health, stamina, mana, actionCount, weight, mapIconImgFile, type, actionListNames, currentEffectJSONList):
        super().__init__(name, health, stamina, mana, actionCount, weight, mapIconImgFile, type, actionListNames, currentEffectJSONList)
        self.type = "player_character"