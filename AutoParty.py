from phBot import *
import phBotChat
import QtBind
import sqlite3
import struct
import json 
import os
import time
import shutil
from threading import Timer
import urllib.request


PLUGIN = "AutoParty"
PLUGIN_VERSION = 0.1
MAX_LEN_SCRIPT = 90
DEFAULT_PARTY_SIZE = "8"
DEFAULT_AREA_DELAY = 5
DEFAULT_AREA_OFFSET = 0
DEFAULT_AUTO_AREA = True
DEFAULT_BUY_ITEMS_DELAY = 180
db_path = ''

###Skill Lists###
#Warrior
LIST_WARRIOR_PARTY_BUFFS = ["Pain Quota","Physical Fence","Magical Fence","Protect","Physical Screen","Ultimate Screen","Morale Screen"]
#1H-Sword
LIST_1H_ATTACKS = ["Taunting Target","Howling Shout","Sprint Assault","Slash","Shield Trash","Shield Crush","Double Stab","Cunning Stab","Berserker",
                   "Daring Berserker"]
LIST_1H_BUFFS = ["Vital Increase","Iron Skin","Mana Skin"]
#2H-Sword
LIST_2H_ATTACKS = ["Taunting Target","Howling Shout","Sprint Assault","Bash","Turn Rising","Charge Swing","Triple Swing","Maddening","Dare Devil",]
LIST_2H_BUFFS = ["Vital Increase","Iron Skin","Mana Skin","Warcry"]
#Axe
LIST_AXE_ATTACKS = ["Taunting Target","Howling Shout","Sprint Assault""Down Cross","Double Twist","Sudden Twist","Axis Quiver","Dual Counter",
                    "Deadly Counter","Crisis Rush","Crutial Rush"]
LIST_AXE_BUFFS = ["Vital Increase","Iron Skin","Mana Skin"]
#Wizzard
LIST_WIZ_ATTACKS = ["Fire Bolt","Meteor","Fire Blow","Salamander Blow","Ice Bolt","Frozen Spear","Snow Wind","Blizzard",
                    "Lightning Bolt","Chain Lightning","Charged Wind","Charged Squall","Ground Charge","Ground Rave ","Earth Shock","Earth Quake",]
LIST_WIZ_BUFFS = ["Life Control","Life Turnover","Earth Barrier","Earth Fence"]
#XBow
LIST_XBOW_ATTACKS = []
LIST_XBOW_BUFFS = []
#Dagger
LIST_DAGGER_ATTACKS = []
LIST_DAGGER_BUFFS = []
#Warlock
LIST_WARLOCK_ATTACKS = ["Blood Flower","Death Flower","Bloody Trap","Death Trap","Blaze","Dark Blaze","Toxin ","Toxin Invasion","Decayed","Dark Decayed",
                        "Curse Breath","Dark Breath","Medical Raze","Magical Ravage","Combat Raze","Combat Ravage","Courage Raze","Courage Ravage",
                        "Vampire Touch","Vampire Kiss"]
LIST_WARLOCK_BUFFS = ["Mirage","Phantasma","Reflect","Advanced Reflect"]
#Bard
LIST_BARD_ATTACKS = ["Horror Chord","Weird Chord","Booming Chord","Booming Wave",]
LIST_BARD_BUFFS_MAIN = ["Moving March","Swing March","Guard Tambour","Noise","Mana Cycle","Mana Orbit"]
LIST_BARD_BUFFS_SECOND = ["Moving March","Swing March","Mana Tambour","Noise","Mana Cycle","Dancing of Magic","Dancing of Wizardry"]
LIST_BARD_PARTY_BUFFS = ["Mana Switch","Mana Cycle"]
#Cleric
LIST_CLERIC_ATTACKS = ["Trial Cross","Justice Cross","Over Healing","Glut Healing"]
LIST_CLERIC_BUFFS = ["Reverse","Grad Reverse","Healing Cycle","Soul Deity",
                     "Healing Orbit","Bless Spell","Recovery Division","Holy Recovery Division","Group Reverse",
                     "Holy Group Reverse","Reverse Oblation","Reverse Immolation","Holy Word","Holy Spell","Body Blessing","Body Deity","Soul Blessing"]
LIST_CLERIC_PARTY_BUFFS = ["Force Blessing","Force Deity","Mental Blessing","Mental Deity","Body Blessing","Body Deity","Soul Blessing","Soul Deity",
                           "Healing Cycle"]
LIST_CLERIC_HEALING_BUFFS = ["Group Recovery","Healing Division","Group Healing","Group Healing Breath","Healing Favor","Holy Group Recovery",
                             "Holy Word","Holy Spell","Body Bles    sing","Body Deity","Soul Blessing"]

LIST_INT_BUFFS = ["Mental Blessing","Mental Deity"]
LIST_STR_BUFFS = ["Force Blessing","Force Deity"]
LIST_PHY_BUFFS = ["Body Blessing","Body Deity"]
LIST_MAG_BUFFS = ["Soul Blessing","Soul Deity"]

LIST_LIMITED_PARTY_BUFFS = ["Mental Blessing","Mental Deity","Force Blessing","Force Deity","Pain Quota","Physical Fence","Magical Fence","Protect"]
LIST_SCRIPT_BUFFS=["Moving March","Swing March","Guard Tambour","Noise","Soul Deity","Recovery Division","Holy Recovery Division"]

