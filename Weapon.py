from Equipment import Equipment

# Players and Characters will query their equipment to determine available actions

class Weapon(Equipment):
    def __init__(self, name, weight, description, slot, staminaMultiplier, damageMultiplier, speedMultiplier):
        super().__init__(name, weight, description, slot)
        self.staminaMultiplier = staminaMultiplier
        self.damageMultiplier = damageMultiplier
        self.speedMultiplier = speedMultiplier
        