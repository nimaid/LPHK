import threading, webbrowser, os, subprocess
from time import sleep
from functools import partial
import lp_events, lp_colors, kb, sound, ms

COLOR_PRIMED = 5 #red
COLOR_FUNC_KEYS_PRIMED = 9 #amber
EXIT_UPDATE_DELAY = 0.1
DELAY_EXIT_CHECK = 0.025

import files

VALID_COMMANDS = ["@ASYNC", "@SIMPLE", "@LOAD_LAYOUT", "STRING", "DELAY", "TAP", "PRESS", "RELEASE", "WEB", "WEB_NEW", "CODE", "SOUND", "SOUND_STOP", "WAIT_UNPRESSED", "M_MOVE", "M_SET", "M_SCROLL", "M_LINE", "M_LINE_MOVE", "M_LINE_SET", "LABEL", "IF_PRESSED_GOTO_LABEL", "IF_UNPRESSED_GOTO_LABEL", "GOTO_LABEL", "REPEAT_LABEL", "IF_PRESSED_REPEAT_LABEL", "IF_UNPRESSED_REPEAT_LABEL", "M_STORE", "M_RECALL", "M_RECALL_LINE", "OPEN", "RELEASE_ALL", "RESET_REPEATS"]
ASYNC_HEADERS = ["@ASYNC", "@SIMPLE"]

threads = [[None for y in range(9)] for x in range(9)]
running = False
to_run = []
text = [["" for y in range(9)] for x in range(9)]

def check_kill(x, y, is_async, killfunc=None):
    coords = "(" + str(x) + ", " + str(y) + ")"

    if threads[x][y].kill.is_set():
        print("[scripts] " + coords + " Recieved exit flag, script exiting...")
        threads[x][y].kill.clear()
        if not is_async:
            running = False
        if killfunc:
            killfunc()
        threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
        return True
    else:
        return False

def safe_sleep(time, x, y, is_async, endfunc=None):
    while time > DELAY_EXIT_CHECK:
        sleep(DELAY_EXIT_CHECK)
        time -= DELAY_EXIT_CHECK
        if check_kill(x, y, is_async, endfunc):
            return False
    if time > 0:
        sleep(time)
    if endfunc:
        endfunc()
    return True

def is_ignorable_line(line):
    line = line.strip()
    if line != "":
        if line[0] == "-":
            return True
        else:
            return False
    else:
        return True

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

    if script_in.split("\n")[0].split(" ")[0] in ASYNC_HEADERS:
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


