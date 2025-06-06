from phBot import *
import phBotChat
import QtBind
import sqlite3
import struct
import json 
import os
from threading import Timer
import urllib.request
import random


PLUGIN = "AutoParty"
PLUGIN_VERSION = 1.2
MAX_LEN_SCRIPT = 90
DEFAULT_PARTY_SIZE = "8"
DEFAULT_AREA_DELAY = 5
DEFAULT_AREA_OFFSET = 0
DEFAULT_AUTO_AREA = True
DEFAULT_BUY_ITEMS_DELAY = 180
db_path = ''
NewestVersion = 0

###Skill Lists###
## Eu ##
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
LIST_WIZ_BUFFS = ["Life Control","Life Turnover","Earth Barrier","Earth Fence","Bless Spell","Holy Word","Holy Spell","Moving March","Swing March","Noise"]
#XBow
LIST_XBOW_ATTACKS = ["Power Shot","Intense Shot","Fast Shot","Rapid Shot","Long Shot","Distance Shot","Blast Shot","Hurricane Shot"]
LIST_XBOW_BUFFS = ["Bless Spell","Holy Word","Holy Spell","Moving March","Swing March","Noise"]
#Dagger
LIST_DAGGER_ATTACKS = ["Spinning","Wounds","Mortal Wounds","Scud","Screw","Combo Blow","Butterfly Blow","Prick"]
LIST_DAGGER_BUFFS = ["Bless Spell","Holy Word","Holy Spell","Moving March","Swing March","Noise"]
#Warlock
LIST_WARLOCK_ATTACKS = ["Blood Flower","Death Flower","Bloody Trap","Death Trap","Blaze","Dark Blaze","Toxin ","Toxin Invasion","Decayed","Dark Decayed",
                        "Curse Breath","Dark Breath","Medical Raze","Magical Ravage","Combat Raze","Combat Ravage","Courage Raze","Courage Ravage",
                        "Vampire Touch","Vampire Kiss"]
LIST_WARLOCK_BUFFS = ["Mirage","Phantasma","Reflect","Advanced Reflect","Bless Spell","Holy Word","Holy Spell"]
#Bard
LIST_BARD_ATTACKS = ["Horror Chord","Weird Chord","Booming Chord","Booming Wave",]
LIST_BARD_BUFFS_MAIN = ["Moving March","Swing March","Guard Tambour","Noise","Mana Cycle","Mana Orbit","Cure Music"]
LIST_BARD_BUFFS_SECOND = ["Moving March","Swing March","Mana Tambour","Noise","Mana Cycle","Dancing of Magic","Dancing of Wizardry","Cure Music"]
LIST_BARD_PARTY_BUFFS = ["Mana Switch","Mana Cycle"]
#Cleric
LIST_CLERIC_ATTACKS = ["Trial Cross","Justice Cross","Over Healing","Glut Healing"]
LIST_CLERIC_BUFFS = ["Reverse","Grad Reverse","Healing Cycle","Soul Deity","Integrity",
                     "Healing Orbit","Bless Spell","Recovery Division","Holy Recovery Division","Group Reverse",
                     "Holy Group Reverse","Reverse Oblation","Reverse Immolation","Holy Word","Holy Spell","Body Blessing","Body Deity","Soul Blessing"]
LIST_CLERIC_PARTY_BUFFS = ["Force Blessing","Force Deity","Mental Blessing","Mental Deity","Body Blessing","Body Deity","Soul Blessing","Soul Deity",
                           "Healing Cycle"]
LIST_CLERIC_HEALING_BUFFS = ["Group Recovery","Healing Division","Group Healing","Group Healing Breath","Healing Favor","Holy Group Recovery"]

LIST_INT_BUFFS = ["Mental Blessing","Mental Deity"]
LIST_STR_BUFFS = ["Force Blessing","Force Deity"]
LIST_PHY_BUFFS = ["Body Blessing","Body Deity"]
LIST_MAG_BUFFS = ["Soul Blessing","Soul Deity"]

LIST_LIMITED_PARTY_BUFFS = ["Mental Blessing","Mental Deity","Force Blessing","Force Deity","Pain Quota","Physical Fence","Magical Fence","Protect"]
LIST_SCRIPT_BUFFS=["Moving March","Swing March","Guard Tambour","Noise","Soul Deity","Recovery Division","Holy Recovery Division"]
LIST_EXCL_BUFFS = ['Str','Int','Pain Quota','Physical Fence',"Magical Fence","Protect","Physical Screen","Ultimate Screen","Morale Screen"]
## Ch ##
#Bicheon
LIST_BICHEON_ATTACKS = ["Strike Smash","Stab Smash","Crosswise Smash ","Flying Stone Smash","Twin Energy Smash","Illusion Chain","Blood Chain","Billow Chain",
                        "Ascension Chain","Heaven Chain","Lightning Chain","Thousand Army Chain","Soul Cut Blade","Evil Cut Blade","Devil Cut Blade","Demon Cut Blade",
                        "Ghost Cut Blade","Blood Blade Force","Soul Blade Force","Demon Blade Force","Ocean Blade Force","Flower Bloom Blade","Flower Bud Blade",
                        "Dragon Sore Blade","Asura Cut Blade","Heavenly Blade","Snake Sword Dance","Petal Sword Dance","Typhoon Sword Dance","Chaotic Sword Dance"]
LIST_BICHEON_NUKER_ATTACKS = ["Illusion Chain","Blood Chain","Billow Chain",
                        "Ascension Chain","Heaven Chain","Lightning Chain","Thousand Army Chain","Soul Cut Blade","Evil Cut Blade","Devil Cut Blade","Demon Cut Blade",
                        "Ghost Cut Blade""Flame Wave - Arrow ","Flame Wave - Burning","Flame Wave - Wide","Flame Wave - Bomb","Flame Wave - HellFire","Flame Wave - Disintegrate",
                      "Wolf's Thunderbolt","Tiger's Thunderbolt","Horse's Thunderbolt","Crane's Thunderbolt","Shock Lion Shout","Heaven Lion Shout","Earth Lion Shout",
                      "Power Lion Shout","Execution Lion Shout","Cold wave - Arrest","Cold wave - Binding","Cold wave - Shackle","Cold Wave - Freeze","Cold Wave - Soul",
                      "Snow Storm - Ice shot","Snow Storm - Ice rain","Snow Storm - Double Shot","Snow Storm - Multi Shot"]
