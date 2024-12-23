# Flask
# from flask import Flask, render_template, url_for, request, redirect
from flask import *
# DeathWish Custom
import Game
from Campaign import Campaign
from Region import Region
from NPC import NPC
from Monster import Monster
from Sentient import Sentient

app = Flask(__name__)

@app.route('/')
def Title():
    return render_template('Title.html')

############################################################################################# Game Master Pages
@app.route('/GameMaster')
def GameMaster():
    return render_template('GameMaster.html', campaigns=Game.assets.campaignList)

@app.route('/GameMaster/EditCampaign/Campaign_<int:index><int:isNew>', methods=['GET', 'POST'])
def EditCampaign(index, isNew):
    if isNew == 0:
        campaign = Game.assets.campaignList[index]
    else:
        campaign = Campaign("blank", 0)
    # create list of serialized regions for browser to use for processing
    regionNames = []
    regionPaths = []
    for region in Game.assets.regionList:
        regionNames.append(region.name)
        regionPaths.append(region.worldMapIconFile)
    regionURLs = [url_for('static', filename=path) for path in regionPaths]
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'save_campaign_form':
            campaignName = request.form.get('campaignName')
            mapDataJson = request.form['map_data']
            mapDataIndexes = json.loads(mapDataJson)
            campaign = Campaign(campaignName, mapDataIndexes)
            if isNew == 1:
                Game.assets.add_campaign(campaign)
            else:
                Game.assets.campaignList[index] = campaign
                Game.assets.update_campaign_save(campaign)
        elif action == 'delete_campaign_form':
            Game.assets.delete_campaign(index)
        return redirect(url_for('GameMaster'))
    return render_template('EditCampaign.html', campaign=campaign, regionNames=regionNames, regionURLs=regionURLs)

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
        region = Region("blank", "path_to_image")
    if request.method == 'POST':
        if request.form.get("action") == "save_region_form":
            regionName = request.form.get('regionName')
            ### only expect the user to type in the filename, not the relative path
            mapIconImgFile = "Assets/Regions/Images/" + request.form.get('mapIconImgFile')
            region = Region(regionName, mapIconImgFile)
            if isNew == 1:
                Game.assets.add_region(region)
            else:
                Game.assets.regionList[index] = region
                Game.assets.update_region_save(region)
        elif request.form.get("action") == "delete_region_form":
            if isNew == 0:
                Game.assets.delete_region(index)
        return redirect(url_for('AssetsTop'))
    return render_template('EditRegion.html', region=region)

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
            mapIconImgFile = "Assets/NPCs/Images/" + request.form.get('mapIconImgFile')
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
    return render_template('EditNPC.html', npc=npc)

### display chosen campaign world map, premise, recent party events, etc.
@app.route('/GameMaster/RunCampaign/Campaign_<int:index>')
def RunCampaign(index):
    campaign = Game.assets.campaignList[index]
    return render_template('RunCampaign.html', campaign=campaign)
