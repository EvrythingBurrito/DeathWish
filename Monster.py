from NPC import NPC

class Monster(NPC):
    def __init__(self, name, health, weight, mapIconImgFile):
        super().__init__(name, health, weight, mapIconImgFile)