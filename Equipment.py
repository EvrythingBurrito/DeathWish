from Tangible import Tangible

class Equipment(Tangible):
    def __init__(self, name, health, weight, description, slot):
        super().__init__(name, health, weight, description)
        self.slot = slot