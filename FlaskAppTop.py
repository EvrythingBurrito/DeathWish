# Flask
# from flask import Flask, render_template, url_for, request, redirect
from flask import *
# DeathWish Custom
import Game
from Campaign import *
from Region import *
from Landmark import *
from NPC import *
from Encounter import *
from Monster import *
from Sentient import *

import DeathWish

def create_flask_app(processQueue):
    app = Flask(__name__)

    @app.route('/')
    def Title():
        return render_template('Title.html')

    ############################################################################################# Game Master Pages
    @app.route('/GameMaster')
    def GameMaster():
        processQueue.put(("gameState", 'title'))
        return render_template('GameMaster.html', campaigns=Game.assets.campaignList)

    @app.route('/GameMaster/EditCampaign/Campaign_<int:index><int:isNew>', methods=['GET', 'POST'])
    def EditCampaign(index, isNew):
        dummyMatrix = [[0 for _ in range(8)] for _ in range(8)]
        if isNew == 0:
            campaign = Game.assets.campaignList[index]
        else:
            campaign = Campaign("New Campaign", dummyMatrix, "blank", None)
        regionJSONs = [rg.to_json() for rg in Game.assets.regionList]
        landmarkJSONs = [lm.to_json() for lm in Game.assets.landmarkList]
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'update_region_form':
                campaign.name = request.form.get('campaignName')
                # transfer to object format
                campaign.regionMapIndexes = json.loads(request.form.get('regionData'))
                if isNew == 1:
                    Game.assets.add_campaign(campaign)
                else:
                    Game.assets.update_campaign_save(campaign)
            elif action == 'update_landmarks_form':
                # keep in json format
                campaign.mapGridJSON = request.form.get('landmarkObjects')
                # campaign.update_party_landmark(Game.assets.landmarkList, Game.assets.regionList)
                Game.assets.update_campaign_save(campaign)
                return redirect(url_for('GameMaster'))
            elif action == 'delete_campaign_form':
                Game.assets.delete_campaign(index)
                return redirect(url_for('GameMaster'))
        return render_template('EditCampaign.html', campaign=campaign.to_json(), regions=regionJSONs, landmarks=landmarkJSONs)

    ### display all global objects as URLs in a big list (tangibles (equipment, weapons, items), encounters, regions, and NPCs (monsters, humanoids))
    @app.route('/GameMaster/Assets', methods=['GET', 'POST'])
    def AssetsTop():
        return render_template('AssetsTop.html', assets=Game.assets)

    ### display chosen objects attributes in editable forms
    @app.route('/GameMaster/Assets/Region_<int:index><int:isNew>', methods=['GET', 'POST'])
    def EditRegion(index, isNew):
        if isNew < 1:
            region = Game.assets.regionList[index]
        else:
            region = Region("blank", "path_to_image", [])
        print(region.encounterListIndexes)
        encounterJSONS = [en.to_json() for en in Game.assets.encounterList]
        if request.method == 'POST':
            if request.form.get("action") == "save_region_form":
                if 'delete_encounter' in request.form:
                    del region.encounterListIndexes[int(request.form['delete_encounter'])]
                elif 'add_encounter' in request.form:
                    region.encounterListIndexes.append(int(request.form['add_encounter']))
                else:
                    regionName = request.form.get('regionName')
                    ### only expect the user to type in the filename, not the relative path
                    mapIconImgFile = request.form.get('mapIconImgFile')
                    region = Region(regionName, mapIconImgFile, region.encounterListIndexes)
                if isNew == 1:
                    Game.assets.add_region(region)
                else:
                    Game.assets.regionList[index] = region
                    Game.assets.update_region_save(region)
                if 'update_region' in request.form:
                    return redirect(url_for('AssetsTop'))
            elif request.form.get("action") == "delete_region_form":
                if isNew == 0:
                    Game.assets.delete_region(index)
                return redirect(url_for('AssetsTop'))
        return render_template('EditRegion.html', region=region.to_json(), encounters=encounterJSONS)

    ### display chosen objects attributes in editable forms
    @app.route('/GameMaster/Assets/Landmark_<int:index><int:isNew>', methods=['GET', 'POST'])
    def EditLandmark(index, isNew):
        if isNew < 1:
            landmark = Game.assets.landmarkList[index]
        else:
            landmark = Landmark("blank", "path_to_image", False, [])
        encounterJSONS = [en.to_json() for en in Game.assets.encounterList]
        if request.method == 'POST':
            if request.form.get("action") == "save_landmark_form":
                if 'delete_encounter' in request.form:
                    del landmark.encounterListIndexes[int(request.form['delete_encounter'])]
                elif 'add_encounter' in request.form:
                    landmark.encounterListIndexes.append(int(request.form['add_encounter']))
                else:
                    isParty = 'isParty' in request.form
                    landmarkName = request.form.get('landmarkName')
                    ### expect the user to type in the relative path
                    mapIconImgFile = request.form.get('mapIconImgFile')
                    landmark = Landmark(landmarkName, mapIconImgFile, isParty, landmark.encounterListIndexes)
                if isNew == 1:
                    Game.assets.add_landmark(landmark)
                else:
                    Game.assets.landmarkList[index] = landmark
                    Game.assets.update_landmark_save(landmark)
                if 'update_landmark' in request.form:
                    return redirect(url_for('AssetsTop'))
            elif request.form.get("action") == "delete_landmark_form":
                if isNew == 0:
                    Game.assets.delete_landmark(index)
                return redirect(url_for('AssetsTop'))
        return render_template('EditLandmark.html', landmark=landmark.to_json(), encounters=encounterJSONS)

    ### display chosen objects attributes in editable forms
    @app.route('/GameMaster/Assets/NPC_<int:index><int:isNew>', methods=['GET', 'POST'])
    def EditNPC(index, isNew):
        if isNew < 1:
            npc = Game.assets.NPCList[index]
        else:
            npc = NPC("blank", 0, 0, "path_to_image")
        if request.method == 'POST':
            if request.form.get("action") == "save_NPC_form":
                npcName = request.form.get('npcName')
                npcType = request.form.get('npcType')
                npcHealth = request.form.get('npcHealth')
                ### only expect the user to type in the filename, not the relative path
                mapIconImgFile = request.form.get('mapIconImgFile')
                if (npcType == "Monster"):
                    npc = Monster(npcName, 0, npcHealth, mapIconImgFile)
                else:
                    npc = Sentient(npcName, 0, npcHealth, mapIconImgFile)
                if isNew == 1:
                    Game.assets.add_NPC(npc)
                else:
                    Game.assets.NPCList[index] = npc
                    Game.assets.update_NPC_save(npc)
            elif request.form.get("action") == "delete_NPC_form":
                if isNew < 1:
                    Game.assets.delete_NPC(index)
            return redirect(url_for('AssetsTop'))
        return render_template('EditNPC.html', npc=npc.to_json())

    ### display chosen objects attributes in editable forms
    @app.route('/GameMaster/Assets/Encounter_<int:index><int:isNew>', methods=['GET', 'POST'])
    def EditEncounter(index, isNew):
        if isNew < 1:
            encounter = Game.assets.encounterList[index]
        else:
            encounter = Encounter("blank", [], "")
        npcJSONs = [npc.to_json() for npc in Game.assets.NPCList]
        if request.method == 'POST':
            if request.form.get("action") == "save_encounter_form":
                encounterName = request.form.get('encounterName')
                encounterMap = request.form.get('mapData')
                encounter = Encounter(encounterName, encounterMap, "")
                if isNew == 1:
                    Game.assets.add_encounter(encounter)
                else:
                    Game.assets.encounterList[index] = encounter
                    Game.assets.update_encounter_save(encounter)
            elif request.form.get("action") == "delete_encounter_form":
                if isNew == 0:
                    Game.assets.delete_encounter(index)
            return redirect(url_for('AssetsTop'))
        return render_template('EditEncounter.html', encounter=encounter.to_json(), mapObjects=npcJSONs)

    ### display chosen campaign world map, premise, recent party events, etc.
    @app.route('/GameMaster/RunCampaign/Campaign_<int:index>', methods=['GET', 'POST'])
    def RunCampaign(index):
        campaign = Game.assets.campaignList[index]
        processQueue.put(("refreshCampaign", campaign))
        processQueue.put(("gameState", 'campaign'))
        regionJSONs = [rg.to_json() for rg in Game.assets.regionList]
        landmarkJSONs = [lm.to_json() for lm in Game.assets.landmarkList]
        encounterJSONs = [en.to_json() for en in Game.assets.encounterList]
        # update assets if landmarks change
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'update_landmarks_form':
                campaign.mapGridJSON = request.form.get('landmarkObjects')
                campaign.update_party_landmark(Game.assets.landmarkList, Game.assets.regionList)
                # print(campaign.partyLocation)
                # print(campaign.availableEncounterIndexes)
                Game.assets.campaignList[index] = campaign
                Game.assets.update_campaign_save(campaign)
                print(len(Game.assets.campaignList))
                processQueue.put(("refreshCampaign", campaign))
        return render_template('RunCampaign.html', campaign=campaign.to_json(), regions=regionJSONs, landmarks=landmarkJSONs, encounters=encounterJSONs)

    ### display encounter map, party/enemy stats, party member/NPC headshot 
    @app.route('/GameMaster/RunEncounter/Encounter_<int:index>', methods=['GET', 'POST'])
    def RunEncounter(index):
        encounter = Game.assets.encounterList[index]
        return render_template('RunEncounter.html', encounter=encounter.to_json())

    return app