# noinspection PyRedundantParentheses
def run_script(script_str, x, y):
    global running
    global exit

    lp_colors.updateXY(x, y)
    coords = "(" + str(x) + ", " + str(y) + ")"

    print("[scripts] " + coords + " Now running script...")

    script_lines = script_str.split("\n")

    script_lines = [i.strip() for i in script_lines]

    #remove comments
    if len(script_lines) > 0:
        while(is_ignorable_line(script_lines[0])):
            line = script_lines.pop(0)
            if line != "":
                print("[scripts] " + coords + "    Comment: " + line[1:])
            if len(script_lines) <= 0:
                break

    if len(script_lines) > 0:
        is_async = False
        if script_lines[0].split(" ")[0] in ASYNC_HEADERS:
            is_async = True
        else:
            running = True

        if script_lines[0].split(" ")[0] == "@ASYNC":
            temp = script_lines.pop(0)

        #parse labels
        labels = dict()
        for idx,line in enumerate(script_lines):
            split_line = line.split(" ")
            if split_line[0] == "LABEL":
                labels[split_line[1]] = idx

        #prepare repeat counter {idx:repeats_left}
        repeats = dict()
        repeats_original = dict()

        m_pos = ()

        def main_logic(idx):
            nonlocal m_pos

            if check_kill(x, y, is_async):
                return idx + 1

            line = script_lines[idx]
            if line == "":
                return idx + 1
            if line[0] == "-":
                print("[scripts] " + coords + "    Comment: " + line[1:])
            else:
                split_line = line.split(" ")
                if split_line[0] == "STRING":
                    type_string = " ".join(split_line[1:])
                    print("[scripts] " + coords + "    Type out string " + type_string)
                    kb.write(type_string)
                elif split_line[0] == "DELAY":
                    print("[scripts] " + coords + "    Delay for " + split_line[1] + " seconds")
                    delay = float(split_line[1])
                    if not safe_sleep(delay, x, y, is_async):
                        return -1
                elif split_line[0] == "TAP":
                    key = kb.sp(split_line[1])
                    releasefunc = lambda: kb.release(key)
                    if len(split_line) <= 2:
                        print("[scripts] " + coords + "    Tap key " + split_line[1])
                        kb.tap(key)
                    elif len(split_line) <= 3:
                        print("[scripts] " + coords + "    Tap key " + split_line[1] + " " + split_line[2] + " times")
                        taps = int(split_line[2])
                        for tap in range(taps):
                            if check_kill(x, y, is_async, releasefunc):
                                return idx + 1
                            kb.tap(key)
                    else:
                        print("[scripts] " + coords + "    Tap key " + split_line[1] + " " + split_line[2] + " times for " + str(split_line[3]) + " seconds each")
                        taps = int(split_line[2])
                        delay = float(split_line[3])
                        for tap in range(taps):
                            if check_kill(x, y, is_async, releasefunc):
                                return -1
                            kb.press(key)
                            if not safe_sleep(delay, x, y, is_async, releasefunc):
                                return -1
                elif split_line[0] == "PRESS":
                    print("[scripts] " + coords + "    Press key " + split_line[1])
                    key = kb.sp(split_line[1])
                    kb.press(key)
                elif split_line[0] == "RELEASE":
                    print("[scripts] " + coords + "    Release key " + split_line[1])
                    key = kb.sp(split_line[1])
                    kb.release(key)
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
                elif split_line[0] == "CODE":
                    args = " ".join(split_line[1:])
                    print("[scripts] " + coords + "    Running code: " + args)
                    try:
                        subprocess.run(args)
                    except Exception as e:
                        print("[scripts] " + coords + "    Error with running code: " + str(e))
                elif split_line[0] == "SOUND":
                    if len(split_line) > 2:
                        print("[scripts] " + coords + "    Play sound file " + split_line[1] + " at volume " + str(split_line[2]))
                        sound.play(split_line[1], float(split_line[2]))
                    else:
                        print("[scripts] " + coords + "    Play sound file " + split_line[1])
                        sound.play(split_line[1])
                elif split_line[0] == "SOUND_STOP":
                    if len(split_line) > 1:
                        delay = split_line[1]
                        print("[scripts] " + coords +
                              "    Stopping sounds with " + delay + " milliseconds fadeout time")
                        sound.fadeout(int(delay))
                    else:
                        print("[scripts] " + coords + "    Stopping sounds")
                        sound.stop()
                elif split_line[0] == "WAIT_UNPRESSED":
                    print("[scripts] " + coords + "    Wait for script key to be unpressed")
                    while lp_events.pressed[x][y]:
                        sleep(DELAY_EXIT_CHECK)
                        if check_kill(x, y, is_async):
                            return idx + 1
                elif split_line[0] == "M_STORE":
                    print("[scripts] " + coords + "    Store mouse position")
                    m_pos = ms.get_pos()
                elif split_line[0] == "M_RECALL":
                    if m_pos == tuple():
                        print("[scripts] " + coords + "    No 'M_STORE' command has been run, cannot do 'M_RECALL'")
                    else:
                        print("[scripts] " + coords + "    Recall mouse position " + str(m_pos))
                        ms.set_pos(m_pos[0], m_pos[1])
                elif split_line[0] == "M_RECALL_LINE":
                    x1, y1 = m_pos

                    delay = None
                    if len(split_line) > 1:
                        delay = float(split_line[1]) / 1000.0

                    skip = 1
                    if len(split_line) > 2:
                        skip = int(split_line[2])

                    if (delay == None) or (delay <= 0):
                        print("[scripts] " + coords + "    Recall mouse position " + str(m_pos) + " in a line by " + str(skip) + " pixels per step")
                    else:
                        print("[scripts] " + coords + "    Recall mouse position " + str(m_pos) + " in a line by " + str(skip) + " pixels per step and wait " + split_line[1] + " milliseconds between each step")

                    x_C, y_C = ms.get_pos()
                    points = ms.line_coords(x_C, y_C, x1, y1)
                    for x_M, y_M in points[::skip]:
                        if check_kill(x, y, is_async):
                            return -1
                        ms.set_pos(x_M, y_M)
                        if (delay != None) and (delay > 0):
                            if not safe_sleep(delay, x, y, is_async):
                                return -1
                elif split_line[0] == "M_MOVE":
                    if len(split_line) >= 3:
                        print("[scripts] " + coords + "    Relative mouse movement (" + split_line[1] + ", " + str(split_line[2]) + ")")
                        ms.move_to_pos(float(split_line[1]), float(split_line[2]))
                    else:
                        print("[scripts] " + coords + "    Both X and Y are required for mouse movement, skipping...")
                elif split_line[0] == "M_SET":
                    if len(split_line) >= 3:
                        print("[scripts] " + coords + "    Set mouse position to (" + split_line[1] + ", " + str(split_line[2]) + ")")
                        ms.set_pos(float(split_line[1]), float(split_line[2]))
                    else:
                        print("[scripts] " + coords + "    Both X and Y are required for mouse positioning, skipping...")
                elif split_line[0] == "M_SCROLL":
                    if len(split_line) > 2:
                        print("[scripts] " + coords + "    Scroll (" + split_line[1] + ", " + split_line[2] + ")")
                        ms.scroll(float(split_line[2]), float(split_line[1]))
                    else:
                        print("[scripts] " + coords + "    Scroll " + split_line[1])
                        ms.scroll(0, float(split_line[1]))
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
                        print("[scripts] " + coords + "    Mouse line from (" + split_line[1] + ", " + split_line[2] + ") to (" + split_line[3] + ", " + split_line[4] + ") by " + str(skip) + " pixels per step")
                    else:
                        print("[scripts] " + coords + "    Mouse line from (" + split_line[1] + ", " + split_line[2] + ") to (" + split_line[3] + ", " + split_line[4] + ") by " + str(skip) + " pixels per step and wait " + split_line[5] + " milliseconds between each step")

                    points = ms.line_coords(x1, y1, x2, y2)
                    for x_M, y_M in points[::skip]:
                        if check_kill(x, y, is_async):
                            return -1
                        ms.set_pos(x_M, y_M)
                        if (delay != None) and (delay > 0):
                            if not safe_sleep(delay, x, y, is_async):
                                return -1
                elif split_line[0] == "M_LINE_MOVE":
                    x1 = int(split_line[1])
                    y1 = int(split_line[2])

                    delay = None
                    if len(split_line) > 3:
                        delay = float(split_line[3]) / 1000.0

                    skip = 1
                    if len(split_line) > 4:
                        skip = int(split_line[4])

                    if (delay == None) or (delay <= 0):
                        print("[scripts] " + coords + "    Mouse line move relative (" + split_line[1] + ", " + split_line[2] + ") by " + str(skip) + " pixels per step")
                    else:
                        print("[scripts] " + coords + "    Mouse line move relative (" + split_line[1] + ", " + split_line[2] + ") by " + str(skip) + " pixels per step and wait " + split_line[3] + " milliseconds between each step")

                    x_C, y_C = ms.get_pos()
                    x_N, y_N = x_C + x1, y_C + y1
                    points = ms.line_coords(x_C, y_C, x_N, y_N)
                    for x_M, y_M in points[::skip]:
                        if check_kill(x, y, is_async):
                            return -1
                        ms.set_pos(x_M, y_M)
                        if (delay != None) and (delay > 0):
                            if not safe_sleep(delay, x, y, is_async):
                                return -1
                elif split_line[0] == "M_LINE_SET":
                    x1 = int(split_line[1])
                    y1 = int(split_line[2])

                    delay = None
                    if len(split_line) > 3:
                        delay = float(split_line[3]) / 1000.0

                    skip = 1
                    if len(split_line) > 4:
                        skip = int(split_line[4])

                    if (delay == None) or (delay <= 0):
                        print("[scripts] " + coords + "    Mouse line set (" + split_line[1] + ", " + split_line[2] + ") by " + str(skip) + " pixels per step")
                    else:
                        print("[scripts] " + coords + "    Mouse line set (" + split_line[1] + ", " + split_line[2] + ") by " + str(skip) + " pixels per step and wait " + split_line[3] + " milliseconds between each step")

                    x_C, y_C = ms.get_pos()
                    points = ms.line_coords(x_C, y_C, x1, y1)
                    for x_M, y_M in points[::skip]:
                        if check_kill(x, y, is_async):
                            return -1
                        ms.set_pos(x_M, y_M)
                        if (delay != None) and (delay > 0):
                            if not safe_sleep(delay, x, y, is_async):
                                return -1
                elif split_line[0] == "LABEL":
                   print("[scripts] " + coords + "    Label: " + split_line[1])
                   return idx + 1
                elif split_line[0] == "IF_PRESSED_GOTO_LABEL":
                    print("[scripts] " + coords + "    If key is pressed goto LABEL " + split_line[1])
                    if lp_events.pressed[x][y]:
                        return labels[split_line[1]]
                elif split_line[0] == "IF_UNPRESSED_GOTO_LABEL":
                    print("[scripts] " + coords + "    If key is not pressed goto LABEL " + split_line[1])
                    if not lp_events.pressed[x][y]:
                        return labels[split_line[1]]
                elif split_line[0] == "GOTO_LABEL":
                    print("[scripts] " + coords + "    Goto LABEL " + split_line[1])
                    return labels[split_line[1]]
                elif split_line[0] == "REPEAT_LABEL":
                    print("[scripts] " + coords + "    Repeat LABEL " + split_line[1] + " " + split_line[2] + " times max")
                    if idx in repeats:
                        if repeats[idx] > 0:
                            print("[scripts] " + coords + "        " + str(repeats[idx]) + " repeats left.")
                            repeats[idx] -= 1
                            return labels[split_line[1]]
                        else:
                            print("[scripts] " + coords + "        No repeats left, not repeating.")
                    else:
                        repeats[idx] = int(split_line[2])
                        repeats_original[idx] = int(split_line[2])
                        print("[scripts] " + coords + "        " + str(repeats[idx]) + " repeats left.")
                        repeats[idx] -= 1
                        return labels[split_line[1]]
                elif split_line[0] == "IF_PRESSED_REPEAT_LABEL":
                    print("[scripts] " + coords + "    If key is pressed repeat LABEL " + split_line[1] + " " + split_line[2] + " times max")
                    if lp_events.pressed[x][y]:
                        if idx in repeats:
                            if repeats[idx] > 0:
                                print("[scripts] " + coords + "        " + str(repeats[idx]) + " repeats left.")
                                repeats[idx] -= 1
                                return labels[split_line[1]]
                            else:
                                print("[scripts] " + coords + "        No repeats left, not repeating.")
                        else:
                            repeats[idx] = int(split_line[2])
                            print("[scripts] " + coords + "        " + str(repeats[idx]) + " repeats left.")
                            repeats[idx] -= 1
                            return labels[split_line[1]]
                elif split_line[0] == "IF_UNPRESSED_REPEAT_LABEL":
                    print("[scripts] " + coords + "    If key is not pressed repeat LABEL " + split_line[1] + " " + split_line[2] + " times max")
                    if not lp_events.pressed[x][y]:
                        if idx in repeats:
                            if repeats[idx] > 0:
                                print("[scripts] " + coords + "        " + str(repeats[idx]) + " repeats left.")
                                repeats[idx] -= 1
                                return labels[split_line[1]]
                            else:
                                print("[scripts] " + coords + "        No repeats left, not repeating.")
                        else:
                            repeats[idx] = int(split_line[2])
                            print("[scripts] " + coords + "        " + str(repeats[idx]) + " repeats left.")
                            repeats[idx] -= 1
                            return labels[split_line[1]]
                elif split_line[0] == "@SIMPLE":
                    print("[scripts] " + coords + "    Simple keybind: " + split_line[1])
                    #PRESS
                    key = kb.sp(split_line[1])
                    releasefunc = lambda: kb.release(key)
                    kb.press(key)
                    #WAIT_UNPRESSED
                    while lp_events.pressed[x][y]:
                        sleep(DELAY_EXIT_CHECK)
                        if check_kill(x, y, is_async, releasefunc):
                            return idx + 1
                    #RELEASE
                    kb.release(key)
                elif split_line[0] == "@LOAD_LAYOUT":
                    layout_name = " ".join(split_line[1:])
                    print("[scripts] " + coords + "    Load layout " + layout_name)
                    layout_path = os.path.join(files.LAYOUT_PATH, layout_name)
                    if not os.path.isfile(layout_path):
                        print("[scripts] " + coords + "        ERROR: Layout file does not exist.")
                        return -1
                    try:
                        layout = files.load_layout(layout_path, popups=False, save_converted=False)
                    except files.json.decoder.JSONDecodeError:
                        print("[scripts] " + coords + "        ERROR: Layout is malformated.")
                        return -1
                    if files.layout_changed_since_load:
                        files.save_lp_to_layout(files.curr_layout)
                    files.load_layout_to_lp(layout_path, popups=False, save_converted=False, preload=layout)
                elif split_line[0] == "OPEN":
                    path_name = " ".join(split_line[1:])
                    print("[scripts] " + coords + "    Open file or folder " + path_name)
                    files.open_file_folder(path_name)
                elif split_line[0] == "RELEASE_ALL":
                    print("[scripts] " + coords + "    Release all keys")
                    kb.release_all()
                elif split_line[0] == "RESET_REPEATS":
                    print("[scripts] " + coords + "    Reset all repeats")
                    for i in repeats:
                        repeats[i] = repeats_original[i]
                else:
                    print("[scripts] " + coords + "    Invalid command: " + split_line[0] + ", skipping...")
            return idx + 1
        run = True
        idx = 0
        while run:
            idx = main_logic(idx)
            if (idx < 0) or (idx >= len(script_lines)):
                run = False

        if not is_async:
            running = False
        threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()

    print("[scripts] (" + str(x) + ", " + str(y) + ") Script done running.")


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
    files.layout_changed_since_load = True

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
    files.layout_changed_since_load = True

