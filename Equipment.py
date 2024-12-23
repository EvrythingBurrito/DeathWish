from Tangible import Tangible

class Equipment(Tangible):
    def __init__(self, name, weight, description, slot):
        super().__init__(name, weight, description)
        self.slot = slot