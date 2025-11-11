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
from Tangible import *
from Encounter import *
# re
import re

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
        return render_template('GameMaster.html', campaigns=Game.assets.campaignDict)

    @app.route('/GameMaster/EditCampaign/Campaign/<name>/<int:isNew>', methods=['GET', 'POST'])
    def EditCampaign(name, isNew):
        defaultRegion = next(iter(Game.assets.regionDict))
        dummyMatrix = [[defaultRegion for _ in range(8)] for _ in range(8)]
        if isNew == 0:
            campaign = Game.assets.campaignDict[name]
        else:
            campaign = Campaign("New Campaign", dummyMatrix, "blank", None)
        regionJSONs = {rn: rg.to_json() for rn, rg in Game.assets.regionDict.items()}
        landmarkJSONs = {ln: lm.to_json() for ln, lm in Game.assets.landmarkDict.items()}
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'update_region_form':
                campaign.name = request.form.get('campaignName')
                # transfer to object format
                campaign.regionMapNames = json.loads(request.form.get('regionData'))
                if isNew == 1:
                    Game.assets.add_campaign(campaign)
                else:
                    Game.assets.update_campaign_save(campaign)
            elif action == 'update_landmarks_form':
                # keep in json format
                campaign.mapGridJSON = request.form.get('mapObjects')
                print(campaign.mapGridJSON)
                campaign.update_party_landmark()
                Game.assets.update_campaign_save(campaign)
                return redirect(url_for('GameMaster'))
            elif action == 'delete_campaign_form':
                Game.assets.delete_campaign(name)
                return redirect(url_for('GameMaster'))
        return render_template('EditCampaign.html', campaign=campaign.to_json(), regions=regionJSONs, landmarks=landmarkJSONs)

    ### display all global objects as URLs in a big list (tangibles (equipment, weapons, items), encounters, regions, and NPCs (monsters, humanoids))
    @app.route('/GameMaster/Assets', methods=['GET', 'POST'])
    def AssetsTop():
        return render_template('AssetsTop.html', assets=Game.assets)

    ### display chosen objects attributes in editable forms
    @app.route('/GameMaster/Assets/Region/<name>/<int:isNew>', methods=['GET', 'POST'])
    def EditRegion(name, isNew):
        if isNew < 1:
            region = Game.assets.regionList[name]
        else:
            region = Region("blank", "path_to_image", [])
        encounterJSONS = {en: ec.to_json() for en, ec in Game.assets.encounterDict.items()}
        if request.method == 'POST':
            if request.form.get("action") == "save_region_form":
                if 'delete_encounter' in request.form:
                    del region.encounterListNames[request.form['delete_encounter']]
                elif 'add_encounter' in request.form:
                    region.encounterListNames.append(request.form['add_encounter'])
                else:
                    regionName = request.form.get('regionName')
                    ### only expect the user to type in the filename, not the relative path
                    mapIconImgFile = request.form.get('mapIconImgFile')
                    region = Region(regionName, mapIconImgFile, region.encounterListNames)
                if isNew == 1:
                    Game.assets.add_region(region)
                else:
                    Game.assets.update_region_save(region)
                if 'update_region' in request.form:
                    return redirect(url_for('AssetsTop'))
            elif request.form.get("action") == "delete_region_form":
                if isNew == 0:
                    Game.assets.delete_region(name)
                return redirect(url_for('AssetsTop'))
        return render_template('EditRegion.html', region=region.to_json(), encounters=encounterJSONS)

    ### display chosen objects attributes in editable forms
    @app.route('/GameMaster/Assets/Footing/<name>/<int:isNew>', methods=['GET', 'POST'])
    def EditFooting(name, isNew):
        print("rendering template")
        if isNew < 1:
            footing = Game.assets.footingDict[name]
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
                    Game.assets.update_footing_save(footing)
                if 'update_footing' in request.form:
                    return redirect(url_for('AssetsTop'))
            elif request.form.get("action") == "delete_footing_form":
                if isNew == 0:
                    Game.assets.delete_footing(name)
                return redirect(url_for('AssetsTop'))
        print("rendering template")
        return render_template('EditFooting.html', footing=footing.to_json())
    
    ### display chosen objects attributes in editable forms
    @app.route('/GameMaster/Assets/Tangible/<name>/<int:isNew>', methods=['GET', 'POST'])
    def EditTangible(name, isNew):
        if isNew == 0:
            tangible = Game.assets.tangibleDict[name]
        else:
            tangible = Tangible(name="blank", health=0, weight=0, description="blank", mapIconImgFile="path_to_image", currentEffectJSONList=[])
        if request.method == 'POST':
            if request.form.get("action") == "save_tangible_form":
                tangible.name = request.form.get('name')
                tangible.health = request.form.get('health')
                tangible.weight = request.form.get('weight')
                tangible.description = request.form.get('description')
                tangible.mapIconImgFile = request.form.get('mapIconImgFile')
                if isNew == 1:
                    Game.assets.add_tangible(tangible)
                else:
                    Game.assets.update_tangible_save(tangible)
                if 'update_tangible' in request.form:
                    return redirect(url_for('AssetsTop'))
            elif request.form.get("action") == "delete_tangible_form":
                if isNew == 0:
                    Game.assets.delete_tangible(name)
                return redirect(url_for('AssetsTop'))
        return render_template('EditTangible.html', tangible=tangible.to_json())

    ### display chosen objects attributes in editable forms
    @app.route('/GameMaster/Assets/Effect/<name>/<int:isNew>', methods=['GET', 'POST'])
    def EditEffect(name, isNew):
        if isNew < 1:
            effect = Game.assets.effectDict[name]
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
                    Game.assets.update_effect_save(effect)
                return redirect(url_for('AssetsTop'))
            elif request.form.get("effect") == "delete_effect_form":
                if isNew == 0:
                    Game.assets.delete_effect(name)
                return redirect(url_for('AssetsTop'))
        return render_template('EditEffect.html', effect=effect.to_json())

    ### display chosen objects attributes in editable forms
    @app.route('/GameMaster/Assets/Action/<name>/<int:isNew>', methods=['GET', 'POST'])
    def EditAction(name, isNew):
        if isNew < 1:
            action = Game.assets.actionDict[name]
        else:
            action = Action(name="blank", staminaCost=0, manaCost=0, activityListNames=[])
        activityJSONS = {an: ac.to_json() for an, ac in Game.assets.activityDict.items()}
        if request.method == 'POST':
            if request.form.get("action") == "save_action_form":
                if 'delete_activity' in request.form:
                    del action.activityListNames[request.form['delete_activity']]
                elif 'add_activity' in request.form:
                    action.activityListNames.append(request.form['add_activity'])
                else:
                    action.name = request.form.get('actionName')
                    action.staminaCost = request.form.get('staminaCost')
                    action.manaCost = request.form.get('manaCost')
                if isNew == 1:
                    Game.assets.add_action(action)
                else:
                    Game.assets.update_action_save(action)
                if 'update_action' in request.form:
                    return redirect(url_for('AssetsTop'))
            elif request.form.get("action") == "delete_action_form":
                if isNew == 0:
                    Game.assets.delete_action(name)
                return redirect(url_for('AssetsTop'))
        return render_template('EditAction.html', action=action.to_json(), activities=activityJSONS)

    ### display chosen objects attributes in editable forms
    @app.route('/GameMaster/Assets/Activity/<name>/<int:isNew>', methods=['GET', 'POST'])
    def EditActivity(name, isNew):
        dummyMatrix = [[0 for _ in range(9)] for _ in range(9)]
        if isNew < 1:
            activity = Game.assets.activityDict[name]
        else:
            activity = Activity(name="blank", shape=dummyMatrix, type=None,
                                effectNameList=[], setupTime=0, cooldownTime=0,
                                negationAmount=0, interruptStrength=0)
        effectJSONS = {en: ef.to_json() for en, ef in Game.assets.effectDict.items()}
        if request.method == 'POST':
            if request.form.get("activity") == "save_activity_form":
                if 'delete_effect' in request.form:
                    del activity.effectNameList[request.form['delete_effect']]
                elif 'add_effect' in request.form:
                    activity.effectNameList.append(request.form['add_effect'])
                else:
                    activity.name = request.form.get('name')
                    activity.shape = json.loads(request.form.get('shapeData'))
                    activity.type = request.form.get('type')
                if isNew == 1:
                    Game.assets.add_activity(activity)
                else:
                    Game.assets.update_activity_save(activity)
                if 'update_activity' in request.form:
                    return redirect(url_for('AssetsTop'))
            elif request.form.get("activity") == "delete_activity_form":
                if isNew == 0:
                    Game.assets.delete_activity(name)
                return redirect(url_for('AssetsTop'))
        return render_template('EditActivity.html', activity=activity.to_json(), effects=effectJSONS)

    ### display chosen objects attributes in editable forms
    @app.route('/GameMaster/Assets/Landmark/<name>/<int:isNew>', methods=['GET', 'POST'])
    def EditLandmark(name, isNew):
        if isNew < 1:
            landmark = Game.assets.landmarkDict[name]
        else:
            landmark = Landmark("blank", "path_to_image", False, [])
        encounterJSONS = {en: ec.to_json() for en, ec in Game.assets.encounterDict.items()}
        if request.method == 'POST':
            if request.form.get("action") == "save_landmark_form":
                if 'delete_encounter' in request.form:
                    del landmark.encounterListNames[request.form['delete_encounter']]
                elif 'add_encounter' in request.form:
                    landmark.encounterListNames.append(request.form['add_encounter'])
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
                    Game.assets.update_landmark_save(landmark)
                if 'update_landmark' in request.form:
                    return redirect(url_for('AssetsTop'))
            elif request.form.get("action") == "delete_landmark_form":
                if isNew == 0:
                    Game.assets.delete_landmark(name)
                return redirect(url_for('AssetsTop'))
        return render_template('EditLandmark.html', landmark=landmark.to_json(), encounters=encounterJSONS)

    ### display chosen objects attributes in editable forms
    @app.route('/GameMaster/Assets/NPC/<name>/<int:isNew>', methods=['GET', 'POST'])
    def EditNPC(name, isNew):
        if isNew < 1:
            npc = Game.assets.NPCDict[name]
        else:
            npc = NPC(name="blank", health=0, stamina=0, mana=0, actionCount=2,
                      weight=0, mapIconImgFile="path_to_image", type="npc", actionListNames=[], currentEffectJSONList=[])
        actionJSONS = {an: ac.to_json() for an, ac in Game.assets.actionDict.items()}
        if request.method == 'POST':
            if request.form.get("action") == "save_NPC_form":
                if 'delete_action' in request.form:
                    del npc.actionListNames[request.form['delete_action']]
                elif 'add_action' in request.form:
                    npc.actionListNames.append(request.form['add_action'])
                else:
                    npc.name = request.form.get('npcName')
                    npc.health = request.form.get('npcHealth')
                    ### only expect the user to type in the filename, not the relative path
                    npc.mapIconImgFile = request.form.get('mapIconImgFile')
                    if isNew == 1:
                        Game.assets.add_NPC(npc)
                    else:
                        Game.assets.update_NPC_save(npc)
                if 'update_NPC' in request.form:
                    return redirect(url_for('AssetsTop'))
            elif request.form.get("action") == "delete_NPC_form":
                if isNew == 0:
                    Game.assets.delete_NPC(name)
                return redirect(url_for('AssetsTop'))
        return render_template('EditNPC.html', npc=npc.to_json(), actions=actionJSONS)

    ### display chosen objects attributes in editable forms
    @app.route('/GameMaster/Assets/Encounter/<name>/<int:isNew>', methods=['GET', 'POST'])
    def EditEncounter(name, isNew):
        defaultFooting = next(iter(Game.assets.footingDict))
        dummyMatrix = [[defaultFooting for _ in range(8)] for _ in range(8)]
        if isNew == 0:
            encounter = Game.assets.encounterDict[name]
        else:
            encounter = Encounter("New Encounter", dummyMatrix, "blank", None)
        footingJSONs = {fn: ft.to_json() for fn, ft in Game.assets.footingDict.items()}
        mapObjectJSONs = {mon: mo.to_json() for mon, mo in Game.assets.allMapObjectsDict.items()}
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'update_footing_form':
                encounter.name = request.form.get('encounterName')
                # transfer to object format
                encounter.footingMap = json.loads(request.form.get('footingData'))
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
                Game.assets.delete_encounter(name)
                return redirect(url_for('AssetsTop'))
        return render_template('EditEncounter.html', encounter=encounter.to_json(), footings=footingJSONs, mapObjects=mapObjectJSONs)

    ### display chosen campaign world map, premise, recent party events, etc.
    @app.route('/GameMaster/RunCampaign/Campaign/<name>/<int:startNew>', methods=['GET', 'POST'])
    def RunCampaign(name, startNew):
        if (startNew == 1):
            Game.assets.curCampaign = Game.assets.campaignDict[name]
        campaign = Game.assets.curCampaign
        print(campaign.availableEncounterNames)
        processQueue.put(("refreshCampaign", campaign))
        processQueue.put(("gameState", 'campaign'))
        regionJSONs = {rn: rg.to_json() for rn, rg in Game.assets.regionDict.items()}
        landmarkJSONs = {ln: lm.to_json() for ln, lm in Game.assets.landmarkDict.items()}
        encounterJSONs = {en: ec.to_json() for en, ec in Game.assets.encounterDict.items()}
        # update assets if landmarks change
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'update_landmarks_form':
                campaign.mapGridJSON = request.form.get('mapObjects')
                campaign.update_party_landmark()
                Game.assets.update_campaign_save(campaign)
                processQueue.put(("refreshCampaign", campaign))
        return render_template('RunCampaign.html', campaign=campaign.to_json(), regions=regionJSONs, landmarks=landmarkJSONs, encounters=encounterJSONs)

    ### display encounter map, party/enemy stats, party member/NPC headshot 
    @app.route('/GameMaster/RunEncounter/Encounter/<name>/<int:startNew>', methods=['GET', 'POST'])
    def RunEncounter(name, startNew):
        if (startNew == 1):
            Game.assets.curEncounter = Game.assets.encounterDict[name]
            Game.assets.curEncounter.create_map_object_list()
        encounter = Game.assets.curEncounter
        processQueue.put(("refreshEncounter", encounter))
        processQueue.put(("gameState", 'encounter'))
        mapObjectJSONs = {mon: mo.to_json() for mon, mo in Game.assets.allMapObjectsDict.items()}
        footingJSONs = {fn: ft.to_json() for fn, ft in Game.assets.footingDict.items()}
        actionJSONS = {an: ac.to_json() for an, ac in Game.assets.actionDict.items()}
        return render_template('RunEncounter.html', encounter=encounter.to_json(), mapObjects=mapObjectJSONs, actions=actionJSONS, footings=footingJSONs, mapObjectList=encounter.mapObjectList)

    ### Action contains modified info 
    @app.route('/GameMaster/CompleteAction/Action/<string:mapObjectID>/<actionListName>', methods=['GET', 'POST'])
    def CompleteAction(mapObjectID, actionListName):
        activityJSONS = {an: ac.to_json() for an, ac in Game.assets.activityDict.items()}
        turnAction = Game.assets.actionDict[actionListName]
        footingJSONs = {fn: ft.to_json() for fn,ft in Game.assets.footingDict.items()}
        encounter = Game.assets.curEncounter
        npc = encounter.get_object_from_object_id(mapObjectID)
        mapObjectJSONs = {mon: mo.to_json() for mon, mo in Game.assets.allMapObjectsDict.items()}
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'submit_action_form':
                activityEntryNames = {key: request.form[key] for key in request.form if key.endswith('_name')}
                # for each activity in action, resolve pre/post reactions, then resolve effects
                for entryName in activityEntryNames:
                    match = re.match(r'activity_(\d.*)_name', entryName)
                    submissionNum = match.group(1)
                    dataEntry = request.form.get(f'activity_{submissionNum}_data')
                    nameEntry = request.form.get(entryName)
                    activity = Game.assets.activityDict[nameEntry]
                    # reactionDict = encounter.get_pre_activity_counters(activity, Game.assets)
                    # pre reactions
                    # if (len(reactionDict.keys()) > 0):
                    #     return render_template('CompleteAction.html', encounter=encounter.to_json(), mapObjects=mapObjectJSONs,
                    #                             footings=footingJSONs, action=turnAction.to_json(), npc=npc.to_json(),
                    #                             activities=activityJSONS, executorID=mapObjectID, reactionDict=reactionDict)
                    # else:
                        # resolve activity effects
                    encounter.resolve_activity_effects(activity, mapObjectID, dataEntry)
                        # post reactions
                        # reactionDict = encounter.get_post_activity_counters(activity, Game.assets)
                        # if (len(reactionDict.keys()) > 0):
                        #     return render_template('CompleteAction.html', encounter=encounter.to_json(), mapObjects=mapObjectJSONs,
                        #                             footings=footingJSONs, action=turnAction.to_json(), npc=npc.to_json(),
                        #                             activities=activityJSONS, executorID=mapObjectID, reactionDict=reactionDict)
                        # else:
                            # return to the current encounter
                encounter.end_NPC_action(mapObjectID)
                return redirect(url_for('RunEncounter', name="current", startNew=0))
        return render_template('CompleteAction.html', encounter=encounter.to_json(), mapObjects=mapObjectJSONs,
                                                footings=footingJSONs, action=turnAction.to_json(), npc=npc.to_json(),
                                                activities=activityJSONS, executorID=mapObjectID, reactionDict=None)
    return app