def swap(x1, y1, x2, y2):
    global text
    color_1 = lp_colors.curr_colors[x1][y1]
    color_2 = lp_colors.curr_colors[x2][y2]

    script_1 = text[x1][y1]
    script_2 = text[x2][y2]

    unbind(x1, y1)
    if script_2 != "":
        bind(x1, y1, script_2, color_2)
    lp_colors.updateXY(x1, y1)

    unbind(x2, y2)
    if script_1 != "":
        bind(x2, y2, script_1, color_1)
    lp_colors.updateXY(x2, y2)
    files.layout_changed_since_load = True

def copy(x1, y1, x2, y2):
    global text
    color_1 = lp_colors.curr_colors[x1][y1]

    script_1 = text[x1][y1]

    unbind(x2, y2)
    if script_1 != "":
        bind(x2, y2, script_1, color_1)
    lp_colors.updateXY(x2, y2)
    files.layout_changed_since_load = True

def move(x1, y1, x2, y2):
    global text
    color_1 = lp_colors.curr_colors[x1][y1]

    script_1 = text[x1][y1]

    unbind(x1, y1)
    unbind(x2, y2)
    if script_1 != "":
        bind(x2, y2, script_1, color_1)
    lp_colors.updateXY(x2, y2)
    files.layout_changed_since_load = True

