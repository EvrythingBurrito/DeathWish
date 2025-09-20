import json
import os

from Effect import Effect

# children classes MUST include a "type" field for javascript to create appropriate map tokens
class MapObject:
    def __init__(self, name, health, weight, mapIconImgFile, currentEffectJSONList):
        self.name = name
        self.health = health
        self.weight = weight
        self.mapIconImgFile = mapIconImgFile
        self.currentEffectJSONList = currentEffectJSONList

    def to_json(self):
        return self.__dict__

    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)
    
    def apply_effects(self, effectList):
        jsonIndexesToRemove = []
        for effectJSON in self.currentEffectJSONList:
            effect = Effect.from_json(effectJSON)
            print(f'applying effect {effect.name} to {self.name}')
            # apply effects
            if effect.effectType == 'slashing':
                self.health = max(0, int(self.health) - int(effect.effectQuantity))
            elif effect.effectType == 'bludgeoning':
                self.health = max(0, int(self.health) - int(effect.effectQuantity))
            elif effect.effectType == 'piercing':
                self.health = max(0, int(self.health) - int(effect.effectQuantity))
            elif effect.effectType == 'fire':
                self.health = max(0, int(self.health) - int(effect.effectQuantity))
            elif effect.effectType == 'rupture':
                self.health = max(0, int(self.health) - int(effect.effectQuantity))
            elif effect.effectType == 'acid':
                self.health = max(0, int(self.health) - int(effect.effectQuantity))
            elif effect.effectType == 'cold':
                self.health = max(0, int(self.health) - int(effect.effectQuantity))
            elif effect.effectType == 'lightning':
                self.health = max(0, int(self.health) - int(effect.effectQuantity))
            elif effect.effectType == 'poison':
                self.health = max(0, int(self.health) - int(effect.effectQuantity))
            # decrement duration counter
            effect.durationTurns = max(0, int(effect.durationTurns) - 1)
            if effect.durationTurns == 0:
                jsonIndexesToRemove.append(self.currentEffectJSONList.index(effectJSON))
        # remove effect when duration times out
        for index in jsonIndexesToRemove:
            removedEffect = self.currentEffectJSONList.pop(index)
            print(f'removed {removedEffect} from {self.name}s effectList')