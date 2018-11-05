#TODO Refactor so each command is a seperate function in a list. That way, the script parser can just do commands["COMMAND"]((args,))

import threading, webbrowser
from time import sleep
from functools import partial
import lp_events, lp_colors, keyboard, sound, mouse

COLOR_PRIMED = lp_colors.RED
COLOR_FUNC_KEYS_PRIMED = lp_colors.AMBER
EXIT_UPDATE_DELAY = 0.1

import files

VALID_COMMANDS = ["STRING", "DELAY", "TAP", "PRESS", "RELEASE", "SP_TAP", "SP_PRESS", "SP_RELEASE", "WEB", "WEB_NEW", "SOUND", "WAIT_UNPRESSED", "M_MOVE", "M_SET", "M_PRESS", "M_RELEASE", "M_SCROLL", "M_TAP", "M_LINE"]
DELAY_EXIT_CHECK = 0.025

threads = [[None for y in range(9)] for x in range(9)]
running = False
to_run = []
text = [["" for y in range(9)] for x in range(9)]

def schedule_script(script_in, x, y):
    global threads
    global to_run
    global running
    coords = "(" + str(x) + ", " + str(y) + ")"

    if threads[x][y] != None:
        if threads[x][y].is_alive():
            print("[scripts] " + coords + " Script already running, killing script....")
            threads[x][y].kill.set()
            return

    if (x, y) in [l[1:] for l in to_run]:
        print("[scripts] " + coords + " Script already scheduled, unscheduling...")
        indexes = [i for i, v in enumerate(to_run) if ((v[1] == x) and (v[2] == y))]
        for index in indexes[::-1]:
            temp = to_run.pop(index)
        return

    if script_in.split("\n")[0].split(" ")[0] == "@ASYNC":
        print("[scripts] " + coords + " Starting asynchronous script in background...")
        threads[x][y] = threading.Thread(target=run_script, args=(script_in,x,y))
        threads[x][y].kill = threading.Event()
        threads[x][y].start()
    elif not running:
        print("[scripts] " + coords + " No script running, starting script in background...")
        threads[x][y] = threading.Thread(target=run_script_and_run_next, args=(script_in,x,y))
        threads[x][y].kill = threading.Event()
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
    global running
    global exit

    lp_colors.updateXY(x, y)
    coords = "(" + str(x) + ", " + str(y) + ")"

    script_lines = script_str.split("\n")

    async = False
    if script_lines[0].split(" ")[0] == "@ASYNC":
        async = True
        temp = script_lines.pop(0)
    else:
        running = True

    print("[scripts] " + coords + " Now running script...")
    for line in script_lines:
        if threads[x][y].kill.is_set():
            print("[scripts] " + coords + " Recieved exit flag, script exiting...")
            threads[x][y].kill.clear()
            if not async:
                running = False
            threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
            return
        line = line.strip()
        if line == "":
            print("[scripts] " + coords + "    Empty line")
        elif line[0] == "-":
            print("[scripts] " + coords + "    Comment " + line[1:])
        else:
            split_line = line.split(" ")
            if split_line[0] == "STRING":
                type_string = " ".join(split_line[1:])
                print("[scripts] " + coords + "    Type out string " + type_string)
                keyboard.controller.type(type_string)
            elif split_line[0] == "DELAY":
                delay = None
                try:
                    delay =float(split_line[1])
                except:
                    print("[scripts] " + coords + "     Invalid time to delay, skipping...")

                if delay != None:
                    print("[scripts] " + coords + "    Delay for " + split_line[1] + " seconds")
                    while delay > DELAY_EXIT_CHECK:
                        sleep(DELAY_EXIT_CHECK)
                        delay -= DELAY_EXIT_CHECK
                        if threads[x][y].kill.is_set():
                            print("[scripts] " + coords + " Recieved exit flag, script exiting...")
                            threads[x][y].kill.clear()
                            if not async:
                                running = False
                            threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
                            return
                    if delay > 0:
                        sleep(delay)
            elif split_line[0] == "TAP":
                if len(split_line) <= 2:
                    print("[scripts] " + coords + "    Tap key " + split_line[1])
                    keyboard.tap(split_line[1])
                elif len(split_line) <= 3:
                    taps = None
                    try:
                        taps = int(split_line[2])
                    except:
                        print("[scripts] " + coords + "     Invalid number of times to tap, skipping...")

                    if (taps != None):
                        print("[scripts] " + coords + "    Tap key " + split_line[1] + " " + split_line[2] + " times")

                        for tap in range(taps):
                            if threads[x][y].kill.is_set():
                                print("[scripts] " + coords + " Recieved exit flag, script exiting...")
                                threads[x][y].kill.clear()
                                if not async:
                                    running = False
                                keyboard.release(split_line[1])
                                threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
                                return
                            keyboard.tap(split_line[1])
                else:
                    taps = None
                    try:
                        taps = int(split_line[2])
                    except:
                        print("[scripts] " + coords + "     Invalid number of times to tap, skipping...")
                    delay = None
                    try:
                        delay =float(split_line[3])
                    except:
                        print("[scripts] " + coords + "     Invalid time to tap, skipping...")

                    if (taps != None) and (delay != None):
                        print("[scripts] " + coords + "    Tap key " + split_line[1] + " " + split_line[2] + " times for " + str(split_line[3]) + " seconds each")
                        for tap in range(taps):
                            temp_delay = delay
                            if threads[x][y].kill.is_set():
                                print("[scripts] " + coords + " Recieved exit flag, script exiting...")
                                threads[x][y].kill.clear()
                                if not async:
                                    running = False
                                keyboard.release(split_line[1])
                                threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
                                return

                            keyboard.press(split_line[1])
                            while temp_delay > DELAY_EXIT_CHECK:
                                sleep(DELAY_EXIT_CHECK)
                                temp_delay -= DELAY_EXIT_CHECK
                                if threads[x][y].kill.is_set():
                                    print("[scripts] " + coords + " Recieved exit flag, script exiting...")
                                    threads[x][y].kill.clear()
                                    if not async:
                                        running = False
                                    keyboard.release(split_line[1])
                                    threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
                                    return
                            if temp_delay > 0:
                                sleep(temp_delay)
                            keyboard.release(split_line[1])
            elif split_line[0] == "PRESS":
                print("[scripts] " + coords + "    Press key " + split_line[1])
                keyboard.press(split_line[1])
            elif split_line[0] == "RELEASE":
                print("[scripts] " + coords + "    Release key " + split_line[1])
                keyboard.release(split_line[1])
            elif split_line[0] == "SP_TAP":
                if keyboard.sp(split_line[1]) != None:
                    key = keyboard.sp(split_line[1])
                    if len(split_line) <= 2:
                        print("[scripts] " + coords + "    Tap special key " + split_line[1])
                        keyboard.tap(key)
                    elif len(split_line) <= 3:
                        taps = None
                        try:
                            taps = int(split_line[2])
                        except:
                            print("[scripts] " + coords + "     Invalid number of times to tap, skipping...")

                        if (taps != None):
                            print("[scripts] " + coords + "    Tap special key " + split_line[1] + " " + split_line[2] + " times")

                            for tap in range(taps):
                                if threads[x][y].kill.is_set():
                                    print("[scripts] " + coords + " Recieved exit flag, script exiting...")
                                    threads[x][y].kill.clear()
                                    if not async:
                                        running = False
                                    keyboard.release(key)
                                    threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
                                    return
                                keyboard.tap(key)
                    else:
                        taps = None
                        try:
                            taps = int(split_line[2])
                        except:
                            print("[scripts] " + coords + "     Invalid number of times to tap, skipping...")
                        delay = None
                        try:
                            delay =float(split_line[3])
                        except:
                            print("[scripts] " + coords + "     Invalid time to tap, skipping...")

                        if (taps != None) and (delay != None):
                            print("[scripts] " + coords + "    Tap special key " + split_line[1] + " " + split_line[2] + " times for " + str(split_line[3]) + " seconds each")
                            for tap in range(taps):
                                temp_delay = delay
                                if threads[x][y].kill.is_set():
                                    print("[scripts] " + coords + " Recieved exit flag, script exiting...")
                                    threads[x][y].kill.clear()
                                    if not async:
                                        running = False
                                    keyboard.release(key)
                                    threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
                                    return

                                keyboard.press(key)
                                while temp_delay > DELAY_EXIT_CHECK:
                                    sleep(DELAY_EXIT_CHECK)
                                    temp_delay -= DELAY_EXIT_CHECK
                                    if threads[x][y].kill.is_set():
                                        print("[scripts] " + coords + " Recieved exit flag, script exiting...")
                                        threads[x][y].kill.clear()
                                        if not async:
                                            running = False
                                        keyboard.release(key)
                                        threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
                                        return
                                if temp_delay > 0:
                                    sleep(temp_delay)
                                keyboard.release(key)
                else:
                    print("[scripts] " + coords + "    Invalid special character to tap: " + split_line[1] + ", skipping...")
            elif split_line[0] == "SP_PRESS":
                if keyboard.sp(split_line[1]) != None:
                    print("[scripts] " + coords + "    Press special key " + split_line[1])
                    keyboard.press(keyboard.sp(split_line[1]))
                else:
                    print("[scripts] " + coords + "    Invalid special character to press: " + split_line[1] + ", skipping...")
            elif split_line[0] == "SP_RELEASE":
                if keyboard.sp(split_line[1]) != None:
                    print("[scripts] " + coords + "    Release special key " + split_line[1])
                    keyboard.release(keyboard.sp(split_line[1]))
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
                if len(split_line) > 2:
                    print("[scripts] " + coords + "    Play sound file " + split_line[1] + " at volume " + str(split_line[2]))
                    sound.play(split_line[1], float(split_line[2]))
                else:
                    print("[scripts] " + coords + "    Play sound file " + split_line[1])
                    sound.play(split_line[1])
            elif split_line[0] == "WAIT_UNPRESSED":
                print("[scripts] " + coords + "    Wait for script key to be unpressed")
                while lp_events.pressed[x][y]:
                    sleep(DELAY_EXIT_CHECK)
                    if threads[x][y].kill.is_set():
                        print("[scripts] " + coords + " Recieved exit flag, script exiting...")
                        threads[x][y].kill.clear()
                        if not async:
                            running = False
                        threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
                        return
            elif split_line[0] == "M_MOVE":
                if len(split_line) >= 3:
                    print("[scripts] " + coords + "    Relative mouse movement (" + split_line[1] + ", " + str(split_line[2]) + ")")
                    mouse.moveXY(float(split_line[1]), float(split_line[2]))
                else:
                    print("[scripts] " + coords + "    Both X and Y are required for mouse movement, skipping...")
            elif split_line[0] == "M_SET":
                if len(split_line) >= 3:
                    print("[scripts] " + coords + "    Set mouse position to (" + split_line[1] + ", " + str(split_line[2]) + ")")
                    mouse.setXY(float(split_line[1]), float(split_line[2]))
                else:
                    print("[scripts] " + coords + "    Both X and Y are required for mouse positioning, skipping...")
            elif split_line[0] == "M_PRESS":
                print("[scripts] " + coords + "    Press mouse button " + split_line[1])
                mouse.press(split_line[1])
            elif split_line[0] == "M_RELEASE":
                print("[scripts] " + coords + "    Release mouse button " + split_line[1])
                mouse.release(split_line[1])
            elif split_line[0] == "M_SCROLL":
                if len(split_line) > 2:
                    print("[scripts] " + coords + "    Scroll (" + split_line[1] + ", " + split_line[2] + ")")
                    mouse.scroll(float(split_line[2]), float(split_line[1]))
                else:
                    print("[scripts] " + coords + "    Scroll " + split_line[1])
                    mouse.scroll(0, float(split_line[1]))
            elif split_line[0] == "M_TAP":
                if len(split_line) <= 2:
                    print("[scripts] " + coords + "    Tap mouse button " + split_line[1])
                    mouse.click(split_line[1])
                elif len(split_line) <= 3:
                    taps = None
                    try:
                        taps = int(split_line[2])
                    except:
                        print("[scripts] " + coords + "     Invalid number of times to tap, skipping...")

                    if (taps != None):
                        print("[scripts] " + coords + "    Tap mouse button " + split_line[1] + " " + split_line[2] + " times")
                        mouse.click(split_line[1], taps)
                else:
                    taps = None
                    try:
                        taps = int(split_line[2])
                    except:
                        print("[scripts] " + coords + "     Invalid number of times to tap, skipping...")
                    delay = None
                    try:
                        delay =float(split_line[3])
                    except:
                        print("[scripts] " + coords + "     Invalid time to tap, skipping...")

                    if (taps != None) and (delay != None):
                        print("[scripts] " + coords + "    Tap mouse button " + split_line[1] + " " + split_line[2] + " times for " + str(split_line[3]) + " seconds each")
                        for tap in range(taps):
                            temp_delay = delay
                            if threads[x][y].kill.is_set():
                                print("[scripts] " + coords + " Recieved exit flag, script exiting...")
                                threads[x][y].kill.clear()
                                if not async:
                                    running = False
                                mouse.release(split_line[1])
                                threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
                                return

                            mouse.press(split_line[1])
                            while temp_delay > DELAY_EXIT_CHECK:
                                sleep(DELAY_EXIT_CHECK)
                                temp_delay -= DELAY_EXIT_CHECK
                                if threads[x][y].kill.is_set():
                                    print("[scripts] " + coords + " Recieved exit flag, script exiting...")
                                    threads[x][y].kill.clear()
                                    if not async:
                                        running = False
                                    mouse.release(split_line[1])
                                    threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
                                    return
                            if temp_delay > 0:
                                sleep(temp_delay)
                            mouse.release(split_line[1])
            elif split_line[0] == "M_LINE":
                x1 = int(split_line[1])
                y1 = int(split_line[2])
                x2 = int(split_line[3])
                y2 = int(split_line[4])

                delay = None
                if len(split_line) > 5:
                    delay = float(split_line[5]) / 1000.0

                skip = 1
                if len(split_line) > 6:
                    skip = int(split_line[6])

                if (delay == None) or (delay <= 0):
                    print("[scripts] " + coords + "    Mouse line from (" + split_line[1] + ", " + split_line[2] + ") to (" + split_line[3] + ", " + split_line[4] + ")")
                else:
                    print("[scripts] " + coords + "    Mouse line from (" + split_line[1] + ", " + split_line[2] + ") to (" + split_line[3] + ", " + split_line[4] + ") by " + str(skip) + " pixels per step and wait " + split_line[5] + " milliseconds between each step")

                points = mouse.line_coords(x1, y1, x2, y2)
                for x_M, y_M in points[::skip]:
                    if threads[x][y].kill.is_set():
                        print("[scripts] " + coords + " Recieved exit flag, script exiting...")
                        threads[x][y].kill.clear()
                        if not async:
                            running = False
                        threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
                        return
                    mouse.setXY(x_M, y_M)
                    if (delay != None) and (delay > 0):
                        temp_delay = delay
                        while temp_delay > DELAY_EXIT_CHECK:
                            sleep(DELAY_EXIT_CHECK)
                            temp_delay -= DELAY_EXIT_CHECK
                            if threads[x][y].kill.is_set():
                                print("[scripts] " + coords + " Recieved exit flag, script exiting...")
                                threads[x][y].kill.clear()
                                if not async:
                                    running = False
                                threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
                                return
                        if temp_delay > 0:
                            sleep(temp_delay)
            else:
                print("[scripts] " + coords + "    Invalid command: " + split_line[0] + ", skipping...")
    print("[scripts] (" + str(x) + ", " + str(y) + ") Script done running.")

    if not async:
        running = False
    threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()

