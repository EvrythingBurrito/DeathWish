import json
import os
from Region import Region
from Footing import Footing
from Landmark import Landmark
from Encounter import Encounter
from Campaign import Campaign
from NPC import NPC
from Action import Action
from Activity import Activity
from Tangible import Tangible
from Effect import Effect
import glob

class Assets:
    def __init__(self):
        self.campaignDir = "./Assets/Campaigns"
        self.regionDir = "./Assets/Regions"
        self.footingDir = "./Assets/Footings"
        self.landmarkDir = "./Assets/Landmarks"
        self.encounterDir = "./Assets/Encounters"
        self.NPCDir = "./Assets/NPCs"
        self.actionDir = "./Assets/Actions"
        self.activityDir = "./Assets/Activities"
        self.tangibleDir = "./Assets/Tangibles"
        self.effectDir = "./Assets/Effects"
        ### initialize lists
        self.campaignDict = {}
        self.update_campaign_dict()
        self.regionDict = {}
        self.update_region_dict()
        self.footingDict = {}
        self.update_footing_dict()
        self.landmarkDict = {}
        self.update_landmark_dict()
        self.tangibleDict = {}
        self.update_tangible_dict()
        self.encounterDict = {}
        self.update_encounter_dict()
        # create a blank "current" encounter
        curEncounter = Encounter("Current", None, None, None)
        # create a blank "current" campaign
        curCampaign = Campaign("Current", None, None, None)
        self.NPCDict = {}
        self.update_NPC_dict()
        self.actionDict = {}
        self.update_action_dict()
        self.activityDict = {}
        self.update_activity_dict()
        self.effectDict = {}
        self.update_effect_dict()

        self.allMapObjectsDict = self.NPCDict | self.tangibleDict

### operate specific elements
    def add_campaign(self, campaign):
        self.campaignDict[campaign.name] = campaign
        self.update_campaign_save(campaign)
    def delete_campaign(self, campaignName):
        self.delete_campaign_save(self.campaignDict[campaignName])
        del self.campaignDict[campaignName]

    def add_region(self, region):
        self.regionDict[region.name] = region
        self.update_region_save(region)
    def delete_region(self, regionName):
        self.delete_region_save(self.regionDict[regionName])
        del self.regionDict[regionName]

    def add_footing(self, footing):
        self.footingDict[footing.name] = footing
        self.update_footing_save(footing)
    def delete_footing(self, footingName):
        self.delete_footing_save(self.footingDict[footingName])
        del self.footingDict[footingName]

    def add_landmark(self, landmark):
        self.landmarkDict[landmark.name] = landmark
        self.update_landmark_save(landmark)
    def delete_landmark(self, landmarkName):
        self.delete_landmark_save(self.landmarkDict[landmarkName])
        del self.landmarkDict[landmarkName]

    def add_encounter(self, encounter):
        self.encounterDict[encounter.name] = encounter
        self.update_encounter_save(encounter)
    def delete_encounter(self, encounterName):
        self.delete_encounter_save(self.encounterDict[encounterName])
        del self.encounterDict[encounterName]

    def add_NPC(self, NPC):
        self.NPCDict[NPC.name] = NPC
        self.update_NPC_save(NPC)
    def delete_NPC(self, NPCName):
        self.delete_NPC_save(self.NPCDict[NPCName])
        del self.NPCDict[NPCName]

    def add_action(self, action):
        self.actionDict[action.name] = action
        self.update_action_save(action)
    def delete_action(self, actionName):
        self.delete_action_save(self.actionDict[actionName])
        del self.actionDict[actionName]

    def add_activity(self, activity):
        self.activityDict[activity.name] = activity
        self.update_activity_save(activity)
    def delete_activity(self, activityName):
        self.delete_activity_save(self.activityDict[activityName])
        del self.activityDict[activityName]

    def add_effect(self, effect):
        self.effectDict[effect.name] = effect
        self.update_effect_save(effect)
    def delete_effect(self, effectName):
        self.delete_effect_save(self.effectDict[effectName])
        del self.effectDict[effectName]

    def add_tangible(self, tangible):
        self.tangibleDict[tangible.name] = tangible
        self.update_tangible_save(tangible)
    def delete_tangible(self, tangibleName):
        self.delete_tangible_save(self.tangibleDict[tangibleName])
        del self.tangibleDict[tangibleName]

###########################################################
#################### SERIALIZATION ########################
###########################################################