def is_bound(x, y):
    if text[x][y] == "":
        return False
    else:
        return True

def unbind_all():
    global threads
    global text
    global to_run
    lp_events.unbind_all()
    text = [["" for y in range(9)] for x in range(9)]
    to_run = []
    for x in range(9):
        for y in range(9):
            if threads[x][y] is not None:
                if threads[x][y].isAlive():
                    threads[x][y].kill.set()
    files.curr_layout = None
    files.layout_changed_since_load = False


# noinspection PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses,PyRedundantParentheses
def validate_script(script_str):
    if script_str == "":
        return True
    script_lines = script_str.split('\n')

    script_lines = [i.strip() for i in script_lines]

    if len(script_lines) > 0:
        while(is_ignorable_line(script_lines[0])):
            line = script_lines.pop(0)
            if len(script_lines) <= 0:
                return True

    first_line = script_lines[0]
    first_line_split = first_line.split(" ")

    if first_line_split[0] == "@ASYNC":
        if len(first_line_split) > 1:
            return ("@ASYNC takes no arguments.", script_lines[0])
        temp = script_lines.pop(0)

    if first_line_split[0] == "@SIMPLE":
        if len(first_line_split) < 2:
            return ("@SIMPLE requires a key to bind.", first_line)
        if len(first_line_split) > 2:
            return ("@SIMPLE only take one argument", first_line)
        if kb.sp(first_line_split[1]) == None:
            return ("No key named '" + first_line_split[1] + "'.", first_line)
        for line in script_lines[1:]:
            if line != "" and line[0] != "-":
                return ("When @SIMPLE is used, scripts can only contain comments.", line)

    if first_line_split[0] == "@LOAD_LAYOUT":
        for line in script_lines[1:]:
            if line != "" and line[0] != "-":
                return ("When @LOAD_LAYOUT is used, scripts can only contain comments.", line)
        if len(first_line_split) < 2:
            return ("No layout filename provided.", first_line)
        layout_path = os.path.join(files.LAYOUT_PATH, " ".join(first_line_split[1:]))
        if not os.path.isfile(layout_path):
            return ("'" + layout_path + "' does not exist!", first_line)

        try:
            layout = files.load_layout(layout_path, popups=False, save_converted=False, printing=False)
        except:
            return ("Layout '" + layout_path + "' is malformatted.", first_line)

    #parse labels
    labels = []
    for line in script_lines:
        split_line = line.split(" ")
        if split_line[0] == "LABEL":
            if len(split_line) != 2:
                return ("'" + split_line[0] + "' takes exactly 1 argument.", line)
            if split_line[1] in labels:
                return ("Label '" + split_line[1] + "' defined multiple times.", line)
            else:
                labels.append(split_line[1])

    for idx, line in enumerate(script_lines):
        if line != "":
            if line[0] != "-":
                split_line = line.split(' ')
                if split_line[0][0] == "@":
                    if idx != 0:
                        return ("Headers must only be used on the first line of a script.", line)
                if split_line[0] not in VALID_COMMANDS:
                    return ("Command '" + split_line[0] + "' not valid.", line)
                if split_line[0] in ["STRING", "DELAY", "TAP", "PRESS", "RELEASE", "WEB", "WEB_NEW", "CODE", "SOUND", "M_MOVE", "M_SET", "M_SCROLL", "OPEN"]:
                    if len(split_line) < 2:
                        return ("Too few arguments for command '" + split_line[0] + "'.", line)
                if split_line[0] in ["WAIT_UNPRESSED", "RELEASE_ALL", "RESET_REPEATS"]:
                    if len(split_line) > 1:
                        return ("Too many arguments for command '" + split_line[0] + "'.", line)
                if split_line[0] in ["DELAY", "WEB", "WEB_NEW", "PRESS", "RELEASE", "SOUND_STOP"]:
                    if len(split_line) > 2:
                        return ("Too many arguments for command '" + split_line[0] + "'.", line)
                if split_line[0] in ["SOUND", "M_MOVE", "M_SCROLL", "M_SET"]:
                    if len(split_line) > 3:
                        return ("Too many arguments for command '" + split_line[0] + "'.", line)
                if split_line[0] in ["TAP"]:
                    if len(split_line) > 4:
                        return ("Too many arguments for command '" + split_line[0] + "'.", line)
                    if len(split_line) > 3:
                        try:
                            temp = float(split_line[3])
                        except:
                            return (split_line[0] + "Tap wait time '" + split_line[3] + "' not valid.", line)
                    if len(split_line) > 2:
                        try:
                            temp = int(split_line[2])
                        except:
                            return (split_line[0] + " repetitions '" + split_line[2] + "' not valid.", line)
                if split_line[0] in ["M_LINE"]:
                    if len(split_line) > 7:
                        return ("Too many arguments for command '" + split_line[0] + "'.", line)
                if split_line[0] in ["TAP", "PRESS", "RELEASE"]:
                    if kb.sp(split_line[1]) == None:
                        return ("No key named '" + split_line[1] + "'.", line)
                if split_line[0] == "DELAY":
                    try:
                        temp = float(split_line[1])
                    except:
                        return ("Delay time '" + split_line[1] + "' not valid.", line)
                if split_line[0] == "WAIT_UNPRESSED":
                    if len(split_line) > 1:
                        return ("'WAIT_UNPRESSED' takes no arguments.", line)
                if split_line[0] == "SOUND":
                    final_name = sound.full_name(split_line[1])
                    if not os.path.isfile(final_name):
                        return ("Sound file '" + final_name + "' not found.", line)
                    if not sound.is_valid(split_line[1]):
                        return ("Sound file '" + final_name + "' not valid.", line)
                    if len(split_line) > 2:
                        try:
                            vol = float(float(split_line[2]) / 100.0)
                            if (vol < 0.0) or (vol > 1.0):
                                return ("'SOUND' volume must be between 0 and 100.", line)
                        except:
                            return ("'SOUND' volume " + split_line[2] + " not valid.", line)
                if split_line[0] in ["M_STORE", "M_RECALL"]:
                    if len(split_line) > 1:
                        return ("'" + split_line[0] + "' takes no arguments.", line)
                if split_line[0] == "M_RECALL_LINE":
                    if len(split_line) > 1:
                        try:
                            temp = float(split_line[1])
                        except:
                            return ("'" + split_line[0] + "' wait value '" + split_line[1] + "' not valid.", line)
                    if len(split_line) > 2:
                        try:
                            temp = int(split_line[2])
                            if temp == 0:
                                return ("'" + split_line[0] + "' skip value cannot be zero.", line)
                        except:
                            return ("'" + split_line[0] + "' skip value '" + split_line[2] + "' not valid.", line)
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
                    if len(split_line) < 5:
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
                if split_line[0] in ["M_LINE_MOVE", "M_LINE_SET"]:
                    if len(split_line) < 3:
                        return ("'" + split_line[0] + "' requires at least X and Y arguments.", line)
                    try:
                        temp = int(split_line[1])
                    except:
                        return ("'" + split_line[0] + "' X value '" + split_line[1] + "' not valid.", line)
                    try:
                        temp = int(split_line[2])
                    except:
                        return ("'" + split_line[0] + "' Y value '" + split_line[2] + "' not valid.", line)
                    if len(split_line) >= 4:
                        try:
                            temp = float(split_line[3])
                        except:
                            return ("'" + split_line[0] + "' wait value '" + split_line[3] + "' not valid.", line)
                    if len(split_line) >= 5:
                        try:
                            temp = int(split_line[4])
                            if temp == 0:
                                return ("'" + split_line[0] + "' skip value cannot be zero.", line)
                        except:
                            return ("'" + split_line[0] + "' skip value '" + split_line[4] + "' not valid.", line)
                if split_line[0] in ["GOTO_LABEL", "IF_PRESSED_GOTO_LABEL", "IF_UNPRESSED_GOTO_LABEL"]:
                    if len(split_line) != 2:
                        return ("'" + split_line[0] + "' takes exactly 1 argument.", line)
                    if split_line[1] not in labels:
                        return ("Label '" + split_line[1] + "' not defined in this script.", line)
                if split_line[0] in ["REPEAT_LABEL", "IF_PRESSED_REPEAT_LABEL", "IF_UNPRESSED_REPEAT_LABEL"]:
                    if len(split_line) != 3:
                        return ("'" + split_line[0] + "' needs both a label name and how many times to repeat.", line)
                    if split_line[1] not in labels:
                        return ("Label '" + split_line[1] + "' not defined in this script.", line)
                    try:
                        temp = int(split_line[2])
                        if temp < 1:
                            return (split_line[0] + " requires a minimum of 1 repeat.", line)
                    except:
                        return (split_line[0] + " number of repeats '" + split_line[2] + "' not valid.", line)
                if split_line[0] == "OPEN":
                    path_name = " ".join(split_line[1:])
                    if (not os.path.isfile(path_name)) and (not os.path.isdir(path_name)):
                        return (split_line[0] + " folder or file location '" + path_name + "' does not exist.", line)
    return True
