import QtBind
import struct
from threading import Timer
import sqlite3
from phBot import *

Plugin = "AutoTraining"
PlguinVersion = "1.0"

gui = QtBind.init(__name__, 'AutoTraining')
x = 10
y = 10
button1 = QtBind.createButton(gui,'button1_clicked','Button 1',x,y)

def button1_clicked():
   check_level(20)

#Put here the coordinates and level when you want to change to that area
#These below are for EU, starting in Constatinople
spots =[{'level':1,'x':-11372,'y':2491,'radius':20},{'level':4,'x':-12077,'y':2602,'radius':20},{'level':8,'x':-12332,'y':2770,'radius':20},
        {'level':10,'x':-12001,'y':2333,'radius':20},{'level':14,'x':-11807,'y':1511,'radius':20},{'level':18,'x':-11665,'y':1312,'radius':20},
        {'level':20,'x':-8685,'y':2277,'radius':20},{'level':25,'x':-6991,'y':2627,'radius':20},{'level':28,'x':-5232,'y':2587,'radius':20},
        {'level':30,'x':-5224,'y':2298,'radius':20},{'level':34,'x':-3969,'y':2531,'radius':20},{'level':38,'x':-3344,'y':2447,'radius':20}]

#TrainingArea
def check_level(level):
    #searching for the possible spot
    lowest = 0
    for spot in spots:
        if lowest <= spot['level'] <= level:
            lowest = spot['level']
            newArea = spot
    #checking if the current Area is the same
    currentArea = get_training_area()
    if not currentArea['x'] == newArea['x'] and not currentArea['y'] == newArea['y']:
        #changing to the new Area
        log(f'{Plugin}: Changing to new Area')    
        stop_bot()
        set_training_script('')
        region = 0
        x = newArea['x']
        y = newArea['y']
        z = 0
        radius = newArea['radius']
        Timer(2.0,set_training_position,[region, x, y, z]).start()
        Timer(3.0,start_bot,()).start()
        Timer(4.0,set_training_radius,[radius]).start()
    return

def check_party():
    level = get_character_data()
    lvl = level['level']
    lowestLvl = lvl
    party = get_party()
    if party:
        if len(party)==8:
            for key in party:
                if party[key]['name'] == level['name']:
                    continue
                elif party[key]['level'] > 0 and party[key]['level'] < lowestLvl:
                    lowestLvl = party[key]['level']
            check_level(lowestLvl)
    return
    
def handle_joymax(opcode,data):
    if opcode == 0x3056:
        check_party()
    return True

log(f'Plugin: {Plugin} v{PlguinVersion} sucessfully loaded!')