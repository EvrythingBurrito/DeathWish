from NPC import NPC

class Monster(NPC):
    def __init__(self, name, weight, health, mapIconImgFile):
        super().__init__(name, weight, health, mapIconImgFile)