import json

class Action:
    def __init__(self, name, movementRange, setupTime, cooldownTime, staminaCost, manaCost, negationAmount, interruptStrength, activityListIndexes):
        ### Order of operations for every action:
        # 1. Action is decided and locked in by executer
        # 3. Trigger reactions: 
        #       ask all possible reaction weilders if they want to take it (based on perception stat, setup time (for interrupt) & cooldown time (for free shot))
        #       Setup time is before executor does anything, including movement
        #       Amount of setup time within line of sight of ranged attacks is added together as an opportunity window
        #       Movement can be thought of as a lunge or jump as part of the strike, it's not just walking/running (except for step/stride)
        #       dm can skip this any time
        # 4. Resolve status effects, update gamescreen
        ### basic notes
        # all actions have a base percent chance to hit of 100%, will be modified by other factors
        ### general
        self.name = name
        # max spaces allowed to move during action (only used for step and stride)
        self.movementRange = movementRange
        # TODO add movement type: line, flying, any, etc.
        ## cost
        # durations, by 100 milliseconds
        self.setupTime = setupTime # make sure to factor in ALL activities for these numbers! Give archers time to shoot them if they're in the open
        self.cooldownTime = cooldownTime
        self.staminaCost = staminaCost
        self.manaCost = manaCost
        ###### DEFENDABILITY
        # if interrupt strength of attack is less than defending actions negation amount, negate the entirety of the effect
        # max is 100: blocks everything (like a master level shield spell)
        # effect quantity is halved in the event of a tie
        self.negationAmount = negationAmount
        # TODO - add damage types for negation amounts. For now, blocking equally adds negation to all possible effects
        # prevent the parent action from completing
        # if interrupt strength of the defensive action is greater than that of the offensive action, the action is halted
        # max is 100: cannot be interrupted (like movement, or a prep action like guard)
        self.interruptStrength = interruptStrength
        ###### COMPONENTS
        # activities contain ranges, effects and target information for the action components
        # activities are done in the order of the list (i.e. detonate trap, then dodge. or jump, then sword spin)
        self.activityListIndexes = activityListIndexes
        

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json_data):
        return Action(**json_data)

    def __str__(self):
        return f"{self.name}"
    
    # TODO - add method which takes NPC (with equipment) and returns the modified action

    # TODO - add line of sight method