LIST_BICHEON_BUFFS = ["Flame body - Wisdom","Flame body - Power","Flame body - Extreme","Flame Body - Trial","Flame Body - God","Basic Fire protection",
                      "Divine Fire protection","Hard Fire protection","Earth Fire Protection","God Fire Protection","Must - Piercing Force","Flow - Piercing Force",
                      "Speed - Piercing Force","Force - Piercing Force","God - Piercing Force","Grass Walk - Flow","Ghost Walk - phantom","Grass Walk - Speed",
                      "Ghost Walk - Shadow","Ghost Walk - God","Concentration - 1st","Concentration - 2nd","Concentration - 3rd","Concentration - 4th","Weak Guard of Ice",
                      "Soft Guard of Ice","Power Guard of Ice","Might Guard of Ice","Final Guard of Ice","Harmony Therapy","Adaptation Therapy","Whole Therapy","Source Therapy",
                      "Castle Shield","Mountain Shield","Ironwall Shield","Giant Shield","Iron Castle Shield","Sun Guard Shield"]
#Heuksal
LIST_HEUKSAL_ATTACKS = ["Wolf Bite Spear","Waning Moon Spear","Yuhon Spear","Lightning Bird Spear","Celestial Cloud Spear","Dancing Demon Spear","Jade Breaking Spear",
                        "Spirit Crash Spear","Windless Spear","Death Bringer Spear","Soul Spear - Move","Soul Spear - Truth","Soul Spear - Soul","Soul Spear - Emperor",
                        "Soul Spear - Destruction","Ghost Spear - Petal","Ghost Spear - Prince","Ghost Spear - Mars","Ghost Spear - Storm Cloud","Ghost Spear - Emperor",
                        "Chain Spear - Tiger","Chain Spear - Nachal","Chain Spear - Shura","Chain Spear - Pluto","Chain Spear - Dragon","Chain Spear - Phoenix",
                        "Flying Dragon - Flow","Flying Dragon - Fly","Flying Dragon - Bless ","Flying Dragon - Flash"]
LIST_HEUKSAL_NUKER_ATTACKS = ["Soul Spear - Destruction","Ghost Spear - Petal","Ghost Spear - Prince","Ghost Spear - Mars","Ghost Spear - Storm Cloud","Ghost Spear - Emperor",
                        "Flying Dragon - Flow","Flying Dragon - Fly","Flying Dragon - Bless ","Flying Dragon - Flash","Flame Wave - Arrow ","Flame Wave - Burning","Flame Wave - Wide","Flame Wave - Bomb","Flame Wave - HellFire","Flame Wave - Disintegrate",
                      "Wolf's Thunderbolt","Tiger's Thunderbolt","Horse's Thunderbolt","Crane's Thunderbolt","Shock Lion Shout","Heaven Lion Shout","Earth Lion Shout",
                      "Power Lion Shout","Execution Lion Shout","Cold wave - Arrest","Cold wave - Binding","Cold wave - Shackle","Cold Wave - Freeze","Cold Wave - Soul",
                      "Snow Storm - Ice shot","Snow Storm - Ice rain","Snow Storm - Double Shot","Snow Storm - Multi Shot"]
LIST_HEUKSAL_BUFFS = ["Flame body - Wisdom","Flame body - Power","Flame body - Extreme","Flame Body - Trial","Flame Body - God","Basic Fire protection",
                      "Divine Fire protection","Hard Fire protection","Earth Fire Protection","God Fire Protection","Must - Piercing Force","Flow - Piercing Force",
                      "Speed - Piercing Force","Force - Piercing Force","God - Piercing Force","Grass Walk - Flow","Ghost Walk - phantom","Grass Walk - Speed",
                      "Ghost Walk - Shadow","Ghost Walk - God","Concentration - 1st","Concentration - 2nd","Concentration - 3rd","Concentration - 4th","Weak Guard of Ice",
                      "Soft Guard of Ice","Power Guard of Ice","Might Guard of Ice","Final Guard of Ice","Harmony Therapy","Adaptation Therapy","Whole Therapy","Source Therapy","Bloody Fan Storm",
                    "Bloody Wolf Storm","Bloody Snake Storm ","Bloody Demon Storm","Bloody Ghost Storm","Bloody Emperor Storm"]
#Pacheon
LIST_PACHEON_ATTACKS = ["Anti Devil Bow - Missile","Anti Devil Bow - Wave","Anti Devil Bow - Steel","Anti Devil Bow - Strike","Anti Devil Bow - Annihilate",
                        "Anti Devil Bow - Demolition","2 Arrow Combo","3 Arrow Combo","4 Arrow Combo ","5 Arrow Combo ","6 Arrow Combo","Autumn Wind - Flame",
                        "Autumn Wind - Snake","Autumn Wind - Blood","Autumn Wind - Red","Autumn Wind - Devil","Berserker Arrow","Demon Arrow","Devil Arrow",
                        "Celestial Beast Arrow","Strong Bow - Spirit","Strong Bow - Vision","Strong Bow - Craft","Strong Bow - Will","Mind Bow - Flower",
                        "Mind Bow - Butterfly","Mind Bow - Swift","Mind Bow - Lighting"]
LIST_PACHEON_BUFFS = ["Flame body - Wisdom","Flame body - Power","Flame body - Extreme","Flame Body - Trial","Flame Body - God","Basic Fire protection",
                      "Divine Fire protection","Hard Fire protection","Earth Fire Protection","God Fire Protection","Must - Piercing Force","Flow - Piercing Force",
                      "Speed - Piercing Force","Force - Piercing Force","God - Piercing Force","Grass Walk - Flow","Ghost Walk - phantom","Grass Walk - Speed",
                      "Ghost Walk - Shadow","Ghost Walk - God","Concentration - 1st","Concentration - 2nd","Concentration - 3rd","Concentration - 4th","Weak Guard of Ice",
                      "Soft Guard of Ice","Power Guard of Ice","Might Guard of Ice","Final Guard of Ice","White Hawk Summon","Black Hawk Summon","Blue Hawk Summon",
                      "Lightning Hawk Summon","Ice Hawk","Demon Soul Arrow","Bloody Soul Arrow","Dragon Soul Arrow","Phoenix Soul Arrow"]
#Nuker
LIST_NUKER_ATTACKS = ["Flame Wave - Arrow ","Flame Wave - Burning","Flame Wave - Wide","Flame Wave - Bomb","Flame Wave - HellFire","Flame Wave - Disintegrate",
                      "Wolf's Thunderbolt","Tiger's Thunderbolt","Horse's Thunderbolt","Crane's Thunderbolt","Shock Lion Shout","Heaven Lion Shout","Earth Lion Shout",
                      "Power Lion Shout","Execution Lion Shout","Cold wave - Arrest","Cold wave - Binding","Cold wave - Shackle","Cold Wave - Freeze","Cold Wave - Soul",
                      "Snow Storm - Ice shot","Snow Storm - Ice rain","Snow Storm - Double Shot","Snow Storm - Multi Shot"]


