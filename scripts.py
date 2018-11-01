import multiprocessing, webbrowser
from time import sleep
import lp_events, lp_colors, keyboard, sound

COLOR_PRIMED = lp_colors.RED

import files

VALID_COMMANDS = ["STRING", "DELAY", "TAP", "PRESS", "RELEASE", "SP_TAP", "SP_PRESS", "SP_RELEASE", "WEB", "WEB_NEW", "SOUND"]

procs = [[None for y in range(9)] for x in range(9)]
running = multiprocessing.Value('I', 0)
last_run = None
not_scheduling = multiprocessing.Event()
to_run = multiprocessing.Manager().list()
text = [["" for y in range(9)] for x in range(9)]

not_scheduling.set()

def schedule_script(script, x, y):
    global procs
    global last_run
    global running
    global to_run
    global not_scheduling

    not_scheduling.wait()

    not_scheduling.clear()

    coords = "(" + str(x) + ", " + str(y) + ")"
    if (x, y) in [l[1:] for l in to_run]:
        print("[scripts] " + coords + " Script already scheduled...")
    elif ((x, y) == last_run) and (running.value == 1):
        print("[scripts] " + coords + " Script already running...")
    elif running.value == 0:
        running.value = 1
        procs[x][y] = multiprocessing.Process(target=run_script_and_run_next, args=(script, x, y))
        procs[x][y].start()
        #lp_colors.updateXY(x, y)

        last_run = (x, y)

        print("RAN")
    else:
        to_run.append((script, x, y))
        print("QUEUED")
        print(to_run)
        lp_colors.updateXY(x, y)

    not_scheduling.set()

def run_script_and_run_next(script, x, y):
    global running
    global scheduling_done
    global to_run

    print("Now running script...")
    run_script(script, x, y)
    running.value = 0
    lp_colors.set_force_off(x, y, True)
    lp_colors.updateXY(x, y)
    print(to_run)
    if len(to_run) > 0:
        print("sched next")
        tup = to_run.pop(0)
        new_script = tup[0]
        x = tup[1]
        y = tup[2]

        schedule_script(new_script, x, y)

def run_script(script_str, x, y):
    coords = "(" + str(x) + ", " + str(y) + ")"

    script_lines = script_str.split('\n')
    for line in script_lines:
        if line.strip() == "":
            print("[scripts] " + coords + "    Empty line")
        else:
            split_line = line.split(' ')
            if split_line[0] == "STRING":
                type_string = " ".join(split_line[1:])
                keyboard.controller.type(type_string)
                print("[scripts] " + coords + "    Type out string " + type_string)
            elif split_line[0] == "DELAY":
                sleep(float(split_line[1]))
                print("[scripts] " + coords + "    Delay for " + split_line[1] + " seconds")
            elif split_line[0] == "TAP":
                if len(split_line) < 3:
                    keyboard.tap(split_line[1])
                    print("[scripts] " + coords + "    Tap key " + split_line[1])
                else:
                    keyboard.tap(split_line[1], float(split_line[2]))
                    print("[scripts] " + coords + "    Tap key " + split_line[1] + " for " + str(split_line[2]) + " seconds")
            elif split_line[0] == "PRESS":
                keyboard.controller.press(split_line[1])
                print("[scripts] " + coords + "    Press key " + split_line[1])
            elif split_line[0] == "RELEASE":
                keyboard.controller.release(split_line[1])
                print("[scripts] " + coords + " (" + str(x) + ", " + str(y) + ")    Release key " + split_line[1])
            elif split_line[0] == "SP_TAP":
                if keyboard.sp(split_line[1]) != None:
                    if len(split_line) < 3:
                        keyboard.tap(keyboard.sp(split_line[1]))
                        print("[scripts] " + coords + "    Tap special key " + split_line[1])
                    else:
                        keyboard.tap(keyboard.sp(split_line[1]), split_line[2])
                        print("[scripts] " + coords + "    Tap special key " + split_line[1] + " for " + str(split_line[2]) + " seconds")
                else:
                    print("[scripts] " + coords + "    Invalid special character to tap: " + split_line[1] + ", skipping...")
            elif split_line[0] == "SP_PRESS":
                if keyboard.sp(split_line[1]) != None:
                    keyboard.controller.press(keyboard.sp(split_line[1]))
                    print("[scripts] " + coords + "    Press special key " + split_line[1])
                else:
                    print("[scripts] " + coords + "    Invalid special character to press: " + split_line[1] + ", skipping...")
            elif split_line[0] == "SP_RELEASE":
                if keyboard.sp(split_line[1]) != None:
                    keyboard.controller.release(keyboard.sp(split_line[1]))
                    print("[scripts] " + coords + "    Release special key " + split_line[1])
                else:
                    print("[scripts] " + coords + "    Invalid special character to release: " + split_line[1] + ", skipping...")
            elif split_line[0] == "WEB":
                link = split_line[1]
                if "http" not in link:
                    link = "http://" + link
                webbrowser.open(link)
                print("[scripts] " + coords + "    Open website " + link + " in default browser")
            elif split_line[0] == "WEB_NEW":
                link = split_line[1]
                if "http" not in link:
                    link = "http://" + link
                webbrowser.open_new(link)
                print("[scripts] " + coords + "    Open website " + link + " in default browser, try to make a new window")
            elif split_line[0] == "SOUND":
                sound.play(split_line[1])
                print("[scripts] " + coords + "    Play sound file " + split_line[1])
            else:
                print("[scripts] " + coords + "    Invalid command: " + split_line[0] + ", skipping...")

def bind(x, y, script_down, color):
    script_down_bindable = lambda a, b : schedule_script(script_down, x, y)
    lp_events.bind_func_with_colors(x, y, script_down_bindable, color)
    text[x][y] = script_down

def unbind(x, y):
    lp_events.unbind(x, y)
    threads[x][y] = None
    text[x][y] = ""

def unbind_all():
    global procs
    global text
    global to_run
    lp_events.unbind_all()
    procs = [[None for y in range(9)] for x in range(9)]
    text = [["" for y in range(9)] for x in range(9)]
    to_run = multiprocessing.Manager().list()

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
