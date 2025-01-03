from NPC import NPC

class Sentient(NPC):
    def __init__(self, name, health, weight, mapIconImgFile):
        super().__init__(name, health, weight, mapIconImgFile)