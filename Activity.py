import json
import os

# describes the shape and substate of an action
#   during an action:
#       a certain number of each are given
#       user can select which to apply to a square, and the corresponding shape will highlight around the selected encounter cells

# (examples: self, single_adj_I/II/III, single_diag_I/II/III, multi_adj_I/II/III, multi_diag_I/II/III, swath_I/II/III, sphere_I/II/III)
#       note : multi_adj_I is the same as sphere_I
# user can rotate an activity around their current position always (only 90 degrees)
#       doesn't affect most of these examples, affects the single ones

# ACTIVITY TYPES
#   rush - shape represents where to rush to on foot 
#   jump - shape represents where to jump/fly to
#   singleTarget - shape represents available range for single-target attack
#   AOE - shape represents entire area to receive effect

class Activity:
    def __init__(self, name, shape, type, effectListIndexes):
        self.name = name
        # 2D grid describing shape: each value is a number describing multiplier for base effects it deals
        # this allows you to weight certain areas' damage (irrelevant for movement)
        self.shape = shape
        # activity type
        self.type = type
        # apply these effects to targets if activity is successful
        self.effectListIndexes = effectListIndexes

    def to_json(self):
        return self.__dict__

    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)
    
    # TODO method which takes in a shape multiplier integer and modifies the shape field with it