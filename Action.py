import json

class Action:
    def __init__(self, name, movementRange, targetSelf, numTargets, targetRange, setupTime, cooldownTime, staminaCost, manaCost, negationAmount, interruptStrength, effectListIndexes):
        ### Order of operations for every action:
        # 1. Allow movement: ask action executer for movement and target allocation
        #   dynamically display choices on their screen as they are being made
        # 2. Update button is pressed by executer, action is locked in
        # 3. Trigger reactions: ask all possible reaction weilders if they want to take it (based on perception stat, setup time (defense) & cooldown time (free shot))
        #   dm can skip this any time
        # 4. Resolve status effects, update gamescreen
        ### basic notes
        # all actions have a base percent chance to hit of 100%, will be modified by other factors
        ### general
        self.name = name
        # max spaces that the action can move for you, without spending another action on movement
        self.movementRange = movementRange
        # target self
        self.targetSelf = targetSelf
        # target to take the effect, or be defended from the effect
        self.numTargets = numTargets
        # max number of spaces any target can be from you to remain a valid target, after any action movement
        self.targetRange = targetRange
        # TODO - make AOE shape object
        # self.isAOE = isAOE
        # self.AOEShape = AOEShape
        ## cost
        # durations, by 100 milliseconds
        self.setupTime = setupTime
        self.cooldownTime = cooldownTime
        self.staminaCost = staminaCost
        self.manaCost = manaCost
        ###### DEFENSE
        # if interrupt strength of attack is less than defending actions negation amount, negate the entirety of the effect
        # max is 100: blocks everything (like a master level shield spell)
        # effect quantity is halved in the event of a tie
        self.negationAmount = negationAmount
        # TODO - add damage types for negation amounts. For now, blocking equally adds negation to all possible effects
        # prevent the parent action from completing
        # if interrupt strength of the defensive action is greater than that of the offensive action, the action is halted
        # max is 100: cannot be interrupted (like movement, or a prep action like guard)
        self.interruptStrength = interruptStrength
        ###### OFFENSE
        # if the action is successful, apply these effects to all targets
        self.effectListIndexes = effectListIndexes

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json_data):
        return Action(**json_data)

    def __str__(self):
        return f"{self.name}"