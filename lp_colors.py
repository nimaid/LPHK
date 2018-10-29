BLACK = 0
WHITE_THIRD = 1
WHITE_HALF = 2
WHITE = 3
RED = 5
RED_HALF = 6
RED_THIRD = 7
AMBER = 9
AMBER_HALF = 10
AMBER_THIRD = 11
GREEN = 21
GREEN_HALF = 22
GREEN_THIRD = 23
YELLOW = 13
YELLOW_HALF = 14
YELLOW_THIRD = 15
MINT = 29
MINT_HALF = 30
MINT_THIRD = 31
LIGHTBLUE = 37
LIGHTBLUE_HALF = 38
LIGHTBLUE_THIRD = 39
BLUE = 45
BLUE_HALF = 46
BLUE_THIRD = 47
PINK = 53
PINK_HALF = 54
PINK_THIRD = 55
PURPLE = 48
PURPLE_HALF = 49
PURPLE_THIRD = 50

RGB_CODES = {0: "#000000"}

curr_colors = [[BLACK for y in range(9)] for x in range(9)]
effect_colors = [[BLACK for y in range(9)] for x in range(9)]

import lp_events, scripts

lp_object = None

def init(lp_object_in):
    global lp_object
    lp_object = lp_object_in


def setXY(x, y, color):
    curr_colors[x][y] = color

def effectXY(x, y, color):
    effect_colors[x][y] = color

def getXY(x, y):
    return curr_colors[x][y]

def update():
    for x in range(9):
        for y in range(9):
            set_color = None
            if (lp_events.pressed[x][y]) and (scripts.threads[x][y] != None):
                if scripts.threads[x][y].is_alive():
                    set_color = scripts.COLOR_PRIMED
                else:
                    set_color = effect_colors[x][y]
            elif scripts.threads[x][y] != None:
                if scripts.threads[x][y].is_alive():
                    set_color = effect_colors[x][y]
                else:
                    if (x, y) in [l[1:] for l in scripts.to_run]:
                        set_color = scripts.COLOR_PRIMED
                    else:
                        set_color = curr_colors[x][y]
            elif (x, y) in [l[1:] for l in scripts.to_run]:
                set_color = scripts.COLOR_PRIMED
            else:
                set_color = curr_colors[x][y]
            lp_object.LedCtrlXYByCode(x, y, set_color)

update_bindable = lambda x, y : update()

