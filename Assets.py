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
from Effect import Effect
import glob

class Assets:
    def __init__(self):
        self.campaignDir = "Assets/Campaigns"
        self.regionDir = "Assets/Regions"
        self.footingDir = "Assets/Footings"
        self.landmarkDir = "Assets/Landmarks"
        self.encounterDir = "Assets/Encounters"
        self.NPCDir = "Assets/NPCs"
        self.actionDir = "Assets/Actions"
        self.activityDir = "Assets/Activities"
        self.effectDir = "Assets/Effects"
        ### initialize lists
        self.campaignList = []
        self.update_campaign_list()
        self.regionList = []
        self.update_region_list()
        self.footingList = []
        self.update_footing_list()
        self.landmarkList = []
        self.update_landmark_list()
        self.tangibleList = []
        self.encounterList = []
        self.update_encounter_list()
        # create the "current" encounter
        if len(self.encounterList) > 0:
            curEncounter = self.encounterList[0]
            curEncounter.name = "Current"
        else:
            curEncounter = Encounter("Current", [[0 for _ in range(8)] for _ in range(8)], "blank", None)
        self.add_encounter(curEncounter)
        self.NPCList = []
        self.update_NPC_list()
        self.actionList = []
        self.update_action_list()
        self.activityList = []
        self.update_activity_list()
        self.effectList = []
        self.update_effect_list()

### operate specific elements
    def add_campaign(self, campaign):
        self.campaignList.append(campaign)
        self.update_campaign_save(campaign)
    def delete_campaign(self, index):
        self.delete_campaign_save(self.campaignList[index])
        del self.campaignList[index]

    def add_region(self, region):
        self.regionList.append(region)
        self.update_region_save(region)
    def delete_region(self, index):
        self.delete_region_save(self.regionList[index])
        del self.regionList[index]

    def add_footing(self, footing):
        self.footingList.append(footing)
        self.update_footing_save(footing)
    def delete_footing(self, index):
        self.delete_footing_save(self.footingList[index])
        del self.footingList[index]

    def add_landmark(self, landmark):
        self.landmarkList.append(landmark)
        self.update_landmark_save(landmark)
    def delete_landmark(self, index):
        self.delete_landmark_save(self.landmarkList[index])
        del self.landmarkList[index]

    def add_encounter(self, encounter):
        self.encounterList.append(encounter)
        self.update_encounter_save(encounter)
    def delete_encounter(self, index):
        self.delete_encounter_save(self.encounterList[index])
        del self.encounterList[index]

    def add_NPC(self, NPC):
        self.NPCList.append(NPC)
        self.update_NPC_save(NPC)
    def delete_NPC(self, index):
        self.delete_NPC_save(self.NPCList[index])
        del self.NPCList[index]

    def add_action(self, action):
        self.actionList.append(action)
        self.update_action_save(action)
    def delete_action(self, index):
        self.delete_action_save(self.actionList[index])
        del self.actionList[index]

    def add_activity(self, activity):
        self.activityList.append(activity)
        self.update_activity_save(activity)
    def delete_activity(self, index):
        self.delete_activity_save(self.activityList[index])
        del self.activityList[index]

    def add_effect(self, effect):
        self.effectList.append(effect)
        self.update_effect_save(effect)
    def delete_effect(self, index):
        self.delete_effect_save(self.effectList[index])
        del self.effectList[index]

###########################################################
#################### SERIALIZATION ########################
###########################################################

########################################################### CAMPAIGNS
    ### create or update save file for desired campaign
    def update_campaign_save(self, campaign):
        filename = self.campaignDir + "/" + campaign.name.replace(" ", "_") + ".json"
        if os.path.exists(filename):
            print("overwriting campaign save!")
        with open(filename, 'w') as f:
            json.dump(campaign.to_json(), f)
        self.update_campaign_list()

    def delete_campaign_save(self, campaign):
        filename = self.campaignDir + "/" + campaign.name.replace(" ", "_") + ".json"
        os.remove(filename)

    def update_campaign_list(self):
        self.campaignList = []
        for filename in glob.glob(self.campaignDir + "/*.json"):
            with open(filename, 'r') as f:
                data = json.load(f)
                aCampaign = Campaign.from_json(data)
                self.campaignList.append(aCampaign)

########################################################### REGIONS

    ### create or update save file for desired region
    def update_region_save(self, region):
        filename = self.regionDir + "/" + region.name.replace(" ", "_") + ".json"
        if region not in self.regionList:
            self.add_region(region)
        if os.path.exists(filename):
            print("overwriting region save!")
        with open(filename, 'w') as f:
            json.dump(region.to_json(), f)

    def delete_region_save(self, region):
        filename = self.regionDir + "/" + region.name.replace(" ", "_") + ".json"
        os.remove(filename)

    def update_region_list(self):
        self.regionList = []
        for filename in glob.glob(self.regionDir + "/*.json"):
            with open(filename, 'r') as f:
                data = json.load(f)
                aRegion = Region.from_json(data)
                self.regionList.append(aRegion)

########################################################### FOOTINGS

    ### create or update save file for desired footing
    def update_footing_save(self, footing):
        filename = self.footingDir + "/" + footing.name.replace(" ", "_") + ".json"
        if footing not in self.footingList:
            self.add_footing(footing)
        if os.path.exists(filename):
            print("overwriting footing save!")
        with open(filename, 'w') as f:
            json.dump(footing.to_json(), f)

    def delete_footing_save(self, footing):
        filename = self.footingDir + "/" + footing.name.replace(" ", "_") + ".json"
        os.remove(filename)

    def update_footing_list(self):
        self.footingList = []
        for filename in glob.glob(self.footingDir + "/*.json"):
            with open(filename, 'r') as f:
                data = json.load(f)
                aFooting = Footing.from_json(data)
                self.footingList.append(aFooting)


