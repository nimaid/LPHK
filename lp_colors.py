curr_colors = [[[0,0,0] for y in range(9)] for x in range(9)]
color_modes = [["solid" for y in range(9)] for x in range(9)]

import lp_events, scripts, window
import colorsys
from constants import *

lp_object = None # another suspiciously non-threadsafe way of doing things :-(

def init(lp_object_in):
    global lp_object
    lp_object = lp_object_in   # this function just stores the object in a global variable (what?!)

def code_to_RGB(code):
    # Used to convert old layouts to the new format only
    RGB = {0: "#000",
           1: "#555",
           2: "#aaa",
           3: "#fff",
           5: "#f00",
           6: "#a00",
           7: "#500",
           9: "#f90",
           10: "#a60",
           11: "#530",
           21: "#0f0",
           22: "#0a0",
           23: "#050",
           13: "#ff0",
           14: "#aa0",
           15: "#550",
           29: "#0ff",
           30: "#0aa",
           31: "#055",
           37: "#0bf",
           38: "#08a",
           39: "#045",
           45: "#00f",
           46: "#00a",
           47: "#005",
           53: "#f0f",
           54: "#a0a",
           55: "#505",
           48: "#96f",
           49: "#64a",
           50: "#325"}
    rgb = []
    for c in range(3):
        val = RGB[code][c + 1]
        rgb.append(int(val + val, 16))
    return rgb

def RGB_to_RG(rgb):
    if rgb[2] != 0:
        color = list(colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2]))
        color[0] = color[0] * (106/330)
        color = list(colorsys.hsv_to_rgb(color[0], color[1], color[2]))
        color = [round(x) for x in color]
        for x in range(2):
            color[x] = round(color[x])
        return color[:2] + [0]
    else:
        return rgb

# Set the colour of a button (but not the current colour of the button!)
def setXY(x, y, color):
    curr_colors[x][y] = color

# Get the currently recorded colour of the button (not necessarily it's current colour!)
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
    color_string = list_RGB_to_string(color)
    return color_string

def luminance(r, g, b):
    return ((0.299 * r) + (0.587 * g) + (0.114 * b)) / 255.0

# update the colour of a button
def updateXY(x, y):
    if window.lp_connected:                                     # must be connected to a launchpad
        btn = scripts.buttons[x][y]                             # get the button
        if (x, y) != (8, 0):                                    # this is the "missing" button in the top right corner
            is_running = False                                  # assume it's not running
            if btn.thread != None:
                if btn.thread.isAlive():
                    is_running = True                           # unless it is

            is_func_key = ((y == 0) or (x == 8))                # top row or right column

            #print("Update colors for (" + str(x) + ", " + str(y) + "), is_running = " + str(is_running))

            if is_running:                                      # if the button is running
                set_color = scripts.COLOR_PRIMED                # set the desired colour
                color_modes[x][y] = "flash"                     # and mode
            elif (x, y) in [l[1:] for l in scripts.to_run]:     # is it waiting to run?
                if is_func_key:
                    set_color = scripts.COLOR_FUNC_KEYS_PRIMED  # function keys have one colour
                else:
                    set_color = scripts.COLOR_PRIMED            # and other keys have another
                    color_modes[x][y] = "pulse"
            else:
                set_color = curr_colors[x][y]                   # this button is not running (or not even asigned)
                color_modes[x][y] = "solid"                     # set the mode alone

            if window.lp_mode == LP_MK1:                         # how to actually set the colours of Mk:1 launchpads
                if type(set_color) is int:
                    set_color = code_to_RGB(set_color)
                lp_object.LedCtrlXY(x, y, set_color[0]//64, set_color[1]//64)
            else:                                               # setting colours for all other launchpads
                if (color_modes[x][y] == "solid") or is_func_key:
                    #pulse and flash only work on main grid
                    if type(set_color) is list:
                        lp_object.LedCtrlXYByRGB(x, y, [c//4 for c in set_color])
                    else:
                        lp_object.LedCtrlXYByCode(x, y, set_color)
                elif color_modes[x][y] == "pulse":
                    lp_object.LedCtrlPulseXYByCode(x, y, set_color)
                elif color_modes[x][y] == "flash":
                    lp_object.LedCtrlXYByCode(x, y, 0)
                    lp_object.LedCtrlFlashXYByCode(x, y, set_color)
                else:
                    if type(set_color) is list:
                        lp_object.LedCtrlXYByRGB(x, y, [c//4 for c in set_color])
                    else:
                        lp_object.LedCtrlXYByCode(x, y, set_color)
    else:
        print("[lp_colors] (" + str(x) + ", " + str(y) + ") Launchpad is disconnected, cannot update.")

# update the colours of all buttons
def update_all():
    if window.lp_connected:
        for x in range(9):
            for y in range(9):
                updateXY(x, y)  # call this for each buttn
    else:
        print("[lp_colors] Launchpad is disconnected, cannot update.")

def raw_clear():
    for x in range(9):
        for y in range(9):
            if window.lp_mode == LP_MK1:
                lp_object.LedCtrlXY(x, y, 0, 0)
            else:
                lp_object.LedCtrlXYByCode(x, y, 0)
