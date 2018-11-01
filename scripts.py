import threading, webbrowser
from time import sleep
from functools import partial
import lp_events, lp_colors, keyboard, sound

COLOR_PRIMED = lp_colors.RED

import files

VALID_COMMANDS = ["STRING", "DELAY", "TAP", "PRESS", "RELEASE", "SP_TAP", "SP_PRESS", "SP_RELEASE", "WEB", "WEB_NEW", "SOUND"]

threads = [[None for y in range(9)] for x in range(9)]
running = False
last_run = None
to_run = []
text = [["" for y in range(9)] for x in range(9)]

def run_in_bg(func, x, y):
    global threads
    global to_run
    global last_run
    if not running:
        threads[x][y] = threading.Thread(None, func)
        threads[x][y].start()
        lp_colors.updateXY(x, y)
        last_run = (x, y)
    else:
        to_run.append((func, x, y))

def run_funcs(funcs_in):
    global running
    global to_run
    running = True
    for f in funcs_in:
        f()
    running = False
    if len(to_run) > 0:
        tup = to_run.pop(0)
        func = tup[0]
        x = tup[1]
        y = tup[2]
        run_in_bg(func, x, y)

def run_script(script_str, x, y):
    lp_colors.updateXY(x, y)
    coords = "(" + str(x) + ", " + str(y) + ")"
    if (x, y) in [l[1:] for l in to_run]:
        print("[scripts] " + coords + " Script already scheduled...")
        return
    if ((x, y) == last_run) and (running):
        print("[scripts] " + coords + " Script already running...")
        return

    script_lines = script_str.split('\n')
    funcs_to_run = []
    print("[scripts] " + coords + " Now parsing script...")
    for line in script_lines:
        if line.strip() == "":
            print("[scripts] " + coords + "    Empty line")
        else:
            split_line = line.split(' ')
            if split_line[0] == "STRING":
                type_string = " ".join(split_line[1:])
                funcs_to_run.append(partial(keyboard.controller.type, type_string))

                print_string = type_string
                print("[scripts] " + coords + "    Type out string " + print_string)
            elif split_line[0] == "DELAY":
                funcs_to_run.append(partial(sleep, float(split_line[1])))
                print("[scripts] " + coords + "    Delay for " + split_line[1] + " seconds")
            elif split_line[0] == "TAP":
                if len(split_line) < 3:
                    funcs_to_run.append(partial(keyboard.tap, split_line[1]))
                    print("[scripts] " + coords + "    Tap key " + split_line[1])
                else:
                    funcs_to_run.append(partial(keyboard.tap, split_line[1], float(split_line[2])))
                    print("[scripts] " + coords + "    Tap key " + split_line[1] + " for " + str(split_line[2]) + " seconds")
            elif split_line[0] == "PRESS":
                funcs_to_run.append(partial(keyboard.controller.press, split_line[1]))
                print("[scripts] " + coords + "    Press key " + split_line[1])
            elif split_line[0] == "RELEASE":
                funcs_to_run.append(partial(keyboard.controller.release, split_line[1]))
                print("[scripts] " + coords + " (" + str(x) + ", " + str(y) + ")    Release key " + split_line[1])
            elif split_line[0] == "SP_TAP":
                if keyboard.sp(split_line[1]) != None:
                    if len(split_line) < 3:
                        funcs_to_run.append(partial(keyboard.tap, keyboard.sp(split_line[1])))
                        print("[scripts] " + coords + "    Tap special key " + split_line[1])
                    else:
                        funcs_to_run.append(partial(keyboard.tap, keyboard.sp(split_line[1]), split_line[2]))
                        print("[scripts] " + coords + "    Tap special key " + split_line[1] + " for " + str(split_line[2]) + " seconds")
                else:
                    print("[scripts] " + coords + "    Invalid special character to tap: " + split_line[1] + ", skipping...")
            elif split_line[0] == "SP_PRESS":
                if keyboard.sp(split_line[1]) != None:
                    funcs_to_run.append(partial(keyboard.controller.press, keyboard.sp(split_line[1])))
                    print("[scripts] " + coords + "    Press special key " + split_line[1])
                else:
                    print("[scripts] " + coords + "    Invalid special character to press: " + split_line[1] + ", skipping...")
            elif split_line[0] == "SP_RELEASE":
                if keyboard.sp(split_line[1]) != None:
                    funcs_to_run.append(partial(keyboard.controller.release, keyboard.sp(split_line[1])))
                    print("[scripts] " + coords + "    Release special key " + split_line[1])
                else:
                    print("[scripts] " + coords + "    Invalid special character to release: " + split_line[1] + ", skipping...")
            elif split_line[0] == "WEB":
                link = split_line[1]
                if "http" not in link:
                    link = "http://" + link
                funcs_to_run.append(partial(webbrowser.open, link))
                print("[scripts] " + coords + "    Open website " + link + " in default browser")
            elif split_line[0] == "WEB_NEW":
                link = split_line[1]
                if "http" not in link:
                    link = "http://" + link
                funcs_to_run.append(partial(webbrowser.open_new, link))
                print("[scripts] " + coords + "    Open website " + link + " in default browser, try to make a new window")
            elif split_line[0] == "SOUND":
                funcs_to_run.append(partial(sound.play, split_line[1]))
                print("[scripts] " + coords + "    Play sound file " + split_line[1])
            else:
                print("[scripts] " + coords + "    Invalid command: " + split_line[0] + ", skipping...")
        print("[scripts] (" + str(x) + ", " + str(y) + ") Script parsed. Running in background...")
        funcs_to_run.append(partial(lp_colors.set_force_off, x, y, True))
        funcs_to_run.append(partial(lp_colors.updateXY, x, y))
        script_func = partial(run_funcs, funcs_to_run)
        run_in_bg(script_func, x, y)

def bind(x, y, script_down, color):
    script_down_bindable = lambda a, b : run_script(script_down, x, y)
    lp_events.bind_func_with_colors(x, y, script_down_bindable, color)
    text[x][y] = script_down

def unbind(x, y):
    lp_events.unbind(x, y)
    threads[x][y] = None
    text[x][y] = ""

def unbind_all():
    global threads
    global text
    global to_run
    lp_events.unbind_all()
    threads = [[None for y in range(9)] for x in range(9)]
    text = [["" for y in range(9)] for x in range(9)]
    to_run = []

def validate_script(script_str):
    if script_str == "":
        return True
    script_lines = script_str.split('\n')
    for line in script_lines:
        if line.strip() != "":
            split_line = line.split(' ')
            if split_line[0] not in VALID_COMMANDS:
                return ("Command '" + split_line[0] + "' not valid.", line)
            if split_line[0] in ["STRING", "DELAY", "TAP", "PRESS", "RELEASE", "SP_TAP", "SP_PRESS", "SP_RELEASE", "WEB", "WEB_NEW", "SOUND"]:
                if len(split_line) < 2:
                    return ("Command '" + split_line[0] + "' requires at least 1 argument.", line)
                else:
                    for token in split_line[1:]:
                        for sep in (files.ENTRY_SEPERATOR, files.BUTTON_SEPERATOR, files.NEWLINE_REPLACE):
                            if sep in token:
                                return ("You cannot use the string '" + sep + "' in any command.", line)
            if split_line[0] in ["SP_TAP", "SP_PRESS", "SP_RELEASE"]:
                if keyboard.sp(split_line[1]) == None:
                    return ("No special character named '" + split_line[1] + "'.", line)
            if split_line[0] in ["TAP", "PRESS", "RELEASE"]:
                if len(split_line[1]) > 1:
                    return ("More than 1 character supplied.", line)

    return True
