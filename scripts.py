import threading, webbrowser
from time import sleep
from functools import partial
import lp_events, lp_colors, keyboard, sound

COLOR_PRIMED = lp_colors.RED

import files

VALID_COMMANDS = ["STRING", "DELAY", "TAP", "PRESS", "RELEASE", "SP_TAP", "SP_PRESS", "SP_RELEASE", "WEB", "WEB_NEW", "SOUND"]
DELAY_EXIT_CHECK = 0.25

threads = [[None for y in range(9)] for x in range(9)]
running = False
to_run = []
text = [["" for y in range(9)] for x in range(9)]
kill = [[False for y in range(9)] for x in range(9)]

def schedule_script(script_in, x, y):
    global threads
    global to_run

    coords = "(" + str(x) + ", " + str(y) + ")"

    if threads[x][y] != None:
        if threads[x][y].is_alive():
            print("[scripts] " + coords + " Script already running, killing script....")
            kill[x][y] = True
            return

    if (x, y) in [l[1:] for l in to_run]:
        print("[scripts] " + coords + " Script already scheduled, unscheduling...")
        indexes = [i for i, v in enumerate(to_run) if ((v[1] == x) and (v[2] == y))]
        for index in indexes[::-1]:
            temp = to_run.pop(index)
        return

    lp_colors.set_force_off(x, y, False)
    if not running:
        print("[scripts] " + coords + " No script running, starting script in background...")
        threads[x][y] = threading.Thread(target=run_script_and_run_next, args=(script_in,x,y))
        threads[x][y].start()
    else:
        print("[scripts] " + coords + " A script is already running, scheduling...")
        to_run.append((script_in, x, y))
    lp_colors.updateXY(x, y)

def run_next():
    global to_run
    if len(to_run) > 0:
        tup = to_run.pop(0)
        new_script = tup[0]
        x = tup[1]
        y = tup[2]

        schedule_script(new_script, x, y)

def run_script_and_run_next(script_in, x_in, y_in):
    global running
    global to_run
    coords = "(" + str(x_in) + ", " + str(y_in) + ")"

    run_script(script_in, x_in, y_in)
    run_next()

def run_script(script_str, x, y):
    global kill
    global running
    global exit

    lp_colors.updateXY(x, y)
    coords = "(" + str(x) + ", " + str(y) + ")"

    running = True
    script_lines = script_str.split('\n')
    print("[scripts] " + coords + " Now running script...")
    for line in script_lines:
        if kill[x][y]:
            print("[scripts] " + coords + " Recieved exit flag, script exiting...")
            kill[x][y] = False
            lp_colors.set_force_off(x, y, True)
            lp_colors.updateXY(x, y)
            running = False
            threading.Timer(lp_events.RUN_DELAY, lp_colors.updateXY, (x, y)).start()
            return
        if line.strip() == "":
            print("[scripts] " + coords + "    Empty line")
        else:
            split_line = line.split(' ')
            if split_line[0] == "STRING":
                type_string = " ".join(split_line[1:])
                print("[scripts] " + coords + "    Type out string " + type_string)
                keyboard.controller.type(type_string)
            elif split_line[0] == "DELAY":
                print("[scripts] " + coords + "    Delay for " + split_line[1] + " seconds")
                delay =float(split_line[1])
                while delay > DELAY_EXIT_CHECK:
                    sleep(DELAY_EXIT_CHECK)
                    delay -= DELAY_EXIT_CHECK
                    if kill[x][y]:
                        print("[scripts] " + coords + " Recieved exit flag, script exiting...")
                        kill[x][y] = False
                        lp_colors.set_force_off(x, y, True)
                        lp_colors.updateXY(x, y)
                        running = False
                        threading.Timer(lp_events.RUN_DELAY, lp_colors.updateXY, (x, y)).start()
                        return
                if delay > 0:
                    sleep(delay)
            elif split_line[0] == "TAP":
                if len(split_line) < 3:
                    print("[scripts] " + coords + "    Tap key " + split_line[1])
                    keyboard.tap(split_line[1])
                else:
                    print("[scripts] " + coorcds + "    Tap key " + split_line[1] + " for " + str(split_line[2]) + " seconds")
                    keyboard.tap(split_line[1], float(split_line[2]))
            elif split_line[0] == "PRESS":
                print("[scripts] " + coords + "    Press key " + split_line[1])
                keyboard.controller.press(split_line[1])
            elif split_line[0] == "RELEASE":
                print("[scripts] " + coords + " (" + str(x) + ", " + str(y) + ")    Release key " + split_line[1])
                keyboard.controller.release(split_line[1])
            elif split_line[0] == "SP_TAP":
                if keyboard.sp(split_line[1]) != None:
                    if len(split_line) < 3:
                        print("[scripts] " + coords + "    Tap special key " + split_line[1])
                        keyboard.tap(keyboard.sp(split_line[1]))
                    else:
                        print("[scripts] " + coords + "    Tap special key " + split_line[1] + " for " + str(split_line[2]) + " seconds")
                        keyboard.tap(keyboard.sp(split_line[1]), split_line[2])
                else:
                    print("[scripts] " + coords + "    Invalid special character to tap: " + split_line[1] + ", skipping...")
            elif split_line[0] == "SP_PRESS":
                if keyboard.sp(split_line[1]) != None:
                    print("[scripts] " + coords + "    Press special key " + split_line[1])
                    keyboard.controller.press(keyboard.sp(split_line[1]))
                else:
                    print("[scripts] " + coords + "    Invalid special character to press: " + split_line[1] + ", skipping...")
            elif split_line[0] == "SP_RELEASE":
                if keyboard.sp(split_line[1]) != None:
                    print("[scripts] " + coords + "    Release special key " + split_line[1])
                    keyboard.controller.release(keyboard.sp(split_line[1]))
                else:
                    print("[scripts] " + coords + "    Invalid special character to release: " + split_line[1] + ", skipping...")
            elif split_line[0] == "WEB":
                link = split_line[1]
                if "http" not in link:
                    link = "http://" + link
                print("[scripts] " + coords + "    Open website " + link + " in default browser")
                webbrowser.open(link)
            elif split_line[0] == "WEB_NEW":
                link = split_line[1]
                if "http" not in link:
                    link = "http://" + link
                print("[scripts] " + coords + "    Open website " + link + " in default browser, try to make a new window")
                webbrowser.open_new(link)
            elif split_line[0] == "SOUND":
                print("[scripts] " + coords + "    Play sound file " + split_line[1])
                sound.play(split_line[1])
            else:
                print("[scripts] " + coords + "    Invalid command: " + split_line[0] + ", skipping...")
        print("[scripts] (" + str(x) + ", " + str(y) + ") Script done running.")

        running = False
        threading.Timer(lp_events.RUN_DELAY, lp_colors.updateXY, (x, y)).start()

def bind(x, y, script_down, color):
    schedule_script_bindable = lambda a, b: schedule_script(script_down, x, y)

    lp_events.bind_func_with_colors(x, y, schedule_script_bindable, color)
    text[x][y] = script_down

def unbind(x, y):
    lp_events.unbind(x, y)
    threads[x][y] = None
    text[x][y] = ""

def unbind_all():
    global threads
    global text
    global to_run
    global kill
    lp_events.unbind_all()
    threads = [[None for y in range(9)] for x in range(9)]
    text = [["" for y in range(9)] for x in range(9)]
    to_run = []
    for x in range(9):
        for y in range(9):
            if threads[x][y] != None:
                if threads[x][y].isAlive():
                    kill[x][y] = True

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