LIST_SKILL_EXCEPTIONS = ["Meteor"]
DIC_SKILL_NAME_CHANGER = {'Body Blessing':'Physical Buff','Body Deity':'Physical Buff','Soul Blessing':'Magical Buff','Soul Deity':'Magical Buff',
                    'Force Blessing':'Str','Force Deity':'Str','Mental Blessing':'Int','Mental Deity':'Int'}
### Training Areas ###
LIST_TRAINING_AREA =[{'level':4,'x': 6771.0, 'y': 1250.199951171875, 'z': 29.0, 'region': 25258, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':7,'x': 6642.7001953125, 'y': 1429.300048828125, 'z': 53.0, 'region': 25513, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':10,'x': 5780.5, 'y': 354.3999938964844, 'z': 301.0, 'region': 23973, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':13,'x': 5318.89990234375, 'y': 341.70001220703125, 'z': 1051.0, 'region': 23970, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':16,'x': 5003.2001953125, 'y': -10.899993896484375, 'z': 1387.0, 'region': 23457, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':19,'x': 4466.7998046875, 'y': 810.7999877929688, 'z': 179.0, 'region': 24734, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':23,'x': 4422.2998046875, 'y': 2106.199951171875, 'z': -123.0, 'region': 26270, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':25,'x': 4027.199951171875, 'y': 2307.60009765625, 'z': -40.0, 'region': 26779, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':27,'x': 3775.300048828125, 'y': 1971.4000244140625, 'z': -74.0, 'region': 26266, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':30,'x': 2887.5, 'y': 1647.199951171875, 'z': -71.0, 'region': 25750, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':32,'x': 2798.5, 'y': 994.2, 'z': 11.0, 'region': 24981, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':34,'x': 3251.5, 'y': 65.2, 'z': 225.0, 'region': 23703, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':38,'x': 2317.5, 'y': 328.2, 'z': 635.0, 'region': 23187, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':4,'x': -11482.5, 'y': 2688.199951171875, 'z': 19.0, 'region': 27211, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':7,'x': -12271.2001953125, 'y': 2567.10009765625, 'z': -20.0, 'region': 26951, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':10,'x': -12371.0, 'y': 3062.199951171875, 'z': -160.0, 'region': 27462, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':12,'x': -12667.900390625, 'y': 2882.5, 'z': 26.0, 'region': 27461, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':15,'x': -11625.7001953125, 'y': 2206.300048828125, 'z': -31.0, 'region': 26442, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
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
                     {'level':66,'x': -305.3999938964844, 'y': 1859.800048828125, 'z': -504.0, 'region': 25989, 'path': '', 'radius': 20.0, 'pick_radius': 50.0},
                     {'level':71,'x': -5522.10009765625, 'y': 632.0999755859375, 'z': 4003.0, 'region': 24426, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':74,'x': -5199.60009765625, 'y': -59.80000305175781, 'z': 2076.0, 'region': 23403, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':82,'x': -4157.89990234375, 'y': -497.8999938964844, 'z': 3305.0, 'region': 22897, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                     {'level':87,'x': -4977.7998046875, 'y': -138.60000610351562, 'z': 3114.0, 'region': 23405, 'path': '', 'radius': 15.0, 'pick_radius': 50.0},
                     {'level':95,'x': -22211.80078125, 'y': -581.9000244140625, 'z': -47.0, 'region': -32762, 'path': '', 'radius': 20.0, 'pick_radius': 50.0},
                     {'level':98,'x': -16425.8, 'y': -648.9, 'z': 805.0, 'region': 22577, 'path': '', 'radius': 20.0, 'pick_radius': 50.0}]

### Dic Quests Area  ###
DIC_QUEST_AREA = {'Inventory Expansion 1 (Europe)':{'x': -11303.400390625, 'y': 2670.199951171875, 'z': 42.0, 'region': 26956, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                  'Inventory Expansion 2 (Europe)':{'x': -6059.5, 'y': 2505.699951171875, 'z': 180.0, 'region': 26983, 'path': '', 'radius': 30.0, 'pick_radius': 50.0},
                  'Inventory Expansion 3 (Common)':{'x': -2042.300048828125, 'y': 82.19999694824219, 'z': 1550.0, 'region': 23676, 'path': '', 'radius': 50.0, 'pick_radius': 50.0},
                  'Inventory Expansion 1 (China)':{'x': 6455.5, 'y': 825.9000244140625, 'z': -29.0, 'region': 24744, 'path': '', 'radius': 50.0, 'pick_radius': 50.0},
                  'Inventory Expansion 2 (China)':{'x': 3608.0, 'y': 1450.0, 'z': 3, 'region': 25497, 'path': '', 'radius': 50.0, 'pick_radius': 50.0}}

### NPCS ###
LIST_NPC_PROTECTOR = ['Protector Trader Jatomo','Protector Trader Aryoan','Protector Trader Gonishya','Protector Trader Yeolah','Protector Trader Mrs Jang']
LIST_NPC_DRUG = {'EU':'Nun Retaldi','CA':'Nun Martel','OASIS_KINGDOM':'Potion Merchant Manina','WEST_CHINA':'Herbalist Bori','CHINA':'Herbalist Yangyun'}
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
use_chn_spots = False
auto_quest = False
auto_area = False
buy_npc_items = False
on_quest = False
bool_walk_to_quest = False
bool_walk_to_monster = False
blocker_buy = False
blocker_change_area = False
blocker_skills = False

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
checkChnSpots = QtBind.createCheckBox(gui,'checkChn_clicked', 'Use CHN Spots',x+110,y+60)
partySizeText = QtBind.createLabel(gui, 'Party Size', x, y+90)
partySize = QtBind.createCombobox(gui, x+100, y+90, 100, 20)
roleText = QtBind.createLabel(gui, 'Role', x+220, y+90)
roleValue = QtBind.createCombobox(gui, x+260, y+90, 100, 20)
QtBind.append(gui,roleValue,'Attacker')
QtBind.append(gui,roleValue,'Healer')
QtBind.append(gui,roleValue,'Bard')
QtBind.append(gui,roleValue,'Warrior')
QtBind.append(gui,roleValue,'Nuker')
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
button2 = QtBind.createButton(gui,'stop_script_clicked','Stop Script',x+100,y)
button3 = QtBind.createButton(gui,'buy_items_clicked','Buy Items',x+200,y)
button4 = QtBind.createButton(gui,'load_clicked','Load Settings',x,y+30)
button5 = QtBind.createButton(gui,'do_quest_clicked','Do Quest',x+100,y+30)
button6 = QtBind.createButton(gui,'add_skills_clicked','Add Skills',x+200,y+30)

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

def stop_script_clicked():
    stop_script()

def buy_items_clicked():
    item = Buy_items()
    item.buy_manual()

def load_clicked():
    global game_data_loaded
    log(f'{PLUGIN}: Loading data')
    load_game_data()
    Timer(2.0,load_last_plugin_settings,()).start()
    game_data_loaded = True

def do_quest_clicked():
    q = check_available_quest()
    if q:
        do_auto_quest()

def add_skills_clicked():
    add_skills()
    blocker_skills = True
    Timer(2.0,reset_skills,()).start()

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

def checkChn_clicked(checked):
    global use_chn_spots
    if checked:
        use_chn_spots = True
        change_plugin_configs(True,'Use Chn Spots')
        log(f'{PLUGIN}: Chn Spots enabled') 
    else:
        use_chn_spots = False
        change_plugin_configs(False,'Use Chn Spots')
        log(f'{PLUGIN}: Chn Spots disabled')

### Functions ###
def load_game_data():
    global char,game_data_loaded
    game_data_loaded = True
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
    dic_mastery = get_mastery()   
    dic_mastery = sorted(dic_mastery.items(), key=lambda item: item[1]['level'],reverse=True)
    list_masterys = []
    for i in range(0,len(dic_mastery)):
        if dic_mastery[i][1]['level'] > 0:
            id = dic_mastery[i][0]
            level = dic_mastery[i][1]['level']
            name = dic_mastery[i][1]['name']
            list_masterys.append({'Name':name,'ID':id,'Level':level})
    return list_masterys

def create_config_file():
    if game_data_loaded:
        if not os.path.exists(char.char_config_path):
            if not os.path.exists(char.folder_path):
                os.makedirs(char.folder_path)
            try:
                log(f"{PLUGIN}: Creating a new config file!")
                data={
                    "Name": "",
                    "Mastery": [],
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
                    "Buy Items":False,
                    "Use Caves": False,
                    "Use Chn Spots": False,
                    "Delay Area": "5",
                    "Offset Area": "0",
                    "Auto Area": False,
                    "DB Path": ""             
                }
                with open(char.char_config_path,'w',encoding='utf-8') as file:
                    json.dump(data,file,indent=4,ensure_ascii=False)
                Timer(2.0,save_settings,()).start()
            except:
                log(f"{PLUGIN}: Can´t create new config file!")

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
                if len(config_data['Mastery']) > 0:
                    config_data['Mastery']=[]
                for i in range(0,len(char.masterys)):                    
                    config_data['Mastery'].append(char.masterys[i])
                config_data['Skills']['Weapon'] = char.weapon              
                config_data['Skills']['Attack List'] = char.attack_list              
                config_data['Skills']['Buff List'] = char.buff_list              
                config_data['Skills']['Party Buff List'] = char.party_buff_list
                config_data['Skills']['Healing Buff List'] = char.healing_buff_list                             
                config_data['Role'] = QtBind.text(gui, roleValue)             
                config_data['Main Bard'] = is_main_bard
                config_data['Plugin enabled'] = enabled
                config_data['Party Size'] = QtBind.text(gui, partySize)   
                config_data['Buy Items'] = buy_npc_items
                config_data['Use Caves'] = use_cave
                config_data['Use Chn Spots'] = use_chn_spots
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
                    data['name'] = config_data.get('Name',"")
                    data['mastery'] = config_data.get('Mastery', None)
                    data['skills'] = {"weapon": config_data.get("Skills", {}).get("Weapon", []),
                                      "attack list": config_data.get("Skills", {}).get("Attack List", []),
                                      "buff list": config_data.get("Skills", {}).get("Buff List", []),
                                      "party buff list": config_data.get("Skills", {}).get("Party Buff List", []),
                                      "healing buff list": config_data.get("Skills", {}).get("Healing Buff List", [])
                                      }
                    data['role'] = config_data.get('Role', 'None')
                    data['main bard'] = config_data.get('Main Bard', False)
                    data['plugin enabled'] = config_data.get('Plugin enabled', False)
                    data['solo mode'] = config_data.get('Solo Mode', False)
                    data['auto quest'] = config_data.get('Auto Quest', False)
                    data['buy items'] = config_data.get('Buy Items', False)
                    data['party size'] = config_data.get('Party Size', 1)
                    data['delay area'] = config_data.get('Delay Area', 0)
                    data['offset area'] = config_data.get('Offset Area', 0)
                    data['auto area'] = config_data.get('Auto Area', False)
                    data['use cave'] = config_data.get('Use Caves', False)
                    data['use chn spots'] = config_data.get('Use Chn Spots', False)
                    data['db path'] = config_data.get('DB Path', '')
                except:
                    log(f"{PLUGIN}: Can´t read Data. An Error occured while reading the config file!")
    return data

def get_roles_from_chat():
    global reading_chat
    reading_chat = True
    phBotChat.Party(f"{PLUGIN}: Get Role")
    Timer(2.0,add_party_skills,[]).start()

def load_last_plugin_settings():
    global enabled, is_main_bard, solo_mode, auto_quest,char,buy_npc_items,auto_area,db_path,use_cave,use_chn_spots
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
    if data['use cave']:
        use_cave = True
        QtBind.setChecked(gui,checkCave,True)
    else:
       use_cave = False
    if data['use chn spots']:
        use_chn_spots = True
        QtBind.setChecked(gui,checkChnSpots,True)
    else:
       use_chn_spots = False
    if data['db path']:
        db_path = data['db path']
        QtBind.setText(gui,path_database,data['db path'])
    else:
       QtBind.setText(gui,path_database,'')
    if data['offset area']:
        QtBind.setText(gui,offsetChangeAreaValue,data['offset area'])
    else:
       QtBind.setText(gui,offsetChangeAreaValue,DEFAULT_AREA_OFFSET)
    if data['role']:
        QtBind.setText(gui,roleValue,data['role'])

def add_party_skills():  
    party_buff_data = {}
    dic = get_skills()
    party_buff_skills = get_skills_to_add(dic,char.first_id,char.party_buff_list) 
    config_file = get_profile_path()  
    with open(char.bot_config_path + config_file,"r") as file:
        config_data = json.load(file)
        party_buff_data['Str'] = config_data.get("Skills", {}).get("Party Buffs", []).get("Str",[])
        party_buff_data['Int'] = config_data.get("Skills", {}).get("Party Buffs", []).get("Int",[])
        party_buff_data['Physical Buff'] = config_data.get("Skills", {}).get("Party Buffs", []).get("Physical Buff",[])
        party_buff_data['Magical Buff'] = config_data.get("Skills", {}).get("Party Buffs", []).get("Magical Buff",[])
        party_buff_data['Healing Cycle'] = config_data.get("Skills", {}).get("Party Buffs", []).get("Healing Cycle",[])
        party_buff_data['Pain Quota'] = config_data.get("Skills", {}).get("Party Buffs", []).get("Pain Quota",[])
        party_buff_data['Physical Fence'] = config_data.get("Skills", {}).get("Party Buffs", []).get("Physical Fence",[])
        party_buff_data['Magical Fence'] = config_data.get("Skills", {}).get("Party Buffs", []).get("Magical Fence",[])
        party_buff_data['Protect'] = config_data.get("Skills", {}).get("Party Buffs", []).get("Protect",[])
        party_buff_data['Physical Screen'] = config_data.get("Skills", {}).get("Party Buffs", []).get("Physical Screen",[])
        party_buff_data['Morale Screen'] = config_data.get("Skills", {}).get("Party Buffs", []).get("Morale Screen",[])
        party_buff_data['Ultimate Screen'] = config_data.get("Skills", {}).get("Party Buffs", []).get("Ultimate Screen",[])
        party_buff_data['Mana Switch'] = config_data.get("Skills", {}).get("Party Buffs", []).get("Mana Switch",[])
        party_buff_data['Mana Cycle'] = config_data.get("Skills", {}).get("Party Buffs", []).get("Mana Cycle",[])
    for skill_server_name in party_buff_skills:
        for name,job in dic_party_roles.items():
            if char.role == "Warrior":
                if len(party_buff_data[party_buff_skills[skill_server_name]]) >= 2:
                    continue
                elif party_buff_skills[skill_server_name] == 'Pain Quota':
                    if name in party_buff_data['Physical Fence'] or name in party_buff_data['Magical Fence']:
                        continue
                elif party_buff_skills[skill_server_name] == 'Protect':
                    if name in party_buff_data['Physical Fence'] or name in party_buff_data['Magical Fence']:
                        continue                                            
                elif party_buff_skills[skill_server_name] == 'Physical Fence':
                    if name in party_buff_data['Pain Quota'] or name in party_buff_data['Protect']:
                        continue  
                elif party_buff_skills[skill_server_name] == 'Magical Fence':
                    if name in party_buff_data['Pain Quota'] or name in party_buff_data['Protect']:
                        continue
                elif party_buff_skills[skill_server_name] == 'Physical Screen':
                    if len(party_buff_skills[skill_server_name]) >= 1:
                        continue
                elif party_buff_skills[skill_server_name] == 'Morale Screen':
                    if len(party_buff_skills[skill_server_name]) >= 1:
                        continue
                elif party_buff_skills[skill_server_name] == 'Ultimate Screen':
                    if len(party_buff_skills[skill_server_name]) >= 1:
                        continue
            if char.role == "Healer":
                if party_buff_skills[skill_server_name] == 'Healing Cycle':
                    for key in dic:
                        if dic[key]['name'] == "Healing Orbit":
                            config_data['Skills']['Party Buffs']['Healing Cycle'] = []
                            break
            if char.role == "Bard":
                if party_buff_skills[skill_server_name] == 'Mana Cycle':
                    for key in dic:
                        if dic[key]['name'] == "Mana Orbit":
                            config_data['Skills']['Party Buffs']['Mana Cycle'] = []
                            break
            if job == 'Attacker':
                if char.role == "Bard" and not char.is_main_bard:
                    continue
                if not name in party_buff_data[party_buff_skills[skill_server_name]]:
                    config_data['Skills']['Party Buffs'][party_buff_skills[skill_server_name]].append(name)
            else:
                if char.role == "Bard" and char.is_main_bard:
                    continue
                if party_buff_skills[skill_server_name] in LIST_EXCL_BUFFS:
                    continue
                if party_buff_skills[skill_server_name] == 'Healing Cycle' and role == "Bard":
                    continue
                if not name in party_buff_data[party_buff_skills[skill_server_name]]:
                    config_data['Skills']['Party Buffs'][party_buff_skills[skill_server_name]].append(name)
    with open(char.bot_config_path + config_file,"w") as file:
        file.write(json.dumps(config_data,indent=4))
        log(f"{PLUGIN}: Party Buffs successfully changed in [{config_file}]")
        config_loader()

def add_skills():
    dic = get_skills()
    attack_skills = get_skills_to_add(dic,"Attack",char.attack_list)
    buff_skills = get_skills_to_add(dic,"Buffs",char.buff_list)
    healing_skills = get_skills_to_add(dic,"Buffs",char.healing_buff_list)
    config_file = get_profile_path()
    with open(char.bot_config_path + config_file,"r") as file:
        config_data = json.load(file)
        config_data['Skills']['sNormal'] = []
        config_data['Skills']['bNormal'] = []
        config_data['Skills']['Healing'] = []
        for x in attack_skills:
            config_data['Skills']['sNormal'].append(attack_skills[x])
        for x in buff_skills:
            config_data['Skills']['bNormal'].append(buff_skills[x])
        for x in healing_skills:
            config_data['Skills']['Healing'].append(healing_skills[x])
    with open(char.bot_config_path + config_file,"w") as file:
        file.write(json.dumps(config_data,indent=4))
        log(f"{PLUGIN}: Attacks successfully changed in [{config_file}]")
        config_loader()
    if not char.role == "Attacker" and not char.role == "Nuker":
        Timer(2.0,get_roles_from_chat,[]).start()

def get_dic_cur_skills(dic,skill_list):
    dic_servername = {}
    if dic == None:
        log(f"{PLUGIN}: Can´t create a list of skills. Dictionary is empty!")
        return None
    if skill_list == None:
        log(f"{PLUGIN}: Can´t create a list of skills. Skill list is empty!")
        return None
    for x in dic:
        if dic[x]['name'] in skill_list:
            dic_servername[dic[x]['servername']] = dic[x]['name']
    return dic_servername

def trim_string(string):
    numb_split = 4
    if '_EU_' in string:
        numb_split = 5
    pool = string.split('_')
    return '_'.join(pool[:numb_split])

def get_skills_to_add(dic,skill_type,skill_list):
    dic_servername = {}
    if dic == None:
        log(f"{PLUGIN}: Can´t create a list of skills to add. Dictionary is empty!")
        return None
    if skill_list == None:
        log(f"{PLUGIN}: Can´t create a list of skills to add. Skill list is empty!")
        return None
    for item in dic:
        skill_server_name = dic[item]['servername']
        skill_name = dic[item]['name']
        skill_trim_name = trim_string(skill_server_name)
        if skill_name in skill_list:
            if not any(skill_trim_name in key for key in dic_servername)or skill_name in LIST_SKILL_EXCEPTIONS:
                for key in DIC_SKILL_NAME_CHANGER:
                        if skill_name == key:
                            skill_name = DIC_SKILL_NAME_CHANGER[key]
                            break
                dic_servername[skill_server_name] = skill_name
            else:
                lvl = dic[item]['level']
                for newItem in dic:
                    new_skill_server_name = dic[newItem]['servername']
                    new_skill_trim_name = trim_string(new_skill_server_name)
                    if new_skill_trim_name == skill_trim_name:
                        new_lvl = dic[newItem]['level']
                        if lvl > new_lvl:
                            for name in dic_servername:
                                if new_skill_trim_name in name:
                                    dic_servername.pop(name)
                                    break
                            if not skill_type == "Buffs":
                                for key in DIC_SKILL_NAME_CHANGER:
                                        if skill_name == key:
                                            skill_name = DIC_SKILL_NAME_CHANGER[key]
                                            break
                            dic_servername[skill_server_name] = skill_name
    return dic_servername

def change_gap(gap):
    config_file = get_profile_path()
    with open(char.bot_config_path + config_file,"r") as file:
        config_data = json.load(file)   
        config_data["Auto Mastery"]["Gap"] = gap
    with open(char.bot_config_path + config_file,"w") as file:
        file.write(json.dumps(config_data,indent=4))
        log(f"{PLUGIN}: Gap successfully changed to [{str(gap)}]")
        config_loader() 

class Character(): 

    def __init__(self):        
        self.data = get_character_data()
        self.name = self.data['name']
        self.server = self.data['server']
        self.bot_config_path = get_config_dir()
        self.folder_path = self.bot_config_path + f"\{PLUGIN}\\"  
        self.char_config_path = self.folder_path + f"{self.server}_{self.name}.json"
        self.is_main_bard = self.get_main_bard()
        self.__load_data()

    def get_data(self):
        self.__load_data()

    def get_data_from_json(self):
        self.__load_data_from_json()

    def get_role(self):
        if os.path.exists(self.char_config_path):
            with open(self.char_config_path,"r") as file:
                config_data = json.load(file)
                try:
                    role = config_data.get('Role',"")
                    return role
                except:
                    pass
        role = QtBind.text(gui, roleValue)
    
    def get_main_bard(self):
        main_bard = False
        if os.path.exists(self.char_config_path):
            with open(self.char_config_path,"r") as file:
                config_data = json.load(file)
                try:
                    main_bard = config_data.get('Main Bard',False)
                except:
                    main_bard = False
                    log(f'{PLUGIN}: Failed to load config file for [{self.name}]')
        if main_bard:
            return True
        return False

    def __load_data(self):
        self.masterys = get_masterys()
        self.role = self.get_role()
        self.__get_skill_list()

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
    
    def __get_skill_list(self):
        inventory = get_inventory()
        weapon = inventory['items'][6]['servername']        
        self.weapon = weapon
        self.buff_list = ""
        self.attack_list = ""
        self.party_buff_list = ""
        self.healing_buff_list = ""
        if len(self.masterys) < 1:
            self.attack_list = ""
            self.buff_list = ""
            self.party_buff_list = ""
            self.healing_buff_list = ""
        else:
            self.first_mastery_name = self.masterys[0]['Name']
            self.first_id = self.masterys[0]['ID']
        for i in range(0,len(self.masterys)):
            if self.masterys[i]['Name'] == "Cleric" and self.role == "Healer":
                self.attack_list = LIST_CLERIC_ATTACKS
                self.buff_list = LIST_CLERIC_BUFFS
                self.party_buff_list = LIST_CLERIC_PARTY_BUFFS
                self.healing_buff_list = LIST_CLERIC_HEALING_BUFFS
                return
            elif self.masterys[i]['Name'] == "Bard" and self.role == "Bard":
                self.attack_list = LIST_BARD_ATTACKS
                if self.is_main_bard:
                    self.buff_list = LIST_BARD_BUFFS_MAIN
                else:
                    self.buff_list = LIST_BARD_BUFFS_SECOND
                self.party_buff_list = LIST_BARD_PARTY_BUFFS
                return
            elif self.masterys[i]['Name'] == "Warrior" and self.role == "Warrior":
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
                return
            elif self.masterys[i]['Name'] == "Wizard" and self.role == "Attacker":
                self.attack_list = LIST_WIZ_ATTACKS
                self.buff_list = LIST_WIZ_BUFFS
                return 
            elif self.masterys[i]['Name'] == "Rogue" and self.role == "Attacker":
                if "CROSSBOW" in weapon:
                    self.attack_list = LIST_XBOW_ATTACKS
                    self.buff_list = LIST_XBOW_BUFFS
                elif "DAGGER" in weapon:
                    self.attack_list = LIST_DAGGER_ATTACKS
                    self.buff_list = LIST_DAGGER_BUFFS
                return 
            elif self.masterys[i]['Name'] == "Warlock" and self.role == "Attacker":
                self.attack_list = LIST_WARLOCK_ATTACKS
                self.buff_list = LIST_WARLOCK_BUFFS
                return
            elif self.masterys[i]['Name'] == "Pacheon" and self.role == "Attacker":
                self.attack_list = LIST_PACHEON_ATTACKS
                self.buff_list = LIST_PACHEON_BUFFS
                return 
            elif self.masterys[i]['Name'] == "Bicheon":
                if self.role == "Attacker":
                    self.attack_list = LIST_BICHEON_ATTACKS
                    self.buff_list = LIST_BICHEON_BUFFS
                    return
                elif self.role == "Nuker":
                    self.attack_list = LIST_BICHEON_NUKER_ATTACKS
                    self.buff_list = LIST_BICHEON_BUFFS
                    return 
            elif self.masterys[i]['Name'] == "Heuksal":
                if self.role == "Attacker":
                    self.attack_list = LIST_PACHEON_ATTACKS
                    self.buff_list = LIST_PACHEON_BUFFS
                    return 
                elif self.role == "Nuker":
                    self.attack_list = LIST_HEUKSAL_NUKER_ATTACKS
                    self.buff_list = LIST_HEUKSAL_BUFFS
                    return
             

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
        if current_quests:
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

def reset_skills():
    global blocker_skills
    blocker_skills = False

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
        if party:
            if  not len(party) >= int(QtBind.text(gui,partySize)) and not solo_mode:
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
                    if area['region'] < 0 and lvl < 71:
                        if not use_cave:
                            continue
                    if area['x'] > 0 and lvl < 40:
                        if not use_chn_spots:
                            continue  
                    blocker_change_area = True       
                    stop_bot()
                    set_training_script('')
                    Timer(0.5,set_training_position,[area['region'], area['x'], area['y'],area['z']]).start()
                    Timer(1.0,start_bot,()).start()
                    Timer(0.1+float(QtBind.text(gui,delayChangeAreaValue))*60,reset_blocker_change_area,()).start()
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
    cur_area = get_current_auto_area()
    if cur_area:
        cur_area_level = cur_area['level']
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

def get_char_db():
    path = get_config_path()
    path = path[:-4]+'db3'
    return path

def change_char_db(table,id,column1='',column2='',t1=0,amount=0):
    dbPath =  get_char_db()
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    if table == 'town':
        query = f"UPDATE {table} SET {column1} = '{t1}', {column2} = {amount} WHERE id = {id}"
        cursor.execute(query)
        conn.commit()
        conn.close()

def read_char_db(table,id='',servername='',itemname=''):
	dbPath = get_char_db()
	conn = sqlite3.connect(dbPath)
	cursor = conn.cursor()
	query = f"SELECT * FROM {table}"
	cursor.execute(query)
	rows = cursor.fetchall()
	conn.close()
	if id:
		for row in rows:
			if row[0] == id:
				return row    
	elif servername:
		for row in rows:
			if row[1] == servername:
				return row
	elif itemname:
		for row in rows:
			if row[2] == itemname:
				return row

def get_npc_position_from_db(quest):
    if "Beginner's Assistant" in quest:
        quest = "Lv. 5 Beginner's Assistant"
    npc_start = readDB('quest',2,quest)[3].split(',')
    if len(npc_start) < 2 and "Beginner's Assistant" in quest:
        if not is_in_town():
            return
        reg = readDB('zones',0,get_position()['region'])[1].upper()
        npc_start = LIST_NPC_DRUG[reg]
        npc_start = readDB('monsters',2,npc_start)[1]
    if len(npc_start) > 1:
        reg = readDB('zones',0,get_position()['region'])[1].upper()
        if reg == "CHINA":
            reg = "_CH_"
        elif reg == "WEST_CHINA":
            reg = "_WC_"
        elif reg == "OASIS_KINGDOM":
            reg = "_KT_"
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
    if list_script == None:
        log(f'{PLUGIN}: Error at "generate_script_to_destination". Path could not be found')
    if list_script:
        walk_scr = ""
        for item in list_script:
            walk_scr += item + '\n'
        return walk_scr
    else:
        log(f'{PLUGIN}: Error at "get_script_to_npc". Could not generate script') 


# Execute Quest #   
def do_auto_quest():
    global quest
    q = check_available_quest()
    if q:
        free_size = get_free_inventory_slots()
        if free_size > 0:
            quest = Quest(q)
            quest.do_quest()
    return

def get_current_inventory_size():
    c_inventory = get_inventory() 
    return c_inventory['size']

def get_free_inventory_slots():
    inv = get_inventory()
    counter = 0
    index = 0
    for i in inv['items']:
        index += 1
        if index >13:
            if i == None:
                counter += 1
    return counter

def check_available_quest():    
    c_data = get_character_data()
    model = c_data['model']
    level = c_data['level']
    race = 'EU'
    char_servername = get_monster(model)['servername']
    if "_CH_" in char_servername:
        race = 'CHN'
    cur_inv_size = get_current_inventory_size()
    current_quests = get_quests()
    if current_quests:
        for item in current_quests:
            if "Beginner's Assistant" in current_quests[item]['name']:
                return str(current_quests[item]['name'])
    if cur_inv_size == 45 and level >= 5:
        if race == 'EU':
            return 'Inventory Expansion 1 (Europe)'
        elif race == 'CHN':
            return 'Inventory Expansion 1 (China)'
    if cur_inv_size == 55 and level >= 32:
        if race == 'EU':
           return 'Inventory Expansion 2 (Europe)'
        elif race == 'CHN':
            return 'Inventory Expansion 2 (China)'
    if cur_inv_size == 59 and level >= 64:
        return 'Inventory Expansion 3 (Common)'
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
            if int(self.npc_game_x)-3 <= int(self.cur_char_position[0]) <= int(self.npc_game_x)+3:
                if int(self.npc_game_y)-3 <= int(self.cur_char_position[1]) <= int(self.npc_game_y)+3:
                    log(f'{PLUGIN}: Script finished. Talking to NPC')
                    stop_script()
                    self.is_walking_to_npc = False
                    self.enter_npc()
    
    def walk_to_monster(self):
        if not self.is_walking_to_monster:
            self.script_to_monster = generate_script_to_destination(DIC_QUEST_AREA[self.name]['region'],DIC_QUEST_AREA[self.name]['x'],DIC_QUEST_AREA[self.name]['y'])
            self.script_last_x,self.script_last_y = (self.script_to_monster.strip().split("\n"))[-1].split(",")[1:3]
            if self.script_to_monster:
                log(f'{PLUGIN}: Walking to Monster')
                QtBind.setText(gui,gui_task_value,'Walking to Monster')
                self.is_walking_to_monster = True
                start_script(self.script_to_monster)
        elif self.is_walking_to_monster:
            if int(DIC_QUEST_AREA[self.name]['x'])-3 <= int(self.cur_char_position[0]) <= int(DIC_QUEST_AREA[self.name]['x'])+3:
                if int(DIC_QUEST_AREA[self.name]['y'])-3 <= int(self.cur_char_position[1]) <= int(DIC_QUEST_AREA[self.name]['y'])+3:
                    log(f'{PLUGIN}: Script finished. Starting Quest')
                    stop_script()
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
        if not npc:
            log(f'{PLUGIN}: Could not find NPC')
            return
        for id in npc:
            if npc[id]['servername'] == self.npc_start_name:
                break
        log(f'{PLUGIN}: Entering NPC {self.npc_ingame_name}')
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
        if self.current_character_quests:
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
                    log(f'{PLUGIN}: Generating Script to Monster')               
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
        c_data = get_character_data()
        model = c_data['model']
        level = c_data['level']
        char_servername = get_monster(model)['servername']
        if "_CH_" in char_servername:
            return c_data['level']
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
                char_set[x] = inv['items'][1]
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
            if int(self.npc_game_x)-3 <= int(self.cur_char_position[0]) <= int(self.npc_game_x)+3:
                if int(self.npc_game_y)-3 <= int(self.cur_char_position[1]) <= int(self.npc_game_y)+3:
                    log(f'{PLUGIN}: Script finished. Talking to NPC')
                    self.is_walking_to_npc = False
                    self.is_at_npc = True
                    self.enter_npc()

    def buy(self):
        stop_bot()
        log(f'{PLUGIN}: Items available! Buying Items')
        self.is_buying_items = True
        if self.is_at_npc:
            log(f'{PLUGIN}: Buying items')
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
    global quest,blocker_skills
    if opcode == 0xB0A1:
        if not blocker_skills:
            Timer(12.0,add_skills,()).start()
            blocker_skills = True
            Timer(15.0,reset_skills,()).start()
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
        Timer(5.0,create_config_file,()).start()
        Timer(7.0,load_last_plugin_settings,()).start()
        game_data_loaded = True
        return
    if not quest == None:
        if quest.is_teleporting_for_quest:
            quest.is_teleporting_for_quest = False
            Timer(5.0,quest.do_quest,()).start()
            return
    if not char == None and enabled:
        save_settings()
        

counter = 0
quest_counter = 0
save_counter = 0
def event_loop():
    global quest,counter,quest_counter,buy_items,blocker_buy,save_counter
    if enabled and save_counter >= 240:
        if not char == None:
            save_settings()
        save_counter = 0
    elif enabled:
        save_counter += 1
    if not quest == None and not blocker_buy:
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
    if enabled and auto_quest and quest == None and not blocker_buy:
        if quest_counter >= 20 and is_in_town():
            quest_counter = 0
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
            quest_counter += 1
    if not buy_items == None and quest == None:
        if buy_items.is_walking_to_npc:
            stats = update_states()
            buy_items.cur_char_position = stats[1],stats[2]
            buy_items.walk_to_npc()
    if enabled and buy_npc_items and quest == None and buy_items == None and not blocker_buy:        
        if is_in_town():
            buy_items = Buy_items()
            free_size = get_free_inventory_slots()
            if free_size > 0:
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
        elif msg == "RELOAD":
            load_clicked()
        elif msg.startswith('OFFAREA'):
            msg = msg[8:]
            QtBind.setText(gui,offsetChangeAreaValue,msg)
        elif msg.startswith('DISABLE'):
            checkEnable_clicked(False)
            QtBind.setChecked(gui,checkEnable,False)
        elif msg.startswith('ENABLE'):
            checkEnable_clicked(True)
            QtBind.setChecked(gui,checkEnable,True)
        elif msg == "STOP":
            stop_bot()
        elif msg == "START":
            start_bot()        
        elif msg == "TRACEME":
            start_trace(player)
        elif msg.startswith("TRACE"):
            msg = msg.rstrip()
            if msg == "TRACE":
                if start_trace(player):
                    log("Plugin: Starting trace to ["+player+"]")
            else:
                msg = msg[5:].split()[0]
                if start_trace(msg):
                    log("Plugin: Starting trace to ["+msg+"]")
        elif msg == "NOTRACE":
            stop_trace()
        elif msg == "ATKHERE":
            stop_trace()
            set_training_script('')
            p = get_position()
            set_training_position(p['region'], p['x'], p['y'],p['z'])
            Timer(1.0,start_bot,()).start()
        elif msg.startswith("SETPOS"):
            msg = msg.rstrip()
            if msg == "SETPOS":
                set_training_script('')
                p = get_position()
                set_training_position(p['region'], p['x'], p['y'],p['z'])
                log("Plugin: Training area set to current position (X:%.1f,Y:%.1f)"%(p['x'],p['y']))
            else:
                try:
                    set_training_script('')
                    p = msg[6:].split(',')
                    x = float(p[0])
                    y = float(p[1])
                    region = int(p[2]) if len(p) >= 3 else 0
                    z = float(p[3]) if len(p) >= 4 else 0
                    set_training_position(region,x,y,z)
                    log("Plugin: Training area set to (X:%.1f,Y:%.1f)"%(x,y))
                except:
                    log("Plugin: Wrong training area coordinates!")
        elif msg.startswith('SETAREA '):
            msg = msg[8:]
            if msg:
                set_training_script('')
                if set_training_area(msg):
                    log('Plugin: Training area has been changed to ['+msg+']')
                else:
                    log('Plugin: Training area ['+msg+'] not found in the list')
        elif msg.startswith("SETRADIUS"):
            msg = msg.rstrip()
            if msg == "SETRADIUS":
                radius = 35
                set_training_radius(radius)
                log("Plugin: Training radius reseted to "+str(radius)+" m.")
            else:
                try:
                    radius = int(float(msg[9:].split()[0]))
                    radius = (radius if radius > 0 else radius*-1)
                    set_training_radius(radius)
                    log("Plugin: Training radius set to "+str(radius)+" m.")
                except:
                    log("Plugin: Wrong training radius value!")
        elif msg == "RETURN":
            character = get_character_data()
            if character['hp'] == 0:
                log('Plugin: Resurrecting at town...')
                inject_joymax(0x3053,b'\x01',False)
            else:
                log('Plugin: Trying to use return scroll...')
                Timer(random.uniform(0.5,2),use_return_scroll).start()
        elif msg.startswith("GAP"):
            msg = msg[4:]
            change_gap(int(msg))
        elif msg == "SAVE":
            save_clicked()
        elif msg.startswith('BUY '):
            msg = msg[4:].split(',')
            if msg:
                row = read_char_db('town',itemname=msg[0])
                if row:
                    change_char_db('town',row[0],'enabled','quantity',1,msg[1])
                    log(f'Plugin: Added {msg[0]} to Townloop. Quantity: {msg[1]}')
        elif msg.startswith('NOBUY '):
            msg = msg[6:]
            if msg:
                row = read_char_db('town',itemname=msg)
                if row:
                    change_char_db('town',row[0],'enabled','quantity',0,0)
                    log(f'Plugin: Removed {msg} from Townloop.')
        elif msg.startswith("TP"):
            msg = msg[3:]
            if not msg:
                return
            split = ',' if ',' in msg else ' '
            source_dest = msg.split(split)
            if len(source_dest) >= 2:
                inject_teleport(source_dest[0].strip(),source_dest[1].strip())
        
        


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