def bind(x, y, script_down, color):
    global to_run
    if (x, y) in [l[1:] for l in to_run]:
        indexes = [i for i, v in enumerate(to_run) if ((v[1] == x) and (v[2] == y))]
        for index in indexes[::-1]:
            temp = to_run.pop(index)
        return

    schedule_script_bindable = lambda a, b: schedule_script(script_down, x, y)

    lp_events.bind_func_with_colors(x, y, schedule_script_bindable, color)
    text[x][y] = script_down

def unbind(x, y):
    global to_run
    lp_events.unbind(x, y)
    text[x][y] = ""
    if (x, y) in [l[1:] for l in to_run]:
        indexes = [i for i, v in enumerate(to_run) if ((v[1] == x) and (v[2] == y))]
        for index in indexes[::-1]:
            temp = to_run.pop(index)
        return
    if threads[x][y] != None:
        threads[x][y].kill.set()

def unbind_all():
    global threads
    global text
    global to_run
    lp_events.unbind_all()
    text = [["" for y in range(9)] for x in range(9)]
    to_run = []
    for x in range(9):
        for y in range(9):
            if threads[x][y] != None:
                if threads[x][y].isAlive():
                    threads[x][y].kill.set()

def validate_script(script_str):
    if script_str == "":
        return True
    script_lines = script_str.split('\n')

    first_line_split = script_lines[0].split(" ")

    if first_line_split[0] == "@ASYNC":
        if len(first_line_split) > 1:
            return ("@ASYNC takes no arguments.", script_lines[0])
        temp = script_lines.pop(0)

    for line in script_lines:
        for sep in (files.ENTRY_SEPERATOR, files.BUTTON_SEPERATOR, files.NEWLINE_REPLACE):
            if sep in line:
                return ("You cannot use the string '" + sep + "' in any script.", line)
        line = line.strip()
        if line != "":
            if line[0] != "-":
                split_line = line.split(' ')
                if split_line[0] not in VALID_COMMANDS:
                    if split_line[0] == "@ASYNC":
                        return ("@ASYNC is a header and can only be used on the first line.", line)
                    else:
                        return ("Command '" + split_line[0] + "' not valid.", line)
                if split_line[0] in ["STRING", "DELAY", "TAP", "PRESS", "RELEASE", "SP_TAP", "SP_PRESS", "SP_RELEASE", "WEB", "WEB_NEW", "SOUND", "M_MOVE", "M_SET", "M_PRESS", "M_RELEASE", "M_SCROLL", "M_TAP"]:
                    if len(split_line) < 2:
                        return ("Too few arguments for command '" + split_line[0] + "'.", line)
                if split_line[0] in ["WAIT_UNPRESSED"]:
                    if len(split_line) > 1:
                        return ("Too many arguments for command '" + split_line[0] + "'.", line)
                if split_line[0] in ["DELAY", "WEB", "WEB_NEW", "PRESS", "RELEASE", "SP_PRESS", "SP_RELEASE", "M_PRESS", "M_RELEASE"]:
                    if len(split_line) > 2:
                        return ("Too many arguments for command '" + split_line[0] + "'.", line)
                if split_line[0] in ["SOUND", "M_MOVE", "M_SCROLL", "M_SET"]:
                    if len(split_line) > 3:
                        return ("Too many arguments for command '" + split_line[0] + "'.", line)
                if split_line[0] in ["TAP", "SP_TAP", "M_TAP"]:
                    if len(split_line) > 4:
                        return ("Too many arguments for command '" + split_line[0] + "'.", line)
                if split_line[0] in ["M_LINE"]:
                    if len(split_line) > 7:
                        return ("Too many arguments for command '" + split_line[0] + "'.", line)
                if split_line[0] in ["SP_TAP", "SP_PRESS", "SP_RELEASE"]:
                    if keyboard.sp(split_line[1]) == None:
                        return ("No special character named '" + split_line[1] + "'.", line)
                if split_line[0] in ["TAP", "PRESS", "RELEASE"]:
                    if len(split_line[1]) > 1:
                        return ("More than 1 character supplied.", line)
                if split_line[0] == "DELAY":
                    try:
                        temp = float(split_line[1])
                    except:
                        return ("Delay time '" + split_line[1] + "' not valid.", line)
                if split_line[0] in ["TAP", "SP_TAP", "M_TAP"]:
                    func_name = "Tap"
                    if split_line[0] == "SP_TAP":
                        func_name = "Special tap"
                    if split_line[0] == "M_TAP":
                        func_name = "Mouse tap"
                    if len(split_line) > 3:
                        try:
                            temp = float(split_line[3])
                        except:
                            return (func_name + " wait time '" + split_line[3] + "' not valid.", line)
                    if len(split_line) > 2:
                        try:
                            temp = int(split_line[2])
                        except:
                            return (func_name + " repetitions '" + split_line[2] + "' not valid.", line)

                if split_line[0] == "WAIT_UNPRESSED":
                    if len(split_line) > 1:
                        return ("'WAIT_UNPRESSED' takes no arguments.", line)
                if split_line[0] == "SOUND":
                    if len(split_line) > 2:
                        try:
                            vol = float(float(split_line[2]) / 100.0)
                            if (vol < 0.0) or (vol > 1.0):
                                return ("'SOUND' volume must be between 0 and 100.", line)
                        except:
                            return ("'SOUND' volume " + split_line[2] + " not valid.", line)
                if split_line[0] == "M_MOVE":
                    if len(split_line) < 3:
                        return ("'M_MOVE' requires both an X and a Y movement value.", line)
                    try:
                        temp = int(split_line[1])
                    except:
                        return ("'M_MOVE' X value '" + split_line[1] + "' not valid.", line)
                    try:
                        temp = int(split_line[2])
                    except:
                        return ("'M_MOVE' Y value '" + split_line[2] + "' not valid.", line)

                if split_line[0] == "M_SET":
                    if len(split_line) < 3:
                        return ("'M_SET' requires both an X and a Y value.", line)
                    try:
                        temp = int(split_line[1])
                    except:
                        return ("'M_SET' X value '" + split_line[1] + "' not valid.", line)
                    try:
                        temp = int(split_line[2])
                    except:
                        return ("'M_SET' Y value '" + split_line[2] + "' not valid.", line)
                if split_line[0] in ["M_PRESS", "M_RELEASE", "M_TAP"]:
                    if split_line[1] not in ["left", "middle", "right"]:
                        return ("Invalid mouse button '" + split_line[1] + "'.", line)
                if split_line[0] == "M_SCROLL":
                    try:
                        temp = float(split_line[1])
                    except:
                        return ("Invalid scroll amount '" + split_line[1] + "'.", line)

                    if len(split_line) > 2:
                        try:
                            temp = float(split_line[2])
                        except:
                            return ("Invalid scroll amount '" + split_line[2] + "'.", line)
                if split_line[0] == "M_LINE":
                    if len(split_line) < 4:
                        return ("'M_LINE' requires at least X1, Y1, X2, and Y2 arguments.", line)
                    try:
                        temp = int(split_line[1])
                    except:
                        return ("'M_LINE' X1 value '" + split_line[1] + "' not valid.", line)
                    try:
                        temp = int(split_line[2])
                    except:
                        return ("'M_LINE' Y1 value '" + split_line[2] + "' not valid.", line)
                    try:
                        temp = int(split_line[3])
                    except:
                        return ("'M_LINE' X2 value '" + split_line[3] + "' not valid.", line)
                    try:
                        temp = int(split_line[4])
                    except:
                        return ("'M_LINE' Y2 value '" + split_line[4] + "' not valid.", line)
                    if len(split_line) >= 6:
                        try:
                            temp = float(split_line[5])
                        except:
                            return ("'M_LINE' wait value '" + split_line[5] + "' not valid.", line)
                    if len(split_line) >= 7:
                        try:
                            temp = int(split_line[6])
                            if temp == 0:
                                return ("'M_LINE' skip value cannot be zero.", line)
                        except:
                            return ("'M_LINE' skip value '" + split_line[6] + "' not valid.", line)

    return True
