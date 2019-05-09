import threading, webbrowser, os
from time import sleep
from functools import partial
import lp_events, lp_colors, kb, sound, ms

COLOR_PRIMED = 5 #red
COLOR_FUNC_KEYS_PRIMED = 9 #amber
EXIT_UPDATE_DELAY = 0.1
DELAY_EXIT_CHECK = 0.025

import files

'''
    Hard-coded functions:
    * @ASYNC (makes script run in the background)
    * LABEL (trated like a comment, pre-parsed)
    * GOTO_LABEL (returns the label index from labels['name'])
    * IF_PRESSED_GOTO_LABEL (if lp_events.pressed[x][y] then return labels['name'])
    * IF_UNPRESSED_GOTO_LABEL (above, but logically inverted
    * REPEAT_LABEL (GOTO_LABEL, but only works set number of times, uses the dict repeats)
    * IF_PRESSED_REPEAT_LABEL
    * IF_UNPRESSED_REPEAT_LABEL
    * RESET_REPEATS (resets all REPEAT_LABEL counters)
'''
HARDCODE_COMMANDS = ["@ASYNC", "LABEL", "GOTO_LABEL", "IF_PRESSED_GOTO_LABEL", "IF_UNPRESSED_GOTO_LABEL", "REPEAT_LABEL", "IF_PRESSED_REPEAT_LABEL", "IF_UNPRESSED_REPEAT_LABEL", "RESET_REPEATS"]

threads = [[None for y in range(9)] for x in range(9)]
running = False
to_run = []
text = [["" for y in range(9)] for x in range(9)]
run_async = [[False for y in range(9)] for x in range(9)]

def strip_script(script_in):
    script_lines = script_in.split("\n")
    script_out = ""
    for idx,line in enumerate(script_lines):
        line = line.strip()
        if (line != "") and (line[0] != "-"):
            if len(script_out) > 0:
                script_out += "\n"
            script_out += line
    return script_out

def split_command_string(cmd_str):
    cmd_split = cmd_str.split(" ")
    cmd_command =  cmd_split[0]
    cmd_args = cmd_split[1:]
    return (cmd_command, cmd_args)

def script_calls_for_async(script_in):
    script_lines = script_in.split('\n')
    first_line = script_lines[0]
    first_cmd, first_args = split_command_string(first_line)
    
    if first_cmd == "@ASYNC":
        return True
    # Add check if is macro that is async here
    
    return False

def schedule_script(script_in, x, y):
    global threads
    global to_run
    global running
    global run_async
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
    
    # Determine if the script is run as ASYNC or not.
    run_async[x][y] = script_calls_for_async(script_in)
    
    if run_async[x][y]:
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
    global run_async

    lp_colors.updateXY(x, y)
    coords = "(" + str(x) + ", " + str(y) + ")"

    script_lines = script_str.split("\n")

    if not run_async[x][y]:
        running = True
    
    if script_lines[0].split(" ")[0] == "@ASYNC":
        temp = script_lines.pop(0)
    
    print("[scripts] " + coords + " Now running script...")
    
    #parse labels
    labels = dict()
    for idx,line in enumerate(script_lines):
        cmd, args = split_command_string(line)
        if cmd == "LABEL":
            labels[args[0]] = idx
    
    #prepare repeat counter {idx:repeats_left}
    repeats = dict()
    repeats_original = dict()
    
    m_pos = ()
    
    
    def main_logic(idx):
        nonlocal m_pos
        
        if threads[x][y].kill.is_set():
            print("[scripts] " + coords + " Recieved exit flag, script exiting...")
            threads[x][y].kill.clear()
            if not is_async:
                running = False
            threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
            return idx + 1
        
        line = script_lines[idx]
        cmd, args = split_command_string(line)
        
        if cmd == "LABEL":
            # Labels are pre-parsed, ignored
            pass
        
        if cmd == "IF_PRESSED_GOTO_LABEL":
            # Only do GOTO_LABEL if key is pressed
            if lp_events.pressed[x][y]:
                cmd = "GOTO_LABEL"
        if cmd == "IF_UNPRESSED_GOTO_LABEL":
            # Only do GOTO_LABEL if key is not pressed
            if  not lp_events.pressed[x][y]:
                cmd = "GOTO_LABEL"
        if cmd == "GOTO_LABEL":
            # Return index of the label
            label_name = args[0]
            return labels[label_name]

        if cmd == "IF_PRESSED_REPEAT_LABEL":
            # Only do REPEAT_LABEL if key is pressed
            if lp_events.pressed[x][y]:
                cmd = "REPEAT_LABEL"
        if cmd == "IF_UNPRESSED_REPEAT_LABEL":
            # Only do REPEAT_LABEL if key is not pressed
            if not lp_events.pressed[x][y]:
                cmd = "REPEAT_LABEL"
        if cmd == "REPEAT_LABEL":
            # Only return the index of label a certain number of times
            if idx in repeats:
                if repeats[idx] > 0:
                    repeats[idx] -= 1
                    return labels[args[0]]
                else:
                    # No repeats left, ignored
                    pass
            else:
                repeats[idx] = int(args[1])
                repeats_original[idx] = int(args[1])
                repeats[idx] -= 1
                return labels[args[0]]
        
        if cmd == "RESET_REPEATS":
            # Reset all repeat counters
            for i in repeats:
                repeats[i] = repeats_original[i]
        
        return idx + 1 # If nothing above returned, return next index
    run = True
    idx = 0
    while run:
        idx = main_logic(idx)
        if (idx < 0) or (idx >= len(script_lines)):
            run = False
    
    print("[scripts] (" + str(x) + ", " + str(y) + ") Script done running.")

    if not run_async[x][y]:
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
            if threads[x][y] != None:
                if threads[x][y].isAlive():
                    threads[x][y].kill.set()
    files.curr_layout = None
    files.layout_changed_since_load = False
    
