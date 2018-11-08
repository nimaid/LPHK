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

RGB = {BLACK: "#000",
       WHITE_THIRD: "#555",
       WHITE_HALF: "#aaa",
       WHITE: "#fff",
       RED: "#f00",
       RED_HALF: "#a00",
       RED_THIRD: "#500",
       AMBER: "#f90",
       AMBER_HALF: "#a60",
       AMBER_THIRD: "#530",
       GREEN: "#0f0",
       GREEN_HALF: "#0a0",
       GREEN_THIRD: "#050",
       YELLOW: "#ff0",
       YELLOW_HALF: "#aa0",
       YELLOW_THIRD: "#550",
       MINT: "#0ff",
       MINT_HALF: "#0aa",
       MINT_THIRD: "#055",
       LIGHTBLUE: "#0bf",
       LIGHTBLUE_HALF: "#08a",
       LIGHTBLUE_THIRD: "#045",
       BLUE: "#00f",
       BLUE_HALF: "#00a",
       BLUE_THIRD: "#005",
       PINK: "#f0f",
       PINK_HALF: "#a0a",
       PINK_THIRD: "#505",
       PURPLE: "#96f",
       PURPLE_HALF: "#64a",
       PURPLE_THIRD: "#325"}

curr_colors = [[[0,0,0] for y in range(9)] for x in range(9)]
color_modes = [["solid" for y in range(9)] for x in range(9)]

import lp_events, scripts, window

lp_object = None

def init(lp_object_in):
    global lp_object
    lp_object = lp_object_in

def setXY(x, y, color):
    if type(color) in (list, tuple):
        color = [int(min(255, max(0, c))) for c in color]
    curr_colors[x][y] = color

def getXY(x, y):
    return curr_colors[x][y]

def list_RGB_to_string(color):
    color_texts = [hex(c)[2:] for c in color]
    color_string = "#"
    for c in color_texts:
        if len(c) < 2:
            color_string += "0"
        color_string += c
    return color_string

def getXY_RGB(x, y):
    color = getXY(x, y)
    if type(color) is list:
        color_string = list_RGB_to_string(color)
        return color_string
    else:
        return RGB[color]

def updateXY(x, y):
    if window.lp_connected:
        if (x, y) != (8, 0):
            is_running = False
            if scripts.threads[x][y] != None:
                if scripts.threads[x][y].isAlive():
                    is_running = True

            is_func_key = ((y == 0) or (x == 8))

            #print("Update colors for (" + str(x) + ", " + str(y) + "), is_running = " + str(is_running))

            if is_running:
                set_color = scripts.COLOR_PRIMED
                color_modes[x][y] = "flash"
            elif (x, y) in [l[1:] for l in scripts.to_run]:
                if is_func_key:
                    set_color = scripts.COLOR_FUNC_KEYS_PRIMED
                else:
                    set_color = scripts.COLOR_PRIMED
                    color_modes[x][y] = "pulse"
            else:
                set_color = curr_colors[x][y]
                color_modes[x][y] = "solid"

            if (color_modes[x][y] == "solid") or is_func_key:
                #pulse and flash only work on main grid
                if type(set_color) is list:
                    lp_object.LedCtrlXYByRGB(x, y, [c//4 for c in set_color])
                else:
                    lp_object.LedCtrlXYByCode(x, y, set_color)
            elif color_modes[x][y] == "pulse":
                lp_object.LedCtrlPulseXYByCode(x, y, set_color)
            elif color_modes[x][y] == "flash":
                lp_object.LedCtrlXYByCode(x, y, BLACK)
                lp_object.LedCtrlFlashXYByCode(x, y, set_color)
            else:
                if type(set_color) is list:
                    lp_object.LedCtrlXYByRGB(x, y, [c//4 for c in set_color])
                else:
                    lp_object.LedCtrlXYByCode(x, y, set_color)
    else:
        print("[lp_colors] (" + str(x) + ", " + str(y) + ") Launchpad is disconnected, cannot update.")

def update_all():
    if window.lp_connected:
        for x in range(9):
            for y in range(9):
                updateXY(x, y)
    else:
        print("[lp_colors] Launchpad is disconnected, cannot update.")

def raw_clear():
    for x in range(9):
        for y in range(9):
            lp_object.LedCtrlXYByCode(x, y, BLACK)

def code_by_color_brightness(color, brightness):
    if brightness == "Full":
        if color == "White":
            return WHITE
        elif color == "Red":
            return RED
        elif color == "Orange":
            return AMBER
        elif color == "Yellow":
            return YELLOW
        elif color == "Green":
            return GREEN
        elif color == "Mint":
            return MINT
        elif color == "Light Blue":
            return LIGHTBLUE
        elif color == "Blue":
            return BLUE
        elif color == "Purple":
            return PURPLE
        elif color == "Pink":
            return PINK
    elif brightness == "Half":
        if color == "White":
            return WHITE_HALF
        elif color == "Red":
            return RED_HALF
        elif color == "Orange":
            return AMBER_HALF
        elif color == "Yellow":
            return YELLOW_HALF
        elif color == "Green":
            return GREEN_HALF
        elif color == "Mint":
            return MINT_HALF
        elif color == "Light Blue":
            return LIGHTBLUE_HALF
        elif color == "Blue":
            return BLUE_HALF
        elif color == "Purple":
            return PURPLE_HALF
        elif color == "Pink":
            return PINK_HALF
    elif brightness == "Third":
        if color == "White":
            return WHITE_THIRD
        elif color == "Red":
            return RED_THIRD
        elif color == "Orange":
            return AMBER_THIRD
        elif color == "Yellow":
            return YELLOW_THIRD
        elif color == "Green":
            return GREEN_THIRD
        elif color == "Mint":
            return MINT_THIRD
        elif color == "Light Blue":
            return LIGHTBLUE_THIRD
        elif color == "Blue":
            return BLUE_THIRD
        elif color == "Purple":
            return PURPLE_THIRD
        elif color == "Pink":
            return PINK_THIRD
    return(-1)
