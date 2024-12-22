from Equipment import Equipment

class Weapon(Equipment):
    def __init__(self, name, weight, description, slot, damage):
        super().__init__(name, weight, description, slot)
        self.damage = damage