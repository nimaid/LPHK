import threading, webbrowser, os, subprocess
from time import sleep
from functools import partial
import lp_events, lp_colors, kb, sound, ms, files, command_base


# VALID_COMMAND is a dictionary of all commands available.
# it is initially empty because now we load it dynamically

VALID_COMMANDS = dict()


# HEADERS is likewise empty until added (all headers, not just async ones)

HEADERS = dict() 


# Add a new command.  This removes any existing command of the same name from the VALID_COMMANDS
# and returns it as the result

def add_command(
    a_command: command_base.Command_Basic  # the command to add
    ):

    if a_command.name in HEADERS:              # if this was previously a header, now it isn't
        HEADERS.pop(a_command.name)
  
    if a_command.name in VALID_COMMANDS:       # if it already exists
        p = VALID_COMMANDS[a_command.name]     # get it
    else:                                      # otherwise
        p = None                               # the return value will be None

    VALID_COMMANDS[a_command.name] = a_command # add the new command

    if a_command is command_base.Command_Header:     # is this a header?
        HEADERS[a_command.name] = a_command.is_async # add it

    return p                                   # return any replaced command
       
 
# Create a new symbol table.  This contains information required for the script to run
# it includes the locations of labels, loop counters, etc.  If we implement variables
# this is where we would place them

def new_symbol_table():
    # returns a new (blank) symbol table
    # symbol table is dictionary of objects
    symbols = {
        "repeats": dict(),
        "original": dict(), 
        "labels": dict(),
        "m_pos": tuple(),
        "vars": dict(),      # global (to the script) variables
        "stack": [] }        # script stack (for RPN_EVAL)        

    return symbols


#  Do what is required to parse the script.  Parsing does not output any information unless it is an error 

def parse_script(script_lines, symbols):
    err = True
    errors = 0                                                  # no errors found

    for pass_no in (1,2):                                       # pass 1, collect info & syntax check, 
                                                                # pass 2 symbol check & assocoated processing
        for idx,line in enumerate(script_lines):                # gen line number and text
            if is_ignorable_line(line):
                continue                                        # don't process ignorable lines
            split_line = line.split(" ")                        # split line on spaces
            if split_line[0] in VALID_COMMANDS:                 # if first element is a command
                res = VALID_COMMANDS[split_line[0]].Parse(idx, line, script_lines, split_line, symbols, pass_no);
                if res != True:
                    if err == True:
                        err = res                               # note the error
                    errors += 1                                 # and 1 more error
            else:
                msg = "Invalid command '" + split_line[0] + "' on line " + str(idx) + "."
                if err == True:
                    err = (msg, line) # note the error
                print (msg)
                errors += 1                                     # and 1 more error

        print('Pass ' + str(pass_no) + ' complete.  ' + str(errors) + ' errors detected.')
        if err != True:
            break                                               # errors prevent next pass

    return err                                                  # success or failure 


COLOR_PRIMED = 5 #red
COLOR_FUNC_KEYS_PRIMED = 9 #amber
EXIT_UPDATE_DELAY = 0.1
DELAY_EXIT_CHECK = 0.025


threads = [[None for y in range(9)] for x in range(9)]
running = False
to_run = []
text = [["" for y in range(9)] for x in range(9)]


def check_kill(x, y, is_async, killfunc=None):
    global threads

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


# a sleep method that works with the multiple threads

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


# some lines can be ignored.  These include blank lines and comments.  It's faster to identify them
# before trying to process them than treat them as an exception afterwards.

def is_ignorable_line(line):
    line = line.strip()      # remove leading and trailing spaces
    if line != "":
        if line[0] == "-":
            return True      # non-blank lines starting with a hyphen are comments (and can be ignored)
        else:
            return False     # other non-blank lines are significant
    else:
        return True          # blank lines can be igmored


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

    token = script_in.split("\n")[0].split(" ")[0]
    if token in HEADERS and HEADERS[token].is_async:
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


# run a script

def run_script(script_str, x, y):
    global running
    global exit

    lp_colors.updateXY(x, y)
    coords = "(" + str(x) + ", " + str(y) + ")"
    
    print("[scripts] " + coords + " Now running script...")

    script_lines = script_str.split("\n")    
    script_lines = [i.strip() for i in script_lines]
    
    if len(script_lines) > 0:
        is_async = False
        token = script_lines[0].split(" ")[0]
        if token in VALID_COMMANDS:
            command = VALID_COMMANDS[token]
            is_async = token in HEADERS and HEADERS[token].is_async
        else:
            running = True

        symbols = new_symbol_table()

        # parse labels (do all parsing required for commands)
        parse_script(script_lines, symbols)
                

        def main_logic(idx):
            nonlocal symbols
            
            if check_kill(x, y, is_async):
                return idx + 1
                
            line = script_lines[idx]
            if line == "":
                return idx + 1

            if line[0] == "-":
                split_line = ["-", line[1:]]                       # comments are special -- not tokenised
            else:
                split_line = line.split(" ")

                if split_line[0] in VALID_COMMANDS:                # if first element is a command
                    command = VALID_COMMANDS[split_line[0]]        # get the command
                    return command.Run(idx, split_line, symbols, (coords, x, y), is_async)

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


# determine if a key is bound

def is_bound(x, y):
    if text[x][y] == "":
        return False
    else:
        return True


# Unbind all keys.  

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
    

# validating a script consists of doing the checks that we do prior to running, but
# we won't run it afterwards.

def validate_script(script_str):
    if script_str == "":
        return True

    script_lines = script_str.split('\n')
    script_lines = [i.strip() for i in script_lines]
    
    symbols = new_symbol_table()

    return parse_script(script_lines, symbols)


