# Flask
# from flask import Flask, render_template, url_for, request, redirect
from flask import *
# DeathWish Custom
import Game
import Assets
from Campaign import *
from Region import *
from Footing import *
from Landmark import *
from Effect import *
from Action import *
from Activity import *
from NPC import *
from Encounter import *

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
                campaign.mapGridJSON = request.form.get('mapObjects')
                print(campaign.mapGridJSON)
                campaign.update_party_landmark(Game.assets.landmarkList, Game.assets.regionList)
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
    @app.route('/GameMaster/Assets/Footing_<int:index><int:isNew>', methods=['GET', 'POST'])
    def EditFooting(index, isNew):
        if isNew < 1:
            footing = Game.assets.footingList[index]
        else:
            footing = Footing("blank", "path_to_image", 0, 0, 0)
        if request.method == 'POST':
            if request.form.get("action") == "save_footing_form":
                footing.name = request.form.get('footingName')
                footing.mapIconFile = request.form.get('mapIconFile')
                footing.terrainDifficulty = request.form.get('terrainDifficulty')
                footing.opacity = request.form.get('opacity')
                footing.solidity = request.form.get('solidity')
                if isNew == 1:
                    Game.assets.add_footing(footing)
                else:
                    Game.assets.footingList[index] = footing
                    Game.assets.update_footing_save(footing)
                if 'update_footing' in request.form:
                    return redirect(url_for('AssetsTop'))
            elif request.form.get("action") == "delete_footing_form":
                if isNew == 0:
                    Game.assets.delete_footing(index)
                return redirect(url_for('AssetsTop'))
        return render_template('EditFooting.html', footing=footing.to_json())
    
    ### display chosen objects attributes in editable forms
    @app.route('/GameMaster/Assets/Effect_<int:index><int:isNew>', methods=['GET', 'POST'])
    def EditEffect(index, isNew):
        if isNew < 1:
            effect = Game.assets.effectList[index]
        else:
            effect = Effect("blank", 0, 0, 0)
        if request.method == 'POST':
            if request.form.get("effect") == "save_effect_form":
                effect.name = request.form.get('effectName')
                effect.effectQuantity = request.form.get('effectQuantity')
                effect.effectType = request.form.get('effectType')
                effect.durationTurns = request.form.get('durationTurns')
                if isNew == 1:
                    Game.assets.add_effect(effect)
                else:
                    Game.assets.effectList[index] = effect
                    Game.assets.update_effect_save(effect)
                return redirect(url_for('AssetsTop'))
            elif request.form.get("effect") == "delete_effect_form":
                if isNew == 0:
                    Game.assets.delete_effect(index)
                return redirect(url_for('AssetsTop'))
        return render_template('EditEffect.html', effect=effect.to_json())

    ### display chosen objects attributes in editable forms
    @app.route('/GameMaster/Assets/Action_<int:index><int:isNew>', methods=['GET', 'POST'])
    def EditAction(index, isNew):
        if isNew < 1:
            action = Game.assets.actionList[index]
        else:
            action = Action("blank", 0, 0, 0, 0, 0, 0, 0, [])
        activityJSONS = [activity.to_json() for activity in Game.assets.activityList]
        if request.method == 'POST':
            if request.form.get("action") == "save_action_form":
                if 'delete_activity' in request.form:
                    del action.activityListIndexes[int(request.form['delete_activity'])]
                elif 'add_activity' in request.form:
                    action.activityListIndexes.append(int(request.form['add_activity']))
                else:
                    action.name = request.form.get('actionName')
                    action.movementRange = request.form.get('movementRange') 
                    action.setupTime = request.form.get('setupTime')
                    action.cooldownTime = request.form.get('cooldownTime')
                    action.staminaCost = request.form.get('staminaCost')
                    action.manaCost = request.form.get('manaCost') 
                    action.negationAmount = request.form.get('negationAmount') 
                    action.interruptStrength = request.form.get('interruptStrength')
                if isNew == 1:
                    Game.assets.add_action(action)
                else:
                    Game.assets.actionList[index] = action
                    Game.assets.update_action_save(action)
                if 'update_action' in request.form:
                    return redirect(url_for('AssetsTop'))
            elif request.form.get("action") == "delete_action_form":
                if isNew == 0:
                    Game.assets.delete_action(index)
                return redirect(url_for('AssetsTop'))
        return render_template('EditAction.html', action=action.to_json(), activities=activityJSONS)

    ### display chosen objects attributes in editable forms
    @app.route('/GameMaster/Assets/Activity_<int:index><int:isNew>', methods=['GET', 'POST'])
    def EditActivity(index, isNew):
        dummyMatrix = [[0 for _ in range(9)] for _ in range(9)]
        if isNew < 1:
            activity = Game.assets.activityList[index]
        else:
            activity = Activity("blank", dummyMatrix, False, [])
        effectJSONS = [effect.to_json() for effect in Game.assets.effectList]
        if request.method == 'POST':
            if request.form.get("activity") == "save_activity_form":
                if 'delete_effect' in request.form:
                    del activity.effectListIndexes[int(request.form['delete_effect'])]
                elif 'add_effect' in request.form:
                    activity.effectListIndexes.append(int(request.form['add_effect']))
                else:
                    activity.name = request.form.get('activityName')
                    activity.shape = json.loads(request.form.get('shapeData'))
                    activity.activityType = request.form.get('activityType')
                if isNew == 1:
                    Game.assets.add_activity(activity)
                else:
                    Game.assets.activityList[index] = activity
                    Game.assets.update_activity_save(activity)
                if 'update_activity' in request.form:
                    return redirect(url_for('AssetsTop'))
            elif request.form.get("activity") == "delete_activity_form":
                if isNew == 0:
                    Game.assets.delete_activity(index)
                return redirect(url_for('AssetsTop'))
        return render_template('EditActivity.html', activity=activity.to_json(), effects=effectJSONS)

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
                    if 'isParty' in request.form:
                        landmark.type = "party"
                    else:
                        landmark.type = "stationary"
                    landmark.name = request.form.get('landmarkName')
                    ### expect the user to type in the relative path
                    landmark.mapIconImgFile = request.form.get('mapIconImgFile')
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
            npc = NPC("blank", 0, 0, "path_to_image", "npc", [])
        actionJSONS = [action.to_json() for action in Game.assets.actionList]
        if request.method == 'POST':
            if request.form.get("action") == "save_NPC_form":
                if 'delete_action' in request.form:
                    del npc.actionListIndexes[int(request.form['delete_action'])]
                elif 'add_action' in request.form:
                    npc.actionListIndexes.append(int(request.form['add_action']))
                else:
                    npc.name = request.form.get('npcName')
                    npc.health = request.form.get('npcHealth')
                    ### only expect the user to type in the filename, not the relative path
                    npc.mapIconImgFile = request.form.get('mapIconImgFile')
                    if isNew == 1:
                        Game.assets.add_NPC(npc)
                    else:
                        Game.assets.NPCList[index] = npc
                        Game.assets.update_NPC_save(npc)
                if 'update_NPC' in request.form:
                    return redirect(url_for('AssetsTop'))
            elif request.form.get("action") == "delete_NPC_form":
                if isNew == 0:
                    Game.assets.delete_NPC(index)
                return redirect(url_for('AssetsTop'))
        return render_template('EditNPC.html', npc=npc.to_json(), actions=actionJSONS)

    ### display chosen objects attributes in editable forms
    @app.route('/GameMaster/Assets/Encounter_<int:index><int:isNew>', methods=['GET', 'POST'])
    def EditEncounter(index, isNew):
        dummyMatrix = [[0 for _ in range(8)] for _ in range(8)]
        if isNew == 0:
            encounter = Game.assets.encounterList[index]
        else:
            encounter = Encounter("New Encounter", dummyMatrix, "blank", None)
        footingJSONs = [ft.to_json() for ft in Game.assets.footingList]
        mapObjectJSONs = [mo.to_json() for mo in Game.assets.NPCList]
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'update_footing_form':
                encounter.name = request.form.get('encounterName')
                # transfer to object format
                encounter.footingMapIndexes = json.loads(request.form.get('footingData'))
                if isNew == 1:
                    Game.assets.add_encounter(encounter)
                else:
                    Game.assets.update_encounter_save(encounter)
            elif action == 'update_mapObjects_form':
                # keep in json format
                encounter.mapGridJSON = request.form.get('mapObjects')
                Game.assets.update_encounter_save(encounter)
                return redirect(url_for('AssetsTop'))
            elif action == 'delete_encounter_form':
                Game.assets.delete_encounter(index)
                return redirect(url_for('AssetsTop'))
        return render_template('EditEncounter.html', encounter=encounter.to_json(), footings=footingJSONs, mapObjects=mapObjectJSONs)

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
                campaign.mapGridJSON = request.form.get('mapObjects')
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
        Game.assets.curEncounter = Game.assets.encounterList[index]
        encounter = Game.assets.curEncounter
        mapObjectList = encounter.create_map_object_list(Game.assets.NPCList)
        mapObjectJSONs = [mo.to_json() for mo in Game.assets.NPCList]
        footingJSONs = [ft.to_json() for ft in Game.assets.footingList]
        actionJSONS = [action.to_json() for action in Game.assets.actionList]
        return render_template('RunEncounter.html', encounter=encounter.to_json(), mapObjects=mapObjectJSONs, actions=actionJSONS, footings=footingJSONs, mapObjectList=mapObjectList)

    ### Action contains modified info 
    @app.route('/GameMaster/CompleteAction/Action_<string:mapObjectID>_<int:actionListIndex>', methods=['GET', 'POST'])
    def CompleteAction(mapObjectID, actionListIndex):
        npc = Game.assets.NPCList[int(mapObjectID.split("-")[1])]
        activityJSONS = [ac.to_json() for ac in Game.assets.activityList]
        action = Game.assets.actionList[actionListIndex]
        footingJSONs = [ft.to_json() for ft in Game.assets.footingList]
        encounter = Game.assets.curEncounter
        mapObjectJSONs = [mo.to_json() for mo in Game.assets.NPCList]
        # modify action from encounter state, incorporates character/npc stats, equipment modifiers, footing modifiers, status conditions
        return render_template('CompleteAction.html', encounter=encounter.to_json(), mapObjects=mapObjectJSONs, footings=footingJSONs, action=action.to_json(), npc=npc.to_json(), activities=activityJSONS, executorID=mapObjectID)

    return app