########################################################### CAMPAIGNS
    ### create or update save file for desired campaign
    def update_campaign_save(self, campaign):
        filename = self.campaignDir + "/" + campaign.name.replace(" ", "_") + ".json"
        if campaign not in self.campaignDict.items():
            self.campaignDict[campaign.name] = campaign
        if os.path.exists(filename):
            print("overwriting campaign save!")
        with open(filename, 'w') as f:
            json.dump(campaign.to_json(), f)

    def delete_campaign_save(self, campaign):
        filename = self.campaignDir + "/" + campaign.name.replace(" ", "_") + ".json"
        os.remove(filename)

    def update_campaign_dict(self):
        self.campaignDict = {}
        for filename in glob.glob(self.campaignDir + "/*.json"):
            with open(filename, 'r') as f:
                data = json.load(f)
                aCampaign = Campaign.from_json(data)
                self.campaignDict[aCampaign.name] = aCampaign

########################################################### REGIONS

    ### create or update save file for desired region
    def update_region_save(self, region):
        filename = self.regionDir + "/" + region.name.replace(" ", "_") + ".json"
        if region not in self.regionDict.items():
            self.regionDict[region.name] = region
        if os.path.exists(filename):
            print("overwriting region save!")
        with open(filename, 'w') as f:
            json.dump(region.to_json(), f)

    def delete_region_save(self, region):
        filename = self.regionDir + "/" + region.name.replace(" ", "_") + ".json"
        os.remove(filename)

    def update_region_dict(self):
        self.regionDict = {}
        for filename in glob.glob(self.regionDir + "/*.json"):
            with open(filename, 'r') as f:
                data = json.load(f)
                aRegion = Region.from_json(data)
                self.regionDict[aRegion.name] = aRegion

########################################################### FOOTINGS

    ### create or update save file for desired footing
    def update_footing_save(self, footing):
        filename = self.footingDir + "/" + footing.name.replace(" ", "_") + ".json"
        if footing not in self.footingDict.items():
            self.footingDict[footing.name] = footing
        if os.path.exists(filename):
            print("overwriting footing save!")
        with open(filename, 'w') as f:
            json.dump(footing.to_json(), f)

    def delete_footing_save(self, footing):
        filename = self.footingDir + "/" + footing.name.replace(" ", "_") + ".json"
        os.remove(filename)

    def update_footing_dict(self):
        self.footingDict = {}
        for filename in glob.glob(self.footingDir + "/*.json"):
            with open(filename, 'r') as f:
                data = json.load(f)
                aFooting = Footing.from_json(data)
                self.footingDict[aFooting.name] = aFooting


########################################################### LANDMARKS

    ### create or update save file for desired landmark
    def update_landmark_save(self, landmark):
        filename = self.landmarkDir + "/" + landmark.name.replace(" ", "_") + ".json"
        if landmark not in self.landmarkDict.items():
            self.landmarkDict[landmark.name] = landmark
        if os.path.exists(filename):
            print("overwriting landmark save!")
        with open(filename, 'w') as f:
            json.dump(landmark.to_json(), f)

    def delete_landmark_save(self, landmark):
        filename = self.landmarkDir + "/" + landmark.name.replace(" ", "_") + ".json"
        os.remove(filename)

    def update_landmark_dict(self):
        self.landmarkDict = {}
        for filename in glob.glob(self.landmarkDir + "/*.json"):
            with open(filename, 'r') as f:
                data = json.load(f)
                aLandmark = Landmark.from_json(data)
                self.landmarkDict[aLandmark.name] = aLandmark

########################################################### ENCOUNTERS

    ### create or update save file for desired encounter
    def update_encounter_save(self, encounter):
        filename = self.encounterDir + "/" + encounter.name.replace(" ", "_") + ".json"
        if encounter not in self.encounterDict.items():
            self.encounterDict[encounter.name] = encounter
        if os.path.exists(filename):
            print("overwriting encounter save!")
        with open(filename, 'w') as f:
            json.dump(encounter.to_json(), f)

    def delete_encounter_save(self, encounter):
        filename = self.encounterDir + "/" + encounter.name.replace(" ", "_") + ".json"
        os.remove(filename)

    def update_encounter_dict(self):
        self.encounterDict = {}
        for filename in glob.glob(self.encounterDir + "/*.json"):
            with open(filename, 'r') as f:
                data = json.load(f)
                aEncounter = Encounter.from_json(data)
                self.encounterDict[aEncounter.name] = aEncounter

