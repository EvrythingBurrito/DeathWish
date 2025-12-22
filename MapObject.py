import json
import os

from Effect import Effect

# children classes MUST include a "type" field for javascript to create appropriate map tokens
class MapObject:
    # reload init
    def __init__(self, name, health, maxHealth, weight, mapIconImgFile, currentEffectJSONList):
        self.name = name
        # loading these from JSON strings
        self.health = health
        self.maxHealth = maxHealth
        self.weight = weight
        self.mapIconImgFile = mapIconImgFile
        self.currentEffectJSONList = currentEffectJSONList

    def to_json(self):
        return self.__dict__

    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)
    
    def apply_effects(self, effectJSONList):
        # add serialized effects to list of effects to resolve
        for effectJSON in effectJSONList:
            self.currentEffectJSONList.append(effectJSON)
            # print(f"adding effect {effectJSON} to")
        # resolve applied effects
        for effectJSON in self.currentEffectJSONList:
            effect = Effect.from_json(effectJSON)
            # print(f'resolving effect {effect.name} to {self.name}')
            # apply effects FIXME - apply resistances here
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
                removedEffect = self.currentEffectJSONList.pop(self.currentEffectJSONList.index(effectJSON))