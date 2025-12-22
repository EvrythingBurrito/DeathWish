import json

class Action:
    def __init__(self, name, staminaCost, manaCost, activityListNames):
        ### Order of operations for every action:
        # 1. Action is decided and locked in by executer
        # 3. Trigger reactions: 
        #       ask all possible reaction weilders if they want to take it (based on setup time (for interrupt and dodge) & cooldown time (for free shot))
        #       Setup time is before executor does anything, including movement
        #       Amount of setup time within line of sight of ranged attacks is added together as an opportunity window
        #       Movement can be thought of as a lunge or jump as part of the strike, it's not just walking/running (except for step/stride)
        #       dm can skip this any time
        # 4. Resolve status effects, update gamescreen
        ### basic notes
        # all actions have a base percent chance to hit of 100%, will be modified by other factors
        ### general
        self.name = name
        # TODO add movement type: line, flying, any, etc.
        ## cost
        self.staminaCost = staminaCost
        self.manaCost = manaCost
        ###### COMPONENTS
        # activities contain ranges, effects and target information for the action components
        # activities are done in the order of the list (i.e. detonate trap, then dodge. or jump, then sword spin)
        self.activityListNames = activityListNames

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json_data):
        return Action(**json_data)

    def __str__(self):
        return f"{self.name}"
    
    # TODO - add method which takes Character (with equipment) and returns the modified action

    # TODO - add line of sight method