def validate_script(script_str):
    script_str = strip_script(script_str)
    
    if script_str == "":
        return True
        
    script_lines = script_str.split('\n')
    first_line = script_lines[0]
    first_cmd, first_args = split_command_string(first_line)
    
    #pre-parse labels
    labels = []
    for line in script_lines:
        cmd, args = split_command_string(line)
        if cmd == "LABEL":
            if len(args) != 1:
                return ("LABEL takes exactly 1 argument.", line)
            label_name = args[0]
            if label_name in labels:
                return ("Label '" + label_name + "' defined multiple times.", line)
            else:
                labels.append(args[0])
    
    #main for loop
    for idx, line in enumerate(script_lines):
        # Check for illegal strings
        for sep in (files.ENTRY_SEPERATOR, files.BUTTON_SEPERATOR, files.NEWLINE_REPLACE):
            if sep[1:-1] in line:
                return ("You cannot use the string '" + sep[1:-1] + "' in any script.", line)
        
        # Split command string
        cmd, args = split_command_string(line)
        
        # Take care of invalid commands
        if (cmd not in HARDCODE_COMMANDS) and (cmd[0] != "_"): ####ADD CHECK FOR IMPORTED COMMANDS
            return ("Command '" + cmd + "' not valid.", line)
        
        # Take care of header and macro rules
        if cmd[0] == "@":
            if idx != 0:
                return ("Headers must only be used on the first line of a script.", line)
        if cmd[0] == "_":
            if len(script_lines) > 1:
                return ("Macros must be the only command in a script. (Comments OK)", line)
        
        # Validate hard-coded functions
        if cmd == "@ASYNC":
            if len(args) > 0:
                return ("@ASYNC takes no arguments.", first_line)
        if cmd in ["GOTO_LABEL", "IF_PRESSED_GOTO_LABEL", "IF_UNPRESSED_GOTO_LABEL"]:
            if len(args) != 1:
                return ("'" + cmd + "' takes exactly 1 argument.", line)
            label_name = args[0]
            if label_name not in labels:
                return ("Label '" + label_name + "' not defined in this script.", line)
        if cmd in ["REPEAT_LABEL", "IF_PRESSED_REPEAT_LABEL", "IF_UNPRESSED_REPEAT_LABEL"]:
            if len(args) != 2:
                return ("'" + cmd + "' needs both a label name and how many times to repeat.", line)
            label_name = args[0]
            repeat_times = args[1]
            if label_name not in labels:
                return ("Label '" + label_name + "' not defined in this script.", line)
            try:
                temp = int(repeat_times)
                if temp < 1:
                    return (cmd + " requires a minimum of 1 repeat.", line)
            except:
                return (cmd + " number of repeats '" + repeat_times + "' must be a valid decimal integer.", line)
        if cmd == "RESET_REPEATS":
            if len(args) > 0:
                return ("RESET_REPEATS takes no arguments.", first_line)
        
        # Validate imported commands
    return True