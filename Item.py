from Tangible import Tangible

class Item(Tangible):
    def __init__(self, name, health, weight, description):
        super().__init__(name, health, weight, description)