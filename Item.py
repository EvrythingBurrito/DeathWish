from Tangible import Tangible

class Item(Tangible):
    def __init__(self, name, weight, description):
        super().__init__(name, weight, description)