### Training Areas ###
LIST_TRAINING_AREA =[{'level':4,'x': -11482.5, 'y': 2688.199951171875, 'z': 19.0, 'region': 27211, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':7,'x': -12271.2001953125, 'y': 2567.10009765625, 'z': -20.0, 'region': 26951, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':10,'x': -12371.0, 'y': 3062.199951171875, 'z': -160.0, 'region': 27462, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':12,'x': -12667.900390625, 'y': 2882.5, 'z': 26.0, 'region': 27461, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':15,'x': -11545.7001953125, 'y': 2168.300048828125, 'z': -31.0, 'region': 26442, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':19,'x': -11800.900390625, 'y': 1509.5999755859375, 'z': 0.0, 'region': 25417, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':23,'x': -8433.900390625, 'y': 1641.0999755859375, 'z': 0.0, 'region': 25691, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':26,'x': -7801.2001953125, 'y': 1998.5, 'z': 182.0, 'region': 26206, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':28,'x': -6909.89990234375, 'y': 1321.5999755859375, 'z': 182.0, 'region': 25187, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':30,'x': -6059.5, 'y': 2505.699951171875, 'z': 180.0, 'region': 26983, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':34,'x': -5224.7001953125, 'y': 2295.89990234375, 'z': 252.0, 'region': 26475, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':38,'x': -3915.10009765625, 'y': 2591.199951171875, 'z': 257.0, 'region': 26994, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':40,'x': -3041.10009765625, 'y': 2623.5, 'z': 504.0, 'region': 26999, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':42,'x': 789.2999877929688, 'y': -90.80000305175781, 'z': -16.0, 'region': 23435, 'path': '', 'radius': 25.0, 'pick_radius': 50.0},
                     {'level':45,'x': 510.3999938964844, 'y': 598.2000122070312, 'z': -11.0, 'region': 24457, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':49,'x': -476.8999938964844, 'y': 113.5, 'z': 711.0, 'region': 23684, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':54,'x': -1087.199951171875, 'y': -66.0999984741211, 'z': 800.0, 'region': 23425, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':57,'x': -1589.800048828125, 'y': -25.699996948242188, 'z': 800.0, 'region': 23422, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':60,'x': -24247.30078125, 'y': -190.3000030517578, 'z': -9.0, 'region': -32767, 'path': '', 'radius': 20.0, 'pick_radius': 50.0},
                     {'level':64,'x': -24159.0, 'y': -198.0, 'z': -8.0, 'region': -32767, 'path': '', 'radius': 20.0, 'pick_radius': 50.0},
                     {'level':66,'x': -24136.599609375, 'y': -172.60000610351562, 'z': 145.0, 'region': -32767, 'path': '', 'radius': 20.0, 'pick_radius': 50.0},
                     {'level':60,'x': 9.0, 'y': 1757.9000244140625, 'z': 23.0, 'region': 25991, 'path': '', 'radius': 20.0, 'pick_radius': 50.0},
                     {'level':67,'x': -305.3999938964844, 'y': 1859.800048828125, 'z': -504.0, 'region': 25989, 'path': '', 'radius': 20.0, 'pick_radius': 50.0},
                     {'level':72,'x': -415.8999938964844, 'y': 1963.199951171875, 'z': -184.0, 'region': 26244, 'path': '', 'radius': 20.0, 'pick_radius': 50.0}]

### Dic Quests Area  ###
DIC_QUEST_AREA = {'Inventory Expansion 1 (Europe)':{'x': -11303.400390625, 'y': 2670.199951171875, 'z': 42.0, 'region': 26956, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                  'Inventory Expansion 2 (Europe)':{'x': -6101.0, 'y': 2533.60009765625, 'z': 180.0, 'region': 26983, 'path': '', 'radius': 50.0, 'pick_radius': 50.0}}

### NPCS ###
LIST_NPC_PROTECTOR = ['Protector Trader Jatomo','Protector Trader Aryoan','Protector Trader Gonishya','Protector Trader Yeolah','Protector Trader Mrs Jang']
LIST_TOWNS = ['Constantinople','Samarkand','Hotan Kingdom','Western China Donwhang','Jangan']

gui = QtBind.init(__name__,PLUGIN)

#globals
config_path =""
char_data = {}
game_data_loaded = False
reading_chat = False
dic_party_roles = {}
char = None
quest = None
buy_items = None
role = ""
enabled = False
is_main_bard = False
solo_mode = False
use_cave = False
auto_quest = False
auto_area = False
buy_npc_items = False
on_quest = False
bool_walk_to_quest = False
bool_walk_to_monster = False
blocker_buy = False
blocker_change_area = False

#Set GUI
x = 10
y = 20

checkEnable = QtBind.createCheckBox(gui,'checkEnable_clicked','Enable Plugin',x,y)
checkQuest = QtBind.createCheckBox(gui,'checkQuest_clicked','Auto Quest',x+110,y)
checkBuy = QtBind.createCheckBox(gui,'checkBuy_clicked','Buy NPC Items',x+220,y)
checkBard = QtBind.createCheckBox(gui,'checkBard_clicked','Main Bard',x,y+30)
checkSolo = QtBind.createCheckBox(gui,'checkSolo_clicked','Solo Mode',x+110,y+30)
checkCave = QtBind.createCheckBox(gui,'checkCave_clicked','Use Cave',x+220,y+30)
checkTrainingArea = QtBind.createCheckBox(gui,'checkTraining_clicked', 'Auto Area',x,y+60)
partySizeText = QtBind.createLabel(gui, 'Party Size', x, y+90)
partySize = QtBind.createCombobox(gui, x+100, y+90, 100, 20)
delayChangeArea = QtBind.createLabel(gui, 'Delay Area (min)', x, y+120)
delayChangeAreaValue = QtBind.createCombobox(gui, x+100, y+120, 100, 20)
offsetChangeArea = QtBind.createLabel(gui, 'Offset Area ', x, y+150)
offsetChangeAreaValue = QtBind.createCombobox(gui, x+100, y+150, 100, 20)
for i in range(1,9):
    QtBind.append(gui,partySize,str(i))
for i in range(0,11):
    QtBind.append(gui,delayChangeAreaValue,str(i))
for i in range(-5,6):
    QtBind.append(gui,offsetChangeAreaValue,str(i))


x += 400

button1 = QtBind.createButton(gui,'save_clicked','Save Settings',x,y)
button2 = QtBind.createButton(gui,'button2_clicked','Button 2',x+100,y)
button3 = QtBind.createButton(gui,'buy_items_clicked','Buy Items',x+200,y)
button4 = QtBind.createButton(gui,'load_clicked','Load Settings',x,y+30)
button5 = QtBind.createButton(gui,'button5_clicked','Button 5',x+100,y+30)
button6 = QtBind.createButton(gui,'button6_clicked','Button 6',x+200,y+30)

label_databse = QtBind.createLabel(gui,'Database path:',x-100,y+60)
path_database = QtBind.createLineEdit(gui,'', x, y+60, 292, 20)

x -= 400

### Visualisation ###
y += 190
gui_trainingarea_text = QtBind.createLabel(gui, 'Current Area: ', x+350, y)
gui_trainingarea_value = QtBind.createLabel(gui, '', x+450, y)
gui_quest_text = QtBind.createLabel(gui, 'Quest: ', x, y)
gui_quest_value = QtBind.createLabel(gui, '', x+60, y)
y += 20
gui_quest_progress_text = QtBind.createLabel(gui, 'Progress: ', x, y)
gui_quest_progress_value = QtBind.createLabel(gui, '', x+60, y)
gui_next_trainingarea_text = QtBind.createLabel(gui, 'Lvl to next Area: ', x+350, y)
gui_next_trainingarea_value = QtBind.createLabel(gui, '', x+450, y)
y += 20
gui_task_text = QtBind.createLabel(gui, 'Task: ', x, y)
gui_task_value = QtBind.createLabel(gui, '', x+60, y)
gui_exp_text = QtBind.createLabel(gui, 'EXP: ', x+350, y)
gui_exp_value = QtBind.createLabel(gui, '', x+450, y)
y += 20
gui_level_text = QtBind.createLabel(gui, 'Level: ', x, y)
gui_level_value = QtBind.createLabel(gui, '', x+60, y)
gui_sp_text = QtBind.createLabel(gui, 'SP: ', x+350, y)
gui_sp_value = QtBind.createLabel(gui, '', x+450, y)



### Button ###
def save_clicked():
    if char:
        save_settings()
        log(f'{PLUGIN}: Settings saved')
    else:
        log(f'{PLUGIN}: Please teleport to load Data first')

def button2_clicked():
    log('Function coming soon')

def buy_items_clicked():
    item = Buy_items()
    item.buy_manual()

def load_clicked():
    global game_data_loaded
    log(f'{PLUGIN}: Loading data')
    load_game_data()
    Timer(2.0,load_last_plugin_settings,()).start()
    game_data_loaded = True

def button5_clicked():
    log('Function coming soon')

def button6_clicked():
        log('Function coming soon')


### Checkbox ###
def checkEnable_clicked(checked):
    global enabled
    if checked:
        enabled = True
        change_plugin_configs(True,'Plugin enabled')        
        log(f'{PLUGIN} has been enabled!') 
    else:
        enabled = False  
        change_plugin_configs(False,'Plugin enabled')       
        log(f'{PLUGIN} has been disabled!')

def checkBard_clicked(checked):
    global is_main_bard,char
    if checked:
        is_main_bard = True
        change_plugin_configs(True,'Main Bard')
        log(f'{PLUGIN}: Char has been set to Main Bard')
        if not char == None:
            char.is_main_bard = True 
    else:
        is_main_bard = False
        change_plugin_configs(False,'Main Bard')
        log(f'{PLUGIN}: Char has been removed as Main Bard')
        if not char == None:
            char.is_main_bard = False

def checkSolo_clicked(checked):
    global solo_mode
    if checked:
        solo_mode = True
        change_plugin_configs(True,'Solo Mode')
        log(f'{PLUGIN}: Solo Mode enabled') 
    else:
        solo_mode = False
        change_plugin_configs(False,'Solo Mode')
        log(f'{PLUGIN}: Solo Mode disabled')

def checkQuest_clicked(checked):
    global auto_quest
    if checked:
        auto_quest = True
        change_plugin_configs(True,'Auto Quest')
        log(f'{PLUGIN}: Auto Quest enabled') 
    else:
        auto_quest = False
        change_plugin_configs(False,'Auto Quest')
        log(f'{PLUGIN}: Auto Quest disabled')

def checkBuy_clicked(checked):
    global buy_npc_items
    if checked:
        buy_npc_items = True
        change_plugin_configs(True,'Buy Items')
        log(f'{PLUGIN}: Buy NPC Items enabled') 
    else:
        buy_npc_items = False
        change_plugin_configs(False,'Buy Items')
        log(f'{PLUGIN}: Buy NPC Items disabled')

def checkCave_clicked(checked):
    global use_cave
    if checked:
        use_cave = True
        change_plugin_configs(True,'Use Caves')
        log(f'{PLUGIN}: Caves enabled') 
    else:
        use_cave = False
        change_plugin_configs(False,'Use Caves')
        log(f'{PLUGIN}: Caves disabled')

def checkTraining_clicked(checked):
    global auto_area
    if checked:
        auto_area = True
        change_plugin_configs(True,'Auto Area')
        log(f'{PLUGIN}: Auto Area enabled') 
    else:
        auto_area = False
        change_plugin_configs(False,'Auto Area')
        log(f'{PLUGIN}: Auto Area disabled')

### Functions ###
def load_game_data():
    global char
    char = Character()

def config_loader():
    reload_profile()

def get_profile_path():
    profile = get_profile()
    if not profile == "":
        path = f"{char.server}_{char.name}.{profile}.json"
    else:
        path= f"{char.server}_{char.name}.json"
    return path

def change_bot_config_settings(*args,**kwargs):
    global config_path
    global char_data
    config_file = get_profile_path()
    if os.path.exists(config_path + config_file):
        if len(kwargs) == 0:
            if len(args) < 3 or len(args) > 5:
                log(f"{PLUGIN}: Wrong amount of arguments used in [change_config_settings]")
            value = args[0]            
            with open(config_path + config_file,"r") as file:
                config_data = json.load(file)
                if len(args) == 3:
                    try:
                        data = config_data[args[1]][args[2]]
                    except:
                        log(f"{PLUGIN}: Can´t read Data. Settings couldn´t be changed!")
                        return
                    if type(data) == list:
                        config_data[args[1]][args[2]].append(value)
                    else:
                        config_data[args[1]][args[2]] = value
                if len(args) == 4:
                    try:
                        data = config_data[args[1]][args[2]][args[3]]
                    except:
                        log(f"{PLUGIN}: Can´t read Data. Settings couldn´t be changed!")
                        return
                    if type(data) == list:
                        config_data[args[1]][args[2]][args[3]].append(value)
                    else:
                        config_data[args[1]][args[2]][args[3]] = value
                if len(args) == 5:
                    try:
                        data = config_data[args[1]][args[2]][args[3]][args[4]]
                    except:
                        log(f"{PLUGIN}: Can´t read Data. Settings couldn´t be changed!")
                        return
                    if type(data) == list:
                        config_data[args[1]][args[2]][args[3]][args[4]].append(value)
                    else:
                        config_data[args[1]][args[2]][args[3]][args[4]] = value
                with open(config_path+config_file,"w") as file:
                    file.write(json.dumps(config_data,indent=4))
                    log(f"{PLUGIN}: Settings successfully changed in [{config_file}]")
                    config_loader()
                    return            
        else:
            with open(config_path + config_file,"r") as file:
                config_data = json.load(file)
                for key, item in kwargs.items():
                    value = item[0]
                    if len(item) == 3:
                        try:
                            data = config_data[item[1]][item[2]]
                        except:
                            log(f"{PLUGIN}: Can´t read Data. Settings couldn´t be changed!")
                            return
                    if type(data) == list:
                        config_data[item[1]][item[2]].append(value)
                    else:
                        config_data[item[1]][item[2]] = value
                    if len(item) == 4:
                        try:
                            data = config_data[item[1]][item[2]][item[3]]
                        except:
                            log(f"{PLUGIN}: Can´t read Data. Settings couldn´t be changed!")
                            return
                        if type(data) == list:
                            config_data[item[1]][item[2]][item[3]].append(value)
                        else:
                            config_data[item[1]][item[2]][item[3]] = value
                    if len(item) == 5:
                        try:
                            data = config_data[item[1]][item[2]][item[3]][item[4]]
                        except:
                            log(f"{PLUGIN}: Can´t read Data. Settings couldn´t be changed!")
                            return
                        if type(data) == list:
                            config_data[item[1]][item[2]][item[3]][item[4]].append(value)
                        else:
                            config_data[item[1]][item[2]][item[3]][item[4]] = value
                with open(config_path+config_file,"w") as file:
                    file.write(json.dumps(config_data,indent=4))
                    log(f"{PLUGIN}: Settings successfully changed in [{config_file}]")
                    config_loader()
                    return
    else:
        log(f"{PLUGIN}: Can´t find cofig file [{config_file}].")

def check_settings():
    mastery = get_mastery()
    prim_mastery = None
    sec_mastery = None

    for id in mastery:
        if mastery[id]['level'] > 0:
            if prim_mastery == None:
                prim_mastery = mastery[id]
                sec_mastery = mastery[id]
                continue
            if prim_mastery['level'] <= mastery[id]['level']:
                sec_mastery = prim_mastery
                prim_mastery = mastery[id]
    l1 = [prim_mastery['name'],'Auto Mastery','Mastery']
    l2 = [sec_mastery['name'],'Auto Mastery','Mastery']
    change_bot_config_settings(arg1 = l1,arg2 = l2)

def get_masterys():
    mastery = get_mastery()
    prim_mastery = None
    sec_mastery = None
    prim_id = 0
    sec_id = 0
    for id in mastery:
        if mastery[id]['level'] > 0:
            if prim_mastery == None:
                prim_mastery = mastery[id]
                prim_id = id
                sec_mastery = mastery[id]
                sec_id = id
                continue
            if prim_mastery['level'] <= mastery[id]['level']:
                sec_mastery = prim_mastery
                sec_id = prim_id
                prim_mastery = mastery[id]
                prim_id = id
            else:
                sec_mastery = mastery[id]
                sec_id = id
    return prim_mastery,sec_mastery,prim_id,sec_id

def update_skills():
    global role
    if enabled:
        is_buffer = False    
        if role == "":
            data = load_settings_from_json()
            if not data.get('role', "") == "":
                role = data['role']
            else:
                save_settings()
        if role == 'Tank' or role == 'Bard' or role == 'Healer':
            is_buffer = True     
        skills = get_skills()
        config_file = get_profile_path()
        mastery_id_1 = char.first_id
        skill_is_empty = True
        buff_is_empty = True
        party_buff_is_empty = True
        new_skill_added = False   
        new_buff_added = False   
        new_party_buff_added = False   
        with open(char.bot_config_path + config_file,"r") as file:
            config_data = json.load(file)
            curSkills = config_data['Skills']['sNormal']
            curBuffs = config_data['Skills']['bNormal']
            curPartyBuffs = config_data['Skills']['Party Buffs']
            try:
                data_skills = config_data['Skills']['sNormal']
                data_buffs = config_data['Skills']['bNormal']
            except:
                log(f"{PLUGIN}: Can´t read Data. Attack-Skills couldn´t be changed!")
            if type(data_skills) == list:
                skill_is_empty = False
            if type(data_buffs) == list:
                buff_is_empty = False
            for item in skills:
                if skills[item]['mastery'] == mastery_id_1:
                    if skills[item]['name'] in char.attack_list and not skills[item]['name'] in curSkills:
                        if not skill_is_empty:                        
                            config_data['Skills']['sNormal'].append(skills[item]['name'])
                            new_skill_added = True
                        else:
                            config_data['Skills']['sNormal'] = skills[item]['name']
                            skill_is_empty = False
                            new_skill_added = True
                    elif skills[item]['name'] in char.buff_list and not skills[item]['name'] in curBuffs:
                        if not buff_is_empty:                        
                            config_data['Skills']['bNormal'].append(skills[item]['name'])                            
                            new_buff_added = True
                            if skills[item]['name'] in LIST_CLERIC_HEALING_BUFFS:
                                config_data['Skills']['bScript'].append(skills[item]['name'])
                        else:
                            config_data['Skills']['bNormal'] = skills[item]['name']
                            buff_is_empty = False
                            new_buff_added = True
                            if skills[item]['name'] in LIST_CLERIC_HEALING_BUFFS:
                                config_data['Skills']['bScript'] = skills[item]['name'] 
                    elif skills[item]['name'] in LIST_CLERIC_HEALING_BUFFS and role == 'Healer':
                        if not buff_is_empty:                        
                            config_data['Skills']['Healing'].append(skills[item]['name'])
                            new_buff_added = True
                        else:
                            config_data['Skills']['Healing'] = skills[item]['name']
                            buff_is_empty = False
                            new_buff_added = True           
                    elif skills[item]['name'] in char.party_buff_list and is_buffer:
                        buff_name = skills[item]['name']
                        if buff_name in LIST_INT_BUFFS:
                            buff_name = "Int"
                        elif buff_name in LIST_STR_BUFFS:   
                            buff_name = "Str"
                        elif buff_name in LIST_PHY_BUFFS:   
                            buff_name = "Physical Buff"          
                        elif buff_name in LIST_MAG_BUFFS:   
                            buff_name = "Magical Buff"          
                        get_roles_from_chat()
                        time.sleep(1.0)                    
                        for name,job in dic_party_roles.items():
                            if (role == "Tank" or role == "Healer" or role == "Bard") and not name in config_data['Skills']['Party Buffs'][buff_name]:
                                if job == "Attacker":
                                    if role == 'Bard' and not char.is_main_bard:
                                        continue
                                    if role == "Tank":
                                        if len(config_data['Skills']['Party Buffs'][buff_name]) >= 2:
                                            continue
                                        elif buff_name == 'Pain Quota':
                                            if name in config_data['Skills']['Party Buffs']['Physical Fence'] or name in config_data['Skills']['Party Buffs']['Magical Fence']:
                                                continue
                                        elif buff_name == 'Protect':
                                            if name in config_data['Skills']['Party Buffs']['Physical Fence'] or name in config_data['Skills']['Party Buffs']['Magical Fence']:
                                                continue                                            
                                        elif buff_name == 'Physical Fence':
                                            if name in config_data['Skills']['Party Buffs']['Pain Quota'] or name in config_data['Skills']['Party Buffs']['Protect']:
                                                continue  
                                        elif buff_name == 'Magical Fence':
                                            if name in config_data['Skills']['Party Buffs']['Pain Quota'] or name in config_data['Skills']['Party Buffs']['Protect']:
                                                continue  
                                    config_data['Skills']['Party Buffs'][buff_name].append(name)
                                    new_party_buff_added = True
                                elif not skills[item]['name'] in LIST_LIMITED_PARTY_BUFFS:   
                                    if role == 'Bard' and char.is_main_bard:    
                                        continue                             
                                    config_data['Skills']['Party Buffs'][buff_name].append(name)
                                    new_party_buff_added = True
                                
                                    
                                    
            if new_skill_added or new_buff_added or new_party_buff_added:
                with open(char.bot_config_path + config_file,"w") as file:
                    file.write(json.dumps(config_data,indent=4))
                    log(f"{PLUGIN}: Attacks successfully changed in [{config_file}]") if new_skill_added else log(f"{PLUGIN}: Buffs successfully changed in [{config_file}]")
                    config_loader()
                    return 
            return

def create_config_file():
    default_config_path = char.folder_path + "default.json"
    if game_data_loaded:
        if not os.path.exists(char.char_config_path):
            if not os.path.exists(char.folder_path):
                os.makedirs(char.folder_path)
            if os.path.exists(default_config_path):
                try:
                    shutil.copyfile(default_config_path,char.char_config_path)
                    log(f"{PLUGIN}: Created a new config file for [{char.name}]!")
                except:
                    log(f"{PLUGIN}: There was an error while creating a config file for [{char.name}].")
            else:
                log(f"{PLUGIN}: No default.json found. Creating a new default file!")
                data={
                    "Name": "",
                    "Mastery": {
                        "First Mastery": "",
                        "First ID": 0,
                        "Second Mastery": "",
                        "Second ID": 0
                    },
                    "Skills": {
                        "Weapon": "",
                        "Attack List": [],
                        "Buff List": [],
                        "Party Buff List": ""
                    },
                    "Role": "",
                    "Plugin enabled": False,
                    "Main Bard": False, 
                    "Solo Mode" : False,
                    "Auto Quest" : False,
                    "Party Size": "8",
                    "Use Caves": False,
                    "Delay Area": "5",
                    "Offset Area": "0",
                    "Auto Area": False,
                    "DB Path": ""             
                }
                with open(char.char_config_path,'w',encoding='utf-8') as file:
                    json.dump(data,file,indent=4,ensure_ascii=False)
                Timer(2.0,save_settings,()).start()
        else:
            log(f"{PLUGIN}: Config file for [{char.name}] already exists.")

def change_plugin_configs(*args):
    char.get_data()
    char_config_path = char.char_config_path
    if os.path.exists(char_config_path):
        with open(char_config_path,'r') as f:
            config_data = json.load(f)
            if len(args) == 2:
                value = args[0]
                try:
                    config_data[args[1]] = value
                    with open(char_config_path,'w') as f:
                        json.dump(config_data,f,indent=4)
                    log(f"{PLUGIN}: Configs have successfully been changed")
                except:
                    log(f"{PLUGIN}: Can´t read Data. An Error occured while changing the config file!")
            elif len(args) == 3:
                value = args[0]
                try:
                    config_data[args[1]][args[2]] = value
                    with open(char_config_path,'w') as f:
                        json.dump(config_data,f,indent=4)
                    log(f"{PLUGIN}: Configs have successfully been changed")
                except:
                    log(f"{PLUGIN}: Can´t read Data. An Error occured while changing the config file!")
            else:
                log(f"{PLUGIN}: change_plugin_configs was called with wrong amount of arguments")                            

def save_settings():
    char.get_data()
    folder_path = char.folder_path
    char_config_path = char.char_config_path
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    if os.path.exists(char_config_path):
        with open(char_config_path,'r') as f:
            config_data = json.load(f)
            try:
                config_data['Name'] = char.name
                config_data['Mastery']['First Mastery'] = char.first_mastery_name
                config_data['Mastery']['First ID'] = char.first_id 
                config_data['Mastery']['Second Mastery'] = char.second_mastery_name
                config_data['Mastery']['Second ID'] = char.second_id  
                config_data['Skills']['Weapon'] = char.weapon              
                config_data['Skills']['Attack List'] = char.attack_list              
                config_data['Skills']['Buff List'] = char.buff_list              
                config_data['Skills']['Party Buff List'] = char.party_buff_list              
                config_data['Role'] = char.role              
                config_data['Main Bard'] = is_main_bard
                config_data['Plugin enabled'] = enabled
                config_data['Party Size'] = QtBind.text(gui, partySize)   
                config_data['Buy Items'] = buy_npc_items
                config_data['Use Caves'] = use_cave
                config_data['Delay Area'] = QtBind.text(gui, delayChangeAreaValue) 
                config_data['Auto Area'] = auto_area
                config_data['DB Path'] = QtBind.text(gui,path_database)   
                config_data['Offset Area'] = QtBind.text(gui, offsetChangeAreaValue)             
                with open(char_config_path,'w') as f:
                    json.dump(config_data,f,indent=4)
            except:
                log(f"{PLUGIN}: Can´t read Data. An Error occured while saving the config file!")

def load_settings_from_json():
    if game_data_loaded:
        if os.path.exists(char.char_config_path):
            with open(char.char_config_path,'r') as file:
                config_data = json.load(file)
                try:
                    data = {}
                    data['name'] = config_data['Name']
                    data['mastery'] = {"first mastery":config_data["Mastery"]["First Mastery"],
                                       "first id":config_data["Mastery"]["First ID"],
                                       "second mastery":config_data["Mastery"]["Second Mastery"],
                                       "second id":config_data["Mastery"]["Second ID"],
                                       }
                    data['skills'] = {"weapon":config_data["Skills"]["Weapon"],
                                      "attack list":config_data["Skills"]["Attack List"],
                                      "buff list":config_data["Skills"]["Buff List"],
                                      "party buff list":config_data["Skills"]["Party Buff List"],
                                      }
                    data['role'] = config_data['Role']
                    data['main bard'] = config_data['Main Bard']
                    data['plugin enabled'] = config_data['Plugin enabled']
                    data['solo mode'] = config_data['Solo Mode']
                    data['auto quest'] = config_data['Auto Quest']
                    data['buy items'] = config_data['Buy Items']
                    data['party size'] = config_data['Party Size']
                    data['delay area'] = config_data['Delay Area']
                    data['offset area'] = config_data['Offset Area']
                    data['auto area'] = config_data['Auto Area']
                    data['db path'] = config_data['DB Path']
                except:
                    log(f"{PLUGIN}: Can´t read Data. An Error occured while reading the config file!")
    return data

def get_roles_from_chat():
    global reading_chat
    reading_chat = True
    phBotChat.Party(f"{PLUGIN}: Get Role")

def load_last_plugin_settings():
    global enabled, is_main_bard, solo_mode, auto_quest,char,buy_npc_items,auto_area,db_path
    data = load_settings_from_json()
    if data['plugin enabled']:
        enabled = True
        QtBind.setChecked(gui,checkEnable,True)
    else:
        enabled = False
    if data['main bard']:
        is_main_bard = True
        QtBind.setChecked(gui,checkBard,True)
        if not char == None:
            char.is_main_bard = True
    else:
        is_main_bard = False
        if not char == None:
            char.is_main_bard = False
    if data['solo mode']:
        solo_mode = True
        QtBind.setChecked(gui,checkSolo,True)
    else:
        solo_mode = False
    if data['auto quest']:
        auto_quest = True
        QtBind.setChecked(gui,checkQuest,True)
    else:
        auto_quest = False
    if data['buy items']:
        buy_npc_items = True
        QtBind.setChecked(gui,checkBuy,True)
    else:
        buy_npc_items = False
    if data['party size']:
        QtBind.setText(gui,partySize,data['party size'])
    else:
       QtBind.setText(gui,partySize,DEFAULT_PARTY_SIZE)
    if data['delay area']:
        QtBind.setText(gui,delayChangeAreaValue,data['delay area'])
    else:
       QtBind.setText(gui,delayChangeAreaValue,DEFAULT_AREA_DELAY)
    if data['auto area']:
        auto_area = True
        QtBind.setChecked(gui,checkTrainingArea,True)
    else:
       auto_area = False
    if data['db path']:
        db_path = data['db path']
        QtBind.setText(gui,path_database,data['db path'])
    else:
       QtBind.setText(gui,path_database,'')
    if data['offset area']:
        QtBind.setText(gui,offsetChangeAreaValue,data['offset area'])
    else:
       QtBind.setText(gui,offsetChangeAreaValue,DEFAULT_AREA_OFFSET)

    

class Character(): 

    def __init__(self):
        self.data = get_character_data()
        self.name = self.data['name']
        self.server = self.data['server']
        self.bot_config_path = get_config_dir()
        self.folder_path = self.bot_config_path + f"\{PLUGIN}\\"  
        self.char_config_path = self.folder_path + f"{self.server}_{self.name}.json"
        self.is_main_bard = is_main_bard
        self.__load_data()

    def get_data(self):
        self.__load_data()

    def get_data_from_json(self):
        self.__load_data_from_json()

    def __load_data(self):
        self.first_mastery,self.second_mastery,self.first_id,self.second_id = get_masterys()
        if self.first_mastery:
            self.first_mastery_name = self.first_mastery['name']
        else:
            self.first_mastery_name = ""
        if self.second_mastery:
            self.second_mastery_name = self.second_mastery['name']
        else:
            self.second_mastery_name = ""
        self.role = self.__get_role()

    def __load_data_from_json(self):
        if os.path.exists(config_path + f"\{PLUGIN}\\" + f"{char_data['server']}_{char_data['name']}.json"):
            with open(config_path + f"\{PLUGIN}\\" + f"{char_data['server']}_{char_data['name']}.json","r") as file:
                config_data = json.load(file)
                try:
                    self.name = config_data['Name']
                    self.first_mastery_name = config_data['Mastery']['First Mastery']
                    self.first_id = config_data['Mastery']['First ID'] 
                    self.second_mastery_name = config_data['Mastery']['Second Mastery']
                    self.second_id  = config_data['Mastery']['Second ID'] 
                    self.weapon = config_data['Skills']['Weapon']              
                    self.attack_list = config_data['Skills']['Attack List']              
                    self.buff_list = config_data['Skills']['Buff List']              
                    self.party_buff_list = config_data['Skills']['Party Buff List']              
                    self.role = config_data['Role']  
                except:
                    log(f"{PLUGIN}: Can´t read Data. An Error occured while loading the config file!")

    def get_mastery(self):
        return self.first_mastery,self.second_mastery

    def get_mastery_id(self):
        return self.first_id,self.second_id 
    
    def __get_role(self):
        inventory = get_inventory()
        weapon = inventory['items'][6]['servername']
        self.weapon = weapon
        self.buff_list = ""
        self.attack_list = ""
        self.party_buff_list = ""
        if self.first_mastery_name == "Cleric":
            self.attack_list = LIST_CLERIC_ATTACKS
            self.buff_list = LIST_CLERIC_BUFFS
            self.party_buff_list = LIST_CLERIC_PARTY_BUFFS
            return "Healer"
        elif self.first_mastery_name == "Bard":
            self.attack_list = LIST_BARD_ATTACKS
            if is_main_bard:
                self.buff_list = LIST_BARD_BUFFS_MAIN
            else:
                self.buff_list = LIST_BARD_BUFFS_SECOND
            self.party_buff_list = LIST_BARD_PARTY_BUFFS
            return "Bard"
        elif self.first_mastery_name == "Warrior":
            if "TSWORD" in weapon:
                self.attack_list = LIST_2H_ATTACKS
                self.buff_list = LIST_2H_BUFFS            
            elif "SWORD" in weapon:
                self.attack_list = LIST_1H_ATTACKS
                self.buff_list = LIST_1H_BUFFS
            elif "AXE" in weapon:
                self.attack_list = LIST_AXE_ATTACKS
                self.buff_list = LIST_AXE_BUFFS                 
            self.party_buff_list = LIST_WARRIOR_PARTY_BUFFS
            return "Tank"
        elif self.first_mastery_name == "Wizard":
            self.attack_list = LIST_WIZ_ATTACKS
            self.buff_list = LIST_WIZ_BUFFS
            return "Attacker"
        elif self.first_mastery_name == "Rouge":
            if "XBOW" in weapon:
                self.attack_list = LIST_XBOW_ATTACKS
                self.buff_list = LIST_XBOW_BUFFS
            elif "DAGGER" in weapon:
                self.attack_list = LIST_DAGGER_ATTACKS
                self.buff_list = LIST_DAGGER_BUFFS
            return "Attacker"
        elif self.first_mastery_name == "Warlock":
            self.attack_list = LIST_WARLOCK_ATTACKS
            self.buff_list = LIST_WARLOCK_BUFFS
            return "Attacker"
        return ""

# Misc #
def set_bools_to_false():
    global bool_walk_to_quest,bool_walk_to_monster
    bool_walk_to_monster = False
    bool_walk_to_quest = False

def get_current_task():
    text = ''
    task = None
    if on_quest:
        text = 'On Quest: '
    if bool_walk_to_monster:
        text += 'Walking to Monster'
        task = 'walk_to_monster'
    elif bool_walk_to_quest:
        text += 'Walking to Quest NPC'
        task = 'walk_to_quest'
    return task,text

def is_in_town():
    region = update_states()[0]
    if region in LIST_TOWNS:
        return True
    return False

def update_states():
    cur_char_data = get_character_data()
    cur_region = readDB('zones',0,cur_char_data['region'])[2]
    cur_x = round(cur_char_data['x'],2)
    cur_y = round(cur_char_data['y'],2)
    cur_task,cur_task_text = get_current_task()
    if quest:
        QtBind.setText(gui,gui_quest_value,quest.name)
        current_quests = get_quests()
        for item in current_quests:
            if current_quests[item]['name'] == quest.name:
                QtBind.setText(gui,gui_quest_progress_value,str(current_quests[item]['objectives'][0]['notice']))
                break
    return cur_region,cur_x,cur_y,cur_task
    
def get_current_weapon():
    inventory = get_inventory()
    weapon = inventory['items'][6]['servername']
    return weapon

def get_updated_weapon_string(item,degree):
    item_split = item.split('_')
    weapon_string = item_split[0]+'_'+item_split[1]+'_'+item_split[2]+'_'+degree+'_BASIC'
    return weapon_string

def get_degree_from_quest(numb):
    if numb == '0':
        return '01'
    elif numb == '2':
        return '02'
    elif numb == '4':
        return '03'
    elif numb == '6':
        return '04'
    elif numb == '8':
        return '05'
    elif numb == '10':
        return '06'
    else:
        return ''

def get_current_auto_area():
    current_area = get_training_area()
    current_x = float(current_area['x'])
    current_y = float(current_area['y'])
    for area in LIST_TRAINING_AREA:
        if  current_x-5 <= float(area['x']) <= current_x+5 and current_y-5 <= float(area['y']) <= current_y+5:
            return area

def upate_visual():
    c_data = get_character_data()
    level = c_data['level']
    exp = c_data['current_exp']/c_data['max_exp']
    sp = c_data['sp']
    QtBind.setText(gui,gui_level_value,str(level))
    QtBind.setText(gui,gui_exp_value,str(round(exp*100,2))+'%')
    QtBind.setText(gui,gui_sp_value,str(sp))
    
### Auto-Training ###
# Automaticly changes the training Area #
def change_area():
    global blocker_change_area   
    upate_visual()
    if auto_area: 
        if blocker_change_area:
            return
        if not quest == None:
            if quest.is_doing_quest:
                return
        party = get_party()
        if not len(party) >= int(QtBind.text(gui,partySize)):
            return
        lvl = check_party_level()
        if solo_mode:
            c_data = get_character_data()
            lvl = c_data['level']
        lvl += int(QtBind.text(gui,offsetChangeAreaValue))
        current_area = get_training_area()
        current_x = float(current_area['x'])
        current_y = float(current_area['y'])
        if lvl > 0 and enabled:
            update_area_visual(lvl)
            for area in LIST_TRAINING_AREA:
                if area['level'] > lvl:
                    if  current_x-5 <= float(area['x']) <= current_x+5 and current_y-5 <= float(area['y']) <= current_y+5 :
                        break
                    if area['region'] < 0:
                        if not use_cave:
                            continue  
                    blocker_change_area = True       
                    stop_bot()
                    set_training_script('')
                    Timer(0.5,set_training_position,[area['region'], area['x'], area['y'],area['z']]).start()
                    Timer(1.0,start_bot,()).start()
                    Timer(0.1+int(QtBind.text(gui,delayChangeAreaValue)*60),reset_blocker_change_area,()).start()
                    log(f"{PLUGIN}: Changing Training Area to Monsters with level: {area['level']}")
                    Timer(1.0,update_area_visual,[lvl]).start()
                    break
        return
    return

def check_party_level():
    c_data = get_character_data()
    lvl = c_data['level']
    lowest_lvl = lvl
    party = get_party()
    if party:
        for key in party:
            if party[key]['name'] == c_data['name']:
                continue
            elif party[key]['level'] > 0 and party[key]['level'] < lowest_lvl:
                lowest_lvl = party[key]['level']
        return lowest_lvl
    return 0

def reset_blocker_change_area():
    global blocker_change_area
    blocker_change_area = False

def update_area_visual(level):
    cur_area_level = get_current_auto_area()['level']
    next_area_level = cur_area_level - level
    QtBind.setText(gui,gui_trainingarea_value,str(cur_area_level))
    QtBind.setText(gui,gui_next_trainingarea_value,str(next_area_level))

### Auto-Quest ###
# Automaticly finishes Inventory-Expansion #
# Walking #
def get_map_coordinates(region_id,pos_x,pos_y):
    if region_id > 0:
        X = ((region_id & 0xFF) - 135) * 192 + pos_x / 10 
        Y = ((region_id >> 8) - 92) * 192 + pos_y / 10
    else:
        X = ((region_id & 255) - 128) * 192 + pos_x / 10
        Y = (((region_id >> 8) & 0xFF) - 128) * 192 + pos_y / 10
    return X,Y

def readDB(table,col,item):
    if db_path == '':
        db_path = QtBind.text(gui,path_database)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = f"SELECT * FROM {table}"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        if row[col] == item:
            return row
 
def get_npc_position_from_db(quest):
    if "Beginner's Assistant" in quest:
        quest = "Lv. 5 Beginner's Assistant"
    npc_start = readDB('quest',2,quest)[3].split(',')
    if len(npc_start) > 1:
        reg = readDB('zones',0,get_position()['region'])[1].upper()
        for item in npc_start:
            if reg in item:
                npc_start = item
    else:
        npc_start = npc_start[0]
    npc_id = readDB('monsters',1,npc_start)[0]
    npc_name = readDB('monsters',1,npc_start)[2]
    npc_pos = readDB('npcpos',0,npc_id)
    npc_region = npc_pos[1]
    npc_x = npc_pos[2]
    npc_y = npc_pos[4]
    return npc_region,npc_x,npc_y,npc_start,npc_name

def generate_script_to_destination(region,x,y):
    list_script = generate_script(region, x, y, 0)
    if list_script:
        walk_scr = ""
        for item in list_script:
            walk_scr += item + '\n'
        return walk_scr
    else:
        log(f'{PLUGIN}: Error at "get_script_to_npc". Could not generate script') 

def walk_to_quest(quest):
    global bool_walk_to_quest
    npc_pos = get_npc_position_from_db(quest)
    if npc_pos:
        x,y = get_map_coordinates(npc_pos[0],npc_pos[1],npc_pos[2])
        if x:
            script = generate_script_to_destination(npc_pos[0],x,y)
            if script:
                start_script(script)
                set_bools_to_false()
                bool_walk_to_quest = True
            else:
                log(f'{PLUGIN}: Error at "walk_to_quest". Could not generate script')
                return
        else:
            log(f'{PLUGIN}: Error at "walk_to_quest". Could not get map_coordinates')
            return
    else:
        log(f'{PLUGIN}: Error at "walk_to_quest". Could not get npc_pos')
        return

def walk_to_monster(quest):
    global bool_walk_to_monster
    area = DIC_QUEST_AREA[quest]
    if area:
        try:
            script = generate_script_to_destination(area['region'],area['x'],area['y'])
            start_script(script)
            set_bools_to_false()
            bool_walk_to_monster = True
            return
        except:
            log(f'{PLUGIN}: Error at "walk_to_monster". Could not generate script')
    else:
        log(f'{PLUGIN}: Error at "walk_to_monster". Could not find an Area for {quest}')
        return

# Execute Quest #   
def do_auto_quest():
    global quest
    q = check_available_quest()
    if q:
        quest = Quest(q)
        quest.do_quest()

def get_current_inventory_size():
    c_inventory = get_inventory() 
    return c_inventory['size']

def check_available_quest():
    c_data = get_character_data()
    level = c_data['level']
    cur_inv_size = get_current_inventory_size()
    current_quests = get_quests()
    for item in current_quests:
        if "Beginner's Assistant" in current_quests[item]['name']:
            return str(current_quests[item]['name'])
    if cur_inv_size == 45 and level >= 5:
        return 'Inventory Expansion 1 (Europe)'
    if cur_inv_size == 55 and level >= 32:
        return 'Inventory Expansion 2 (Europe)'
    return

class Quest():
    def __init__(self,quest):
        self.name = quest
        self.server_name = ""
        self.npc_region,self.npc_x,self.npc_y,self.npc_start_name,self.npc_ingame_name = get_npc_position_from_db(quest)
        self.npc_game_x,self.npc_game_y = get_map_coordinates(self.npc_region,self.npc_x,self.npc_y)
        self.is_doing_quest = False
        self.is_walking_to_npc = False
        self.is_walking_to_monster = False
        self.is_talking_to_npc = False
        self.is_attacking_monsters = False
        self.has_quest_taken = False
        self.quest_completed = False
        self.is_teleporting_for_quest = False
        self.cur_char_position = (0,0)
        self.char_training_area = None
        self.char_quest_area = None
        self.quest_data = None
        if "Beginner's Assistant" in self.name:
            self.is_beginner_quest = True
        else:
            self.is_beginner_quest = False
        self.has_item_reward = False
        self.current_character_quests = get_quests()
        self.quest_list = []       
    
    def walk_to_npc(self):
        if not self.is_walking_to_npc:
            self.script_to_npc = generate_script_to_destination(self.npc_region,self.npc_game_x,self.npc_game_y)
            len_script = self.script_to_npc.split('\n')
            if len(len_script) > MAX_LEN_SCRIPT:
                stop_bot()
                use_return_scroll()
                self.is_teleporting_for_quest = True
                return
            self.script_last_x,self.script_last_y = (self.script_to_npc.strip().split("\n"))[-1].split(",")[1:3]
            if self.script_to_npc:
                self.is_walking_to_npc = True
                start_script(self.script_to_npc)
                if self.quest_completed:
                    log(f'{PLUGIN}: {self.name} completed. Walking to NPC')
                else:
                    log(f'{PLUGIN}: Walking to NPC for {self.name}')
        elif self.is_walking_to_npc:
            if int(self.script_last_x)-1 <= int(self.cur_char_position[0]) <= int(self.script_last_x)+1:
                if int(self.script_last_y)-1 <= int(self.cur_char_position[1]) <= int(self.script_last_y)+1:
                    log(f'{PLUGIN}: Script finished. Talking to NPC')
                    self.is_walking_to_npc = False
                    self.enter_npc()
    
    def walk_to_monster(self):
        if not self.is_walking_to_monster:
            self.script_to_monster = generate_script_to_destination(DIC_QUEST_AREA[self.name]['region'],DIC_QUEST_AREA[self.name]['x'],DIC_QUEST_AREA[self.name]['y'])
            len_script = self.script_to_monster.split('\n')
            if len(len_script) > MAX_LEN_SCRIPT:
                stop_bot()
                use_return_scroll()
                self.is_teleporting_for_quest = True
                return
            if "Dismounting pet" in self.script_to_monster:
                self.script_to_monster = self.script_to_monster.replace('Dismounting pet','')
            self.script_last_x,self.script_last_y = (self.script_to_monster.strip().split("\n"))[-1].split(",")[1:3]
            if self.script_to_monster:
                self.is_walking_to_monster = True
                start_script(self.script_to_monster)
        elif self.is_walking_to_monster:
            if int(self.script_last_x)-3 <= int(self.cur_char_position[0]) <= int(self.script_last_x)+3:
                if int(self.script_last_y)-3 <= int(self.cur_char_position[1]) <= int(self.script_last_y)+3:
                    log(f'{PLUGIN}: Script finished. Starting Quest')
                    self.is_walking_to_monster = False
                    self.attack_monsters()

    def attack_monsters(self):
        self.is_attacking_monsters = True
        self.char_training_area = get_training_area()
        set_training_script('')
        Timer(0.5,set_training_position,[0, int(self.cur_char_position[0]), int(self.cur_char_position[1]), 0.0]).start()
        Timer(1.0,start_bot,()).start()
        QtBind.setText(gui,gui_task_value,'Attacking Monsters')

    def self_call(self):
        log('called')
        Timer(1.0,self.self_call,()).start()

    def enter_npc(self):
        self.is_talking_to_npc = True
        i = 0
        npc = get_npcs()
        for id in npc:
            if npc[id]['servername'] == self.npc_start_name:
                break
        QtBind.setText(gui,gui_task_value,f'Entering NPC {self.npc_ingame_name}')
        opcode =[0x7045,0x7046]
        data = [struct.pack('<I',id),struct.pack('<I',id) + struct.pack('1B',0x02)]
        inject_joymax(opcode[i],data[i],False)
        i +=1
        Timer(1.0,inject_joymax,[opcode[i],data[i],False]).start()
        Timer(2.0,self.get_questlist_from_npc,()).start()

    def get_questlist_from_npc(self):
        quests = {}
        index = 0
        rewards = self.quest_data[index]
        if rewards == 4:
            index += 1
            questLength = struct.unpack_from('<H',self.quest_data,index)[0]
            index += 2
            quests['name'] = struct.unpack_from('<'+ str(questLength) +'s',self.quest_data,index)[0].decode('cp1252')
            index += questLength
            nQuests = self.quest_data[index]
            index += 1
            for i in range (nQuests):       
                questLength = struct.unpack_from('<H',self.quest_data,index)[0]
                index += 2
                quests['name'] = struct.unpack_from('<'+ str(questLength) +'s',self.quest_data,index)[0].decode('cp1252')
                index += questLength
                try:
                    name = readDB('quest',1,quests['name'][3:])   
                    self.quest_list.append(str(name[2]))       
                    log(PLUGIN + ': ' +str(i+1)+'. Quest: '+str(name[2]))
                except:
                    log(f'{PLUGIN}: Error at "get_questlist_from_npc". Could not parse Quests from NPC')
                    return
        self.get_quest_reward()

    def get_quest_reward(self):
        count = 5
        for item in self.quest_list:            
            if 'Inventory' in item:
                QtBind.setText(gui,gui_task_value,f'Turning in {self.name}')
                opcode = 0x30D4
                Timer(1.0,inject_joymax,[opcode,struct.pack('B',count),False]).start()
                Timer(2.0,inject_joymax,[opcode,struct.pack('B',count),False]).start()
                Timer(3.0,inject_joymax,[opcode,struct.pack('B',count),False]).start()
                if self.quest_completed:
                    self.set_to_default()
                    Timer(4.0,start_bot,()).start()
                    log(f'{PLUGIN}: {self.name} successfully redeemed. Continuing with botting')
                    QtBind.setText(gui,gui_quest_value,'')
                    QtBind.setText(gui,gui_quest_progress_value,'')
                else:
                    Timer(4.0,self.do_quest,()).start()
                break
            elif self.name in item and self.is_beginner_quest:
                QtBind.setText(gui,gui_task_value,f'Turning in {self.name}')
                if int(self.server_name.split('_')[-1]) % 2 == 0:
                    self.has_item_reward = True
                    weapon = get_current_weapon()
                    degree = get_degree_from_quest(self.server_name.split('_')[-1])
                    if not weapon == '' and not degree == '':
                        weapon = get_updated_weapon_string(weapon,degree)
                        try:
                            startByte = readDB('quest',1,self.server_name)[0]
                            startByte = struct.pack('<I',startByte)            
                            weaponID = get_item_string(weapon)               
                            p = startByte
                            hex_str = "01"
                            byte_str = bytes.fromhex(hex_str)
                            p += byte_str
                            p += struct.pack('<I',weaponID['model'])
                            Timer(1.0,inject_joymax,[0x30D4,struct.pack('B',count),False]).start()
                            Timer(2.0,inject_joymax,[0x7515,p,False]).start()
                            Timer(3.0,self.set_to_default,()).start()
                            Timer(4.0,start_bot,()).start()
                            Timer(3.5,log,[f'{PLUGIN}: {self.name} successfully redeemed. Continuing with botting']).start()
                        except:
                            log(f'{PLUGIN}: Couldn´t load Weapon from Config') 
                else:
                    opcode = 0x30D4
                    Timer(1.0,inject_joymax,[opcode,struct.pack('B',count),False]).start()
                    Timer(2.0,inject_joymax,[opcode,struct.pack('B',count),False]).start()
                    self.set_to_default()
                    Timer(4.0,start_bot,()).start()
                    log(f'{PLUGIN}: {self.name} successfully redeemed. Continuing with botting')
                    QtBind.setText(gui,gui_quest_value,'')
                    QtBind.setText(gui,gui_quest_progress_value,'')
            else:
                count += 1
    
    def check_quest_taken(self):
        self.current_character_quests = get_quests()
        for item in self.current_character_quests:
            if self.current_character_quests[item]['name'] == self.name:
                self.server_name = self.current_character_quests[item]['servername']
                if self.current_character_quests[item]['completed']:
                    self.quest_completed = True
                    if self.is_attacking_monsters:
                        self.is_attacking_monsters = False
                        stop_bot()
                        set_training_script('')
                        Timer(0.5,set_training_position,[self.char_training_area['region'], self.char_training_area['x'], self.char_training_area['y'],self.char_training_area['z']]).start()        
                        self.do_quest()                                                
                return True
        else:
            return False

    def do_quest(self):
        stop_bot()
        log(f'{PLUGIN}: Quest available! Doing {self.name}')
        self.is_doing_quest = True
        if self.check_quest_taken():
            if self.quest_completed:
                QtBind.setText(gui,gui_task_value,f'Walking to NPC {self.npc_ingame_name}')
                self.walk_to_npc()
            else:
                self.has_quest_taken = True
                if self.is_beginner_quest:                
                    self.walk_to_npc()
                    QtBind.setText(gui,gui_task_value,f'Walking to NPC {self.npc_ingame_name}')
                else:
                    log(f'{PLUGIN}: Walking to Monster')
                    QtBind.setText(gui,gui_task_value,'Walking to NPC Monster')
                    self.walk_to_monster()
        else:
            self.walk_to_npc()
            QtBind.setText(gui,gui_task_value,f'Walking to NPC {self.npc_ingame_name}')

    def set_to_default(self):
        self.is_doing_quest = False
        self.is_walking_to_npc = False
        self.is_walking_to_monster = False
        self.is_talking_to_npc = False
        self.is_attacking_monsters = False
        self.has_quest_taken = False
        self.quest_completed = False
        self.is_teleporting_for_quest = False
        self.is_beginner_quest = False
        QtBind.setText(gui,gui_quest_value,'')
        QtBind.setText(gui,gui_quest_progress_value,'')
        QtBind.setText(gui,gui_task_value,'')
        Timer(1.0,del_quest,()).start()

def del_quest():
    global quest
    quest = None

### Auto-Protector ###
# Buy Protector #
class Buy_items():
    def __init__(self):
        self.npc_server_name = ''
        self.max_item_level = self.get_max_item_level()
        self.char_set = self.get_char_protector_data()
        self.tab = self.get_npc_protector_tab()
        self.item_list,self.npc_id = self.get_item_list()
        self.list_items_to_buy = self.get_items_to_buy()      
        self.is_buying_items = False
        self.is_walking_to_npc = False
        self.is_at_npc = False
        self.cur_char_position = (0,0)
        
    def check_if_items_available(self):
        if len(self.list_items_to_buy) > 0:
            return True
        return False

    def get_max_item_level(self):
        all_masterys = get_mastery()
        mastery = ''
        max = 0
        for item in all_masterys:
            if all_masterys[item]['level'] > max:
                mastery = all_masterys[item]
        return mastery['level']

    def get_char_protector_data(self):
        inv = get_inventory()
        list_inventory_items = []
        for x in inv['items']:
            if not x == None:
                list_inventory_items.append(x['servername'])
        self.list_inventory_items = list_inventory_items 
        head = inv['items'][0]
        chest = inv['items'][1]
        shoulder = inv['items'][2]
        hands = inv['items'][3]
        legs = inv['items'][4]
        foot = inv['items'][5]
        earring = inv['items'][9]
        necklace = inv['items'][10]
        ring_1 = inv['items'][11]
        ring_2 = inv['items'][12]
        char_set={'head':head,'chest':chest,'shoulder':shoulder,'hands':hands,'legs':legs,'foot':foot,
                'earring':earring,'necklace':necklace,'ring_1':ring_1,'ring_2':ring_2}
        for x in char_set:
            if char_set[x] == None:
                char_set[x] = {'model': 11623, 'servername': 'ITEM_EU_M_CLOTHES_01_BA_A_DEF', 'name': 'Sagittarius Cotton Robe (Basic)', 'quantity': 1, 'plus': 0, 'durability': 31}
        return char_set

    def get_npc_protector_tab(self):
        dic = self.char_set
        tab = 0
        for item in dic:
            if not dic[item] == None:
                protector = dic[item]
                break
        if '_CLOTHES_' in protector['servername']:
            if '_M_' in protector['servername']:
                tab = 2
            else:
                tab = 5
        if '_LIGHT_' in protector['servername']:
            if '_M_' in protector['servername']:
                tab = 1
            else:
                tab = 4
        if '_HEAVY_' in protector['servername']:
            if '_M_' in protector['servername']:
                tab = 0
            else:
                tab = 3
        return tab

    def get_item_list(self):
        npcs = get_npcs()
        npc_id = 0
        if npcs:
            for x in npcs:
                if npcs[x]['name'] in LIST_NPC_PROTECTOR:
                    npc_id = x
                    self.npc_id = x
                    npc_model = npcs[x]['model']
                    self.npc_server_name = npcs[x]['servername']
                    self.npc_name = npcs[x]['name']
            if npc_id:
                data = self.read_db_comp_table('npcgoods',0,npc_model)
                item_list = []
                for item in data:
                    if item[1] == self.tab:
                        item_list.append(item)
                return item_list,npc_id
            return None,None
        return None,None

    def get_items_to_buy(self):
        data = self.char_set
        max_level = self.max_item_level
        items = self.item_list
        items_to_buy = {}
        if items:
            for x in items:        
                item_data = get_item(x[3])
                try:
                    if int(item_data['level']) <= max_level:
                        if item_data['servername'] in self.list_inventory_items:                            
                            continue
                        if '_CA_' in item_data['servername']:
                            level = get_item(data['head']['model'])['level']
                            if int(item_data['level']) > int(level):
                                try:
                                    if int(items_to_buy['head'][4]) > int(item_data['level']):
                                        continue
                                except:
                                    items_to_buy['head'] = [item_data['servername'],x[1],x[2],item_data['name'],item_data['level']]
                        if '_BA_' in item_data['servername']:
                            level = get_item(data['chest']['model'])['level']
                            if int(item_data['level']) > int(level):
                                try:
                                    if int(items_to_buy['chest'][4]) > int(item_data['level']):
                                        continue
                                except:
                                    items_to_buy['chest'] = [item_data['servername'],x[1],x[2],item_data['name'],item_data['level']]
                        if '_SA_' in item_data['servername']:
                            level = get_item(data['shoulder']['model'])['level']
                            if int(item_data['level']) > int(level):
                                try:
                                    if int(items_to_buy['shoulder'][4]) > int(item_data['level']):
                                        continue
                                except:
                                    items_to_buy['shoulder'] = [item_data['servername'],x[1],x[2],item_data['name'],item_data['level']]
                        if '_AA_' in item_data['servername']:
                            level = get_item(data['hands']['model'])['level']
                            if int(item_data['level']) > int(level):
                                try:
                                    if int(items_to_buy['hands'][4]) > int(item_data['level']):
                                        continue
                                except:
                                    items_to_buy['hands'] = [item_data['servername'],x[1],x[2],item_data['name'],item_data['level']]
                        if '_LA_' in item_data['servername']:
                            level = get_item(data['legs']['model'])['level']
                            if int(item_data['level']) > int(level):
                                try:
                                    if int(items_to_buy['legs'][4]) > int(item_data['level']):
                                        continue
                                except:
                                    items_to_buy['legs'] = [item_data['servername'],x[1],x[2],item_data['name'],item_data['level']]
                        if '_FA_' in item_data['servername']:
                            level = get_item(data['foot']['model'])['level']
                            if int(item_data['level']) > int(level):
                                try:
                                    if int(items_to_buy['foot'][4]) > int(item_data['level']):
                                        continue
                                except:
                                    items_to_buy['foot'] = [item_data['servername'],x[1],x[2],item_data['name'],item_data['level']]
                except:
                    continue
            return items_to_buy
        return []

    def get_npc_pos(self):
        npc_id = readDB('monsters',1,self.npc_server_name)[0]
        npc_pos = readDB('npcpos',0,npc_id)
        npc_region = npc_pos[1]
        npc_x = npc_pos[2]
        npc_y = npc_pos[4]
        return npc_region,npc_x,npc_y

    def walk_to_npc(self):
        if not self.is_walking_to_npc:
            QtBind.setText(gui,gui_task_value,f'Walking to {self.npc_name} to buy items')
            self.npc_region,self.npc_x,self.npc_y = self.get_npc_pos()
            self.npc_game_x,self.npc_game_y = get_map_coordinates(self.npc_region,self.npc_x,self.npc_y)
            self.script_to_npc = generate_script_to_destination(self.npc_region,self.npc_game_x,self.npc_game_y)
            len_script = self.script_to_npc.split('\n')
            if len(len_script) > MAX_LEN_SCRIPT:
                stop_bot()
                use_return_scroll()
                self.is_teleporting_for_quest = True
                return
            self.script_last_x,self.script_last_y = (self.script_to_npc.strip().split("\n"))[-1].split(",")[1:3]
            if self.script_to_npc:
                self.is_walking_to_npc = True
                start_script(self.script_to_npc)
                log(f'{PLUGIN}: Walking to NPC {self.npc_name}')
        elif self.is_walking_to_npc:
            if int(self.script_last_x)-1 <= int(self.cur_char_position[0]) <= int(self.script_last_x)+1:
                if int(self.script_last_y)-1 <= int(self.cur_char_position[1]) <= int(self.script_last_y)+1:
                    log(f'{PLUGIN}: Script finished. Talking to NPC')
                    self.is_walking_to_npc = False
                    self.is_at_npc = True
                    self.enter_npc()

    def buy(self):
        stop_bot()
        log(f'{PLUGIN}: Items available! Buying Items')
        self.is_buying_items = True
        if self.is_at_npc:
            log('1')
        else:
            self.walk_to_npc()
        
    def build_data_bytes(self,tab,slot,npc_id):
        hex_str = "08" #fix
        byte_str = bytes.fromhex(hex_str)
        p = byte_str
        p += struct.pack('<H',tab)[:1]
        p += struct.pack('<H',slot)[:1]
        hex_str = "01"
        byte_str = bytes.fromhex(hex_str)
        p += byte_str
        p2 = struct.pack('<I',npc_id)#npc id  
        p2 = b'\x00' + p2 
        p += p2
        return p

    def buy_manual(self):
        self.is_at_npc = True
        self.enter_npc()

    def enter_npc(self):
        npc_id = self.npc_id
        QtBind.setText(gui,gui_task_value,f'Entering NPC {self.npc_name}')
        i = 0
        opcode =[0x7045,0x704B,0x7046]
        data = [struct.pack('<I',npc_id),struct.pack('<I',npc_id),struct.pack('<I',npc_id) + struct.pack('1B',0x01)]
        inject_joymax(opcode[i],data[i],False)
        i += 1
        Timer(2.0,inject_joymax,[opcode[i],data[i],False]).start()
        i += 1
        Timer(2.3,inject_joymax,[opcode[i],data[i],False]).start()
        Timer(4.0,self.buy_items,[]).start()

    def buy_items(self,count=0):
        items_to_buy = self.list_items_to_buy        
        if items_to_buy:
            data_codes = []
            item_ingame_names = []
            if self.npc_id:
                QtBind.setText(gui,gui_task_value,f'Buying items')
                for i in items_to_buy:
                    data_codes.append(self.build_data_bytes(items_to_buy[i][1],items_to_buy[i][2],self.npc_id))
                    item_ingame_names.append(items_to_buy[i][3])
                Timer(count + 1.5,log,[f'{PLUGIN}: Buying {item_ingame_names[count]}']).start()
                Timer(count + 2,inject_joymax,[0x7034,data_codes[count],False]).start()
                if len(data_codes)-1 > count:
                    count += 1
                    self.buy_items(count)
                else:
                    Timer(count + 3,self.leave_npc,[self.npc_id]).start()
                    Timer(count + 4.5,start_bot,[]).start()
                    Timer(count + 6,reset_buyer,[]).start()

    def leave_npc(self,npc_id):
        inject_joymax(0x704B,struct.pack('<I',npc_id),False)
        self.is_buying_items = False

    def read_db_comp_table(self,table,col,item):
        if db_path == '':
            db_path = QtBind.text(gui,path_database)
        db_list = []
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = f"SELECT * FROM {table}"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            if row[col] == item:
                db_list.append(row)
        return db_list

def reset_buyer():
    global buy_items,blocker_buy
    buy_items = None
    QtBind.setText(gui,gui_task_value,f'')
    Timer(DEFAULT_BUY_ITEMS_DELAY,change_blocker_buy,[False]).start()

def change_blocker_buy(state):
    global blocker_buy
    blocker_buy = state
#PhBot Events
def handle_joymax(opcode, data):
    global quest
    if opcode == 0xB0A1:
        Timer(2.0,update_skills,()).start()
    if opcode == 0x3056:
        change_area()
    if opcode == 0x30D4 and not quest == None:
        quest.quest_data = data
    if opcode == 0xB04B and not quest == None:
        quest.is_talking_to_npc = False
    return True
         
def teleported():
    global game_data_loaded,quest
    if not game_data_loaded:
        log(f'{PLUGIN}: Loading data')
        load_game_data()
        Timer(2.0,load_last_plugin_settings,()).start()
        Timer(5.0,create_config_file,()).start()
        game_data_loaded = True
        return
    if not quest == None:
        if quest.is_teleporting_for_quest:
            quest.is_teleporting_for_quest = False
            quest.do_quest()
            return
    if enabled and auto_quest and quest == None:
        Timer(4.0,do_auto_quest,()).start()
        return
    if not char == None and enabled:
        save_settings()
        
def handle_event(t, data):
    if t == 10:
        change_area()

counter = 0
quest_counter = 0
def event_loop():
    global quest,counter,quest_counter,buy_items,blocker_buy,custom_timer
    if not quest == None:
        if quest.is_walking_to_npc:
            stats = update_states()
            quest.cur_char_position = stats[1],stats[2]
            if counter == 2:
                quest.walk_to_npc()
                counter = 0
            else:
                counter += 1
        elif quest.is_walking_to_monster:
            stats = update_states()
            quest.cur_char_position = stats[1],stats[2]
            if counter == 2:
                quest.walk_to_monster()
                counter = 0
            else:
                counter += 1
        elif quest.is_attacking_monsters:
            if counter == 2:
                stats = update_states()
                quest.check_quest_taken()
                counter = 0
            else:
                counter += 1
    if enabled and auto_quest and quest == None:
        if quest_counter >= 60:
            q = check_available_quest()
            if q:
                if "Inventory" in q:
                    quest_counter = 0
                    reg = get_position()
                    pos = readDB('regioninfo',0,reg['region'])[1]
                    if pos == "#TOWN":                        
                        do_auto_quest()
                elif "Beginner's Assistant" in q:
                    quest_counter = 0
                    do_auto_quest() 
                else:
                    quest_counter = 0                               
            else:
                quest_counter = 0
        else:
            quest_counter += 1
    if not buy_items == None:
        if buy_items.is_walking_to_npc:
            stats = update_states()
            buy_items.cur_char_position = stats[1],stats[2]
            buy_items.walk_to_npc()
    if enabled and buy_npc_items and quest == None and buy_items == None and not blocker_buy:
        buy_items = Buy_items()
        if is_in_town():
            if buy_items.check_if_items_available():
                blocker_buy = True
                buy_items.buy()
            else:
                buy_items = None
    
def handle_chat(t,player,msg):
    global dic_party_roles
    if t == 4:
        if msg.startswith(PLUGIN + ": Role = ") and reading_chat:
            msg = msg[len(PLUGIN) + 9:]
            dic_party_roles[player] = msg
        elif msg.startswith(PLUGIN):
            msg = msg[len(PLUGIN)+2:]
            if msg == "Get Role" and not reading_chat:
                phBotChat.Party(PLUGIN + ": Role = " +char.role)

def check_Update():
	global NewestVersion
	if NewestVersion == 0:
		try:
			req = urllib.request.Request('https://raw.githubusercontent.com/Day4Date/PhBot-Plugins/refs/heads/main/AutoParty.py', headers={'User-Agent': 'Mozilla/5.0'})
			with urllib.request.urlopen(req) as f:
				lines = str(f.read().decode("utf-8")).split()
				for num, line in enumerate(lines):
					if line == 'PLUGIN_VERSION':
						NewestVersion = int(lines[num+2].replace(".",""))
						CurrentVersion = int(str(PLUGIN_VERSION).replace(".",""))
						if NewestVersion > CurrentVersion:
							log(f'Plugin: There is an update avaliable for {PLUGIN}!')
		except:
			pass
      
check_Update()
log(f'Plugin: {PLUGIN} v{str(PLUGIN_VERSION)} sucessfully loaded!')