########################################################### LANDMARKS

    ### create or update save file for desired landmark
    def update_landmark_save(self, landmark):
        filename = self.landmarkDir + "/" + landmark.name.replace(" ", "_") + ".json"
        if landmark not in self.landmarkList:
            self.add_landmark(landmark)
        if os.path.exists(filename):
            print("overwriting landmark save!")
        with open(filename, 'w') as f:
            json.dump(landmark.to_json(), f)

    def delete_landmark_save(self, landmark):
        filename = self.landmarkDir + "/" + landmark.name.replace(" ", "_") + ".json"
        os.remove(filename)

    def update_landmark_list(self):
        self.landmarkList = []
        for filename in glob.glob(self.landmarkDir + "/*.json"):
            with open(filename, 'r') as f:
                data = json.load(f)
                aLandmark = Landmark.from_json(data)
                self.landmarkList.append(aLandmark)

########################################################### ENCOUNTERS

    ### create or update save file for desired encounter
    def update_encounter_save(self, encounter):
        filename = self.encounterDir + "/" + encounter.name.replace(" ", "_") + ".json"
        if encounter not in self.encounterList:
            self.add_encounter(encounter)
        if os.path.exists(filename):
            print("overwriting encounter save!")
        with open(filename, 'w') as f:
            json.dump(encounter.to_json(), f)

    def delete_encounter_save(self, encounter):
        filename = self.encounterDir + "/" + encounter.name.replace(" ", "_") + ".json"
        os.remove(filename)

    def update_encounter_list(self):
        self.encounterList = []
        for filename in glob.glob(self.encounterDir + "/*.json"):
            with open(filename, 'r') as f:
                data = json.load(f)
                aEncounter = Encounter.from_json(data)
                self.encounterList.append(aEncounter)
    
    def get_current_encounter(self):
        for i in range(0, len(self.encounterList) - 1):
            if self.encounterList[i].name == "Current":
                return self.encounterList[i]

    def update_current_encounter(self, encounter):
        for i in range(0, len(self.encounterList) - 1):
            if self.encounterList[i].name == "Current":
                self.encounterList[i] = encounter
                self.encounterList[i].name = "Current"
                self.update_encounter_save(self.encounterList[i])
        print("error! current encounter not found!")

########################################################### NPCS

    ### create or update save file for desired NPC
    def update_NPC_save(self, npc):
        filename = self.NPCDir + "/" + npc.name.replace(" ", "_") + ".json"
        if npc not in self.NPCList:
            self.add_NPC(npc)
        if os.path.exists(filename):
            print("overwriting NPC save!")
        with open(filename, 'w') as f:
            json.dump(npc.to_json(), f)

    def delete_NPC_save(self, npc):
        filename = self.NPCDir + "/" + npc.name.replace(" ", "_") + ".json"
        os.remove(filename)

    def update_NPC_list(self):
        self.NPCList = []
        for filename in glob.glob(self.NPCDir + "/*.json"):
            with open(filename, 'r') as f:
                data = json.load(f)
                npc = NPC.from_json(data)
                self.NPCList.append(npc)

########################################################### ACTIONS

    ### create or update save file for desired action
    def update_action_save(self, action):
        filename = self.actionDir + "/" + action.name.replace(" ", "_") + ".json"
        if action not in self.actionList:
            self.add_NPC(action)
        if os.path.exists(filename):
            print("overwriting action save!")
        with open(filename, 'w') as f:
            json.dump(action.to_json(), f)

    def delete_action_save(self, action):
        filename = self.actionDir + "/" + action.name.replace(" ", "_") + ".json"
        os.remove(filename)

    def update_action_list(self):
        self.actionList = []
        for filename in glob.glob(self.actionDir + "/*.json"):
            with open(filename, 'r') as f:
                data = json.load(f)
                action = Action.from_json(data)
                self.actionList.append(action)

########################################################### ACTIVITIES

    ### create or update save file for desired activity
    def update_activity_save(self, activity):
        filename = self.activityDir + "/" + activity.name.replace(" ", "_") + ".json"
        if activity not in self.activityList:
            self.add_NPC(activity)
        if os.path.exists(filename):
            print("overwriting activity save!")
        with open(filename, 'w') as f:
            json.dump(activity.to_json(), f)

    def delete_activity_save(self, activity):
        filename = self.activityDir + "/" + activity.name.replace(" ", "_") + ".json"
        os.remove(filename)

    def update_activity_list(self):
        self.activityList = []
        for filename in glob.glob(self.activityDir + "/*.json"):
            with open(filename, 'r') as f:
                data = json.load(f)
                activity = Activity.from_json(data)
                self.activityList.append(activity)

########################################################### EFFECTS

    ### create or update save file for desired effect
    def update_effect_save(self, effect):
        filename = self.effectDir + "/" + effect.name.replace(" ", "_") + ".json"
        if effect not in self.effectList:
            self.add_NPC(effect)
        if os.path.exists(filename):
            print("overwriting effect save!")
        with open(filename, 'w') as f:
            json.dump(effect.to_json(), f)

    def delete_effect_save(self, effect):
        filename = self.effectDir + "/" + effect.name.replace(" ", "_") + ".json"
        os.remove(filename)

    def update_effect_list(self):
        self.effectList = []
        for filename in glob.glob(self.effectDir + "/*.json"):
            with open(filename, 'r') as f:
                data = json.load(f)
                effect = Effect.from_json(data)
                self.effectList.append(effect)