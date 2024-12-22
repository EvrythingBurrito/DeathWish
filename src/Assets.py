import json
import os
from Region import Region
from Campaign import Campaign
from NPC import NPC
import glob

class Assets:
    def __init__(self):
        self.campaignDir = "Assets/Campaigns"
        self.regionDir = "Assets/Regions"
        self.NPCDir = "Assets/NPCs"
        ### initialize lists
        self.campaignList = []
        self.update_campaign_list()
        self.regionList = []
        self.update_region_list()
        self.tangibleList = []
        self.EncounterList = []
        self.NPCList = []
        self.update_NPC_list()

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

    def add_NPC(self, NPC):
        self.NPCList.append(NPC)
        self.update_NPC_save(NPC)
    def delete_NPC(self, index):
        self.delete_NPC_save(self.NPCList[index])
        del self.NPCList[index]

###########################################################
#################### SERIALIZATION ########################
###########################################################

########################################################### CAMPAIGNS
    ### create or update save file for desired campaign
    def update_campaign_save(self, campaign):
        filename = self.campaignDir + "/" + campaign.name.replace(" ", "_") + ".json"
        if campaign not in self.campaignList:
            self.add_campaign(campaign)
        if os.path.exists(filename):
            print("overwriting campaign save!")
        with open(filename, 'w') as f:
            json.dump(campaign.to_json(), f)

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
