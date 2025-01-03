from Equipment import Equipment

class Weapon(Equipment):
    def __init__(self, name, health, weight, description, slot, damage):
        super().__init__(name, health, weight, description, slot)
        self.damage = damage