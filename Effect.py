import json
### Effect types:
    # think like minecraft enchantments: "rupture I", "elusiveness II", etc.
    # damage type options: each ones quantity is damage amount
        # none
        # slashing (swords, axes, knives, etc.)
        # bludgeoning (hammers, explosions, or arcane force)
        # piercing (arrows, swords, spears)
        # fire (can stack for more and more burning damage, hard to burn armored targets)
        # rupture (bleeding from particularly powerful attacks, such as broken bones, deep gauges, etc.)
        # acid (can permanently destroy most armor)
        # cold (slows all movements)
        # lightning (easier to hit when metal is present)
        # poison (melee attacks deal less damage, needs to draw blood to work)
    # buff options:
        # none
        # alertness (+% chance to dodge at all times) - use sparingly
        # elusiveness (+% chance to dodge only reactions) - example: granted for 1 turn with "step"
        # defensiveness (+multiplier negation amount for all actions) - example: granted with "guard"

### basic notes
# multiple turn effects reactivate at the start of the turn
# turn durations decrement when the turn ends (duration 1 means during the players turn only, 2 means throughout the next full round and again during their turn, etc.)
# all effects do their full Effect Quantity/buff unless modified by other factors

class Effect:
    def __init__(self, name, effectQuantity, effectType, durationTurns):
        self.name = name
        self.effectQuantity = effectQuantity
        self.effectType = effectType
        self.durationTurns = durationTurns

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json_data):
        return Effect(**json_data)

    def __str__(self):
        return f"{self.name}"