########################################################### NPCS

    ### create or update save file for desired NPC
    def update_NPC_save(self, NPC):
        filename = self.NPCDir + "/" + NPC.name.replace(" ", "_") + ".json"
        if NPC not in self.NPCDict.items():
            self.NPCDict[NPC.name] = NPC
        if os.path.exists(filename):
            print("overwriting NPC save!")
        with open(filename, 'w') as f:
            json.dump(NPC.to_json(), f)

    def delete_NPC_save(self, NPC):
        filename = self.NPCDir + "/" + NPC.name.replace(" ", "_") + ".json"
        os.remove(filename)

    def update_NPC_dict(self):
        self.NPCDict = {}
        for filename in glob.glob(self.NPCDir + "/*.json"):
            with open(filename, 'r') as f:
                data = json.load(f)
                aNPC = NPC.from_json(data)
                self.NPCDict[aNPC.name] = aNPC

########################################################### ACTIONS

    ### create or update save file for desired action
    def update_action_save(self, action):
        filename = self.actionDir + "/" + action.name.replace(" ", "_") + ".json"
        if action not in self.actionDict.items():
            self.actionDict[action.name] = action
        if os.path.exists(filename):
            print("overwriting action save!")
        with open(filename, 'w') as f:
            json.dump(action.to_json(), f)

    def delete_action_save(self, action):
        filename = self.actionDir + "/" + action.name.replace(" ", "_") + ".json"
        os.remove(filename)

    def update_action_dict(self):
        self.actionDict = {}
        for filename in glob.glob(self.actionDir + "/*.json"):
            with open(filename, 'r') as f:
                data = json.load(f)
                aAction = Action.from_json(data)
                self.actionDict[aAction.name] = aAction

########################################################### ACTIVITIES

    ### create or update save file for desired activity
    def update_activity_save(self, activity):
        filename = self.activityDir + "/" + activity.name.replace(" ", "_") + ".json"
        if activity not in self.activityDict.items():
            self.activityDict[activity.name] = activity
        if os.path.exists(filename):
            print("overwriting activity save!")
        with open(filename, 'w') as f:
            json.dump(activity.to_json(), f)

    def delete_activity_save(self, activity):
        filename = self.activityDir + "/" + activity.name.replace(" ", "_") + ".json"
        os.remove(filename)

    def update_activity_dict(self):
        self.activityDict = {}
        for filename in glob.glob(self.activityDir + "/*.json"):
            with open(filename, 'r') as f:
                data = json.load(f)
                aActivity = Activity.from_json(data)
                self.activityDict[aActivity.name] = aActivity

########################################################### EFFECTS

    ### create or update save file for desired effect
    def update_effect_save(self, effect):
        filename = self.effectDir + "/" + effect.name.replace(" ", "_") + ".json"
        if effect not in self.effectDict.items():
            self.effectDict[effect.name] = effect
        if os.path.exists(filename):
            print("overwriting effect save!")
        with open(filename, 'w') as f:
            json.dump(effect.to_json(), f)

    def delete_effect_save(self, effect):
        filename = self.effectDir + "/" + effect.name.replace(" ", "_") + ".json"
        os.remove(filename)

    def update_effect_dict(self):
        self.effectDict = {}
        for filename in glob.glob(self.effectDir + "/*.json"):
            with open(filename, 'r') as f:
                data = json.load(f)
                aEffect = Effect.from_json(data)
                self.effectDict[aEffect.name] = aEffect

########################################################### TANGIBLES

    ### create or update save file for desired tangible
    def update_tangible_save(self, tangible):
        filename = self.tangibleDir + "/" + tangible.name.replace(" ", "_") + ".json"
        if tangible not in self.tangibleDict.items():
            self.tangibleDict[tangible.name] = tangible
        if os.path.exists(filename):
            print("overwriting tangible save!")
        with open(filename, 'w') as f:
            json.dump(tangible.to_json(), f)

    def delete_tangible_save(self, tangible):
        filename = self.tangibleDir + "/" + tangible.name.replace(" ", "_") + ".json"
        os.remove(filename)

    def update_tangible_dict(self):
        self.tangibleDict = {}
        for filename in glob.glob(self.tangibleDir + "/*.json"):
            with open(filename, 'r') as f:
                data = json.load(f)
                aTangible = Tangible.from_json(data)
                self.tangibleDict[aTangible.name] = aTangible