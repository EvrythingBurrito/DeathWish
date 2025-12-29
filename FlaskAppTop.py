# Flask
# from flask import Flask, render_template, url_for, request, redirect
from flask import *
from flask import Flask, session
from flask_socketio import SocketIO, join_room, emit
import uuid
import time
# DeathWish Custom
import Game
import Assets
import copy
from Campaign import *
from Region import *
from Footing import *
from Landmark import *
from Effect import *
from Action import *
from Activity import *
from Character import *
from PlayerCharacter import *
from Tangible import *
from Encounter import *
# re
import re

import DeathWish

def create_flask_app(processQueue):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'my_secret_key'
    socketio = SocketIO(app)

    # { "user_id": {"last_seen": timestamp, "current_page": url} }
    ACTIVE_USERS = {}

    @socketio.on('connect')
    def handle_connect():
        user_id = session.get('user_id')
        role = session.get('user_role')
        # join a room for role (player name, or GM)
        join_room(role)
        # mark them as 'Connected' in ACTIVE_USERS
        if user_id in ACTIVE_USERS:
            ACTIVE_USERS[user_id]['socket_active'] = True

    @app.before_request
    def setup_user():
        # 1. Ensure the user has an ID
        if 'user_id' not in session:
            session['user_id'] = str(uuid.uuid4())
            session['user_role'] = 'Player'
        # 2. Update the registry with their ID and the page they are hitting
        user_id = session['user_id']
        ACTIVE_USERS[user_id] = {
            "last_seen": time.time(),
            "current_page": request.path, # e.g., /map or /inventory
            "role": session.get('user_role', 'Player')
        }

    def update_other_rooms(data):
        my_id = session.get('user_id')
        for user_id, user_data in ACTIVE_USERS.items():
            if user_id != my_id:
                role = user_data["role"]
                print(f"emiting game event for role {role}")
                socketio.emit('game_event', data, room=role)

    @app.context_processor
    def inject_user_role():
        # Keep this! It makes {% if current_user_role == 'GM' %} work
        return dict(current_user_role=session.get('user_role', 'Player'))

    @app.route('/', methods=['GET'])
    def Title():
        if 'session_client_id' not in session:
            new_id = str(uuid.uuid4())
            session['session_client_id'] = new_id
            print(f"New client connected with ID: {new_id}")
        player_characters = {}
        for charName, character in Game.assets.CharacterDict.items():
            if character.type == "player_character":
                player_characters[charName] = character
        return render_template('Title.html', player_characters=player_characters)

    @app.route('/GameMaster')
    def GameMaster():
        session['user_role'] = "GM"
        processQueue.put(("gameState", 'title'))
        return render_template('GameMaster.html', campaigns=Game.assets.campaignDict, )

    @app.route('/EditPlayerCharacter/<name>/<int:isNew>', methods=['GET', 'POST'])
    def EditPlayerCharacter(name, isNew):
        if isNew < 1:
            character = Game.assets.CharacterDict[name]
        else:
            character = PlayerCharacter(name="blank", health=0, maxHealth=0,
                                  stamina=0, maxStamina=0, mana=0, maxMana=0,
                                  actionCount=2, maxActionCount=2, weight=0,
                                  dexterity=0, strength=0, instinct=0, intellect=0,
                                  mapIconImgFile="path_to_image", type="player_character",
                                  actionListNames=[], currentEffectJSONList=[])
        actionJSONS = {an: ac.to_json() for an, ac in Game.assets.actionDict.items()}
        if request.method == 'POST':
            if request.form.get("action") == "save_character_form":
                if 'delete_action' in request.form:
                    del character.actionListNames[request.form['delete_action']]
                elif 'add_action' in request.form:
                    character.actionListNames.append(request.form['add_action'])
                else:
                    character.name = request.form.get('characterName')
                    character.health = int(request.form.get('characterHealth'))
                    character.maxHealth = int(request.form.get('characterHealth'))
                    # FIXME
                    character.stamina = int(request.form.get('characterHealth'))
                    character.maxStamina = int(request.form.get('characterHealth'))
                    character.mana = int(request.form.get('characterHealth'))
                    character.maxMana = int(request.form.get('characterHealth'))
                    character.dexterity = 10
                    character.strength = 10
                    character.instinct = 10
                    character.intellect = 10
                    ### only expect the user to type in the filename, not the relative path
                    character.mapIconImgFile = request.form.get('mapIconImgFile')
                    if isNew == 1:
                        Game.assets.add_character(character)
                    else:
                        Game.assets.update_character_save(character)
                if 'update_character' in request.form:
                    return redirect(url_for('AssetsTop'))
            elif request.form.get("action") == "delete_character_form":
                if isNew == 0:
                    Game.assets.delete_character(name)
                return redirect(url_for('AssetsTop'))
        return render_template('EditPlayerCharacter.html', character=character.to_json(), actions=actionJSONS)

    @app.route('/RunPlayerCharacter/<name>', methods=['GET', 'POST'])
    def RunPlayerCharacter(name):
        session['user_role'] = name
        footingJSONs = {fn: ft.to_json() for fn, ft in Game.assets.footingDict.items()}
        mapObjectJSONs = {mon: mo.to_json() for mon, mo in Game.assets.allMapObjectsDict.items()}
        if Game.assets.is_current_encounter():
            player_character = Game.assets.curEncounter.get_object_from_object_id(f"player_character-{name}-0")
        else:
            player_character = Game.assets.CharacterDict[name]
        actionJSONS = {an: ac.modify_from_character(player_character).to_json() for an, ac in Game.assets.actionDict.items()}
        encounter = Game.assets.curEncounter
        return render_template('RunPlayerCharacter.html', encounter=encounter.to_json(),
                               mapObjects=mapObjectJSONs, actions=actionJSONS, footings=footingJSONs,
                               mapObjectList=encounter.mapObjectList, character=player_character.to_json())

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
                campaign.update_party_landmark()
                Game.assets.update_campaign_save(campaign)
                return redirect(url_for('GameMaster'))
            elif action == 'delete_campaign_form':
                Game.assets.delete_campaign(name)
                return redirect(url_for('GameMaster'))
        return render_template('EditCampaign.html', campaign=campaign.to_json(), regions=regionJSONs, landmarks=landmarkJSONs)

    ### display all global objects as URLs in a big list (tangibles (equipment, weapons, items), encounters, regions, and Characters (monsters, humanoids))
    @app.route('/GameMaster/Assets', methods=['GET', 'POST'])
    def AssetsTop():
        return render_template('AssetsTop.html', assets=Game.assets)

    ### display chosen objects attributes in editable forms
    @app.route('/GameMaster/Assets/Region/<name>/<int:isNew>', methods=['GET', 'POST'])
    def EditRegion(name, isNew):
        if isNew < 1:
            region = Game.assets.regionDict[name]
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
        return render_template('EditFooting.html', footing=footing.to_json())
    
    ### display chosen objects attributes in editable forms
    @app.route('/GameMaster/Assets/Tangible/<name>/<int:isNew>', methods=['GET', 'POST'])
    def EditTangible(name, isNew):
        if isNew == 0:
            tangible = Game.assets.tangibleDict[name]
        else:
            tangible = Tangible(name="blank", health=0, maxHealth=0, weight=0,
                                description="blank", mapIconImgFile="path_to_image", currentEffectJSONList=[])
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
                    action.staminaCost = int(request.form.get('staminaCost'))
                    action.manaCost = int(request.form.get('manaCost'))
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
    @app.route('/GameMaster/Assets/Character/<name>/<int:isNew>', methods=['GET', 'POST'])
    def EditCharacter(name, isNew):
        if isNew < 1:
            character = Game.assets.CharacterDict[name]
        else:
            character = Character(name="blank", health=0, maxHealth=0,
                                  stamina=0, maxStamina=0, mana=0, maxMana=0,
                                  actionCount=2, maxActionCount=2, weight=0,
                                  dexterity=0, strength=0, instinct=0, intellect=0,
                                  mapIconImgFile="path_to_image", type="character",
                                  actionListNames=[], currentEffectJSONList=[])
        actionJSONS = {an: ac.to_json() for an, ac in Game.assets.actionDict.items()}
        if request.method == 'POST':
            if request.form.get("action") == "save_character_form":
                if 'delete_action' in request.form:
                    del character.actionListNames[request.form['delete_action']]
                elif 'add_action' in request.form:
                    character.actionListNames.append(request.form['add_action'])
                else:
                    character.name = request.form.get('characterName')
                    character.health = int(request.form.get('characterHealth'))
                    character.maxHealth = int(request.form.get('characterHealth'))
                    # FIXME
                    character.stamina = int(request.form.get('characterHealth'))
                    character.maxStamina = int(request.form.get('characterHealth'))
                    character.mana = int(request.form.get('characterHealth'))
                    character.maxMana = int(request.form.get('characterHealth'))
                    character.dexterity = 8
                    character.strength = 8
                    character.instinct = 8
                    character.intellect = 8
                    ### only expect the user to type in the filename, not the relative path
                    character.mapIconImgFile = request.form.get('mapIconImgFile')
                    if isNew == 1:
                        Game.assets.add_character(character)
                    else:
                        Game.assets.update_character_save(character)
                if 'update_character' in request.form:
                    return redirect(url_for('AssetsTop'))
            elif request.form.get("action") == "delete_character_form":
                if isNew == 0:
                    Game.assets.delete_character(name)
                return redirect(url_for('AssetsTop'))
        return render_template('EditCharacter.html', character=character.to_json(), actions=actionJSONS)

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
        Game.assets.reset_curEncounter()
        if (startNew == 1):
            Game.assets.curCampaign = Game.assets.campaignDict[name]
        campaign = Game.assets.curCampaign
        update_other_rooms({'data': 'Entered World Map Screen'})
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

    ### display encounter map, party/enemy stats, party member/Character headshot 
    @app.route('/GameMaster/RunEncounter/Encounter/<name>', methods=['GET', 'POST'])
    def RunEncounter(name):
        # deepcopy and initialize encounter if starting a new one
        if not Game.assets.is_current_encounter():
            Game.assets.curEncounter = copy.deepcopy(Game.assets.encounterDict[name])
            Game.assets.curEncounter.create_map_object_list()
            # update player screens to show encounter screen
            update_other_rooms({'data': 'New Encounter Started'})
        encounter = Game.assets.curEncounter
        processQueue.put(("refreshEncounter", encounter))
        processQueue.put(("gameState", 'encounter'))
        mapObjectJSONs = {mon: mo.to_json() for mon, mo in Game.assets.allMapObjectsDict.items()}
        footingJSONs = {fn: ft.to_json() for fn, ft in Game.assets.footingDict.items()}
        currentCharacter = encounter.get_current_character()
        # get list of modified actions (for the current whose turn it is)
        actionJSONS = {an: ac.modify_from_character(currentCharacter).to_json() for an, ac in Game.assets.actionDict.items()}
        return render_template('RunEncounterGM.html', encounter=encounter.to_json(),
                               mapObjects=mapObjectJSONs, actions=actionJSONS, footings=footingJSONs,
                               mapObjectList=encounter.mapObjectList, character=currentCharacter.to_json())

    ### Action contains modified info 
    @app.route('/GameMaster/CompleteAction/Action/<string:mapObjectID>/<actionListName>', methods=['GET', 'POST'])
    def CompleteAction(mapObjectID, actionListName):
        activityJSONS = {an: ac.to_json() for an, ac in Game.assets.activityDict.items()}
        footingJSONs = {fn: ft.to_json() for fn,ft in Game.assets.footingDict.items()}
        encounter = Game.assets.curEncounter
        character = encounter.get_object_from_object_id(mapObjectID)
        baseAction = Game.assets.actionDict[actionListName]
        turnAction = baseAction.modify_from_character(character)
        mapObjectJSONs = {mon: mo.to_json() for mon, mo in Game.assets.allMapObjectsDict.items()}
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'submit_action_form':
                if turnAction.meets_cost_requirements(character):
                    encounter.resolve_action_costs(mapObjectID, turnAction)
                    activityEntryNames = {key: request.form[key] for key in request.form if key.endswith('_name')}
                    # for each activity in action, resolve pre/post reactions, then resolve effects
                    for entryName in activityEntryNames:
                        match = re.match(r'activity_(\d.*)_name', entryName)
                        submissionNum = match.group(1)
                        dataEntry = request.form.get(f'activity_{submissionNum}_data')
                        nameEntry = request.form.get(entryName)
                        activity = Game.assets.activityDict[nameEntry]
                        encounter.resolve_activity_effects(activity, mapObjectID, dataEntry)
                    encounter.end_character_action(mapObjectID)
                    # refresh all screens to update with new gamestate
                    update_other_rooms({'data': 'Action Complete'})
                current_user_role = session.get('user_role', 'Guest')
                if current_user_role == "GM":
                    return redirect(url_for('RunEncounter', name="current", startNew=0))
                else:
                    return redirect(url_for('RunPlayerCharacter', name=current_user_role))
        return render_template('CompleteAction.html', encounter=encounter.to_json(), mapObjects=mapObjectJSONs,
                                                footings=footingJSONs, action=turnAction.to_json(), character=character.to_json(),
                                                activities=activityJSONS, executorID=mapObjectID, reactionDict=None)
    return app