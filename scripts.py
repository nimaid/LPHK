import threading, webbrowser, os, subprocess
from time import sleep
from functools import partial
import lp_events, lp_colors, kb, sound, ms, files, command_base
from constants import *


# VALID_COMMAND is a dictionary of all commands available.
# it is initially empty because now we load it dynamically

VALID_COMMANDS = dict()


# HEADERS is likewise empty until added (all headers, not just async ones)

HEADERS = dict() 


# GLOBALS is likewise empty until global variables get created

GLOBALS = dict()                  # the globals themselvs
GLOBAL_LOCK = threading.Lock()    # a lock got the globals to prevent simultaneous access




# Add a new command.  This removes any existing command of the same name from the VALID_COMMANDS
# and returns it as the result

def Add_command(
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

def New_symbol_table():
    # returns a new (blank) symbol table
    # symbol table is dictionary of objects
    symbols = {
        SYM_REPEATS:  dict(),
        SYM_ORIGINAL: dict(), 
        SYM_LABELS:   dict(),
        SYM_MOUSE:    tuple(),
        SYM_GLOBAL:   [GLOBAL_LOCK, GLOBALS],  # global (to the application) variables (and associated lock)
        SYM_LOCAL:    dict(),                  # local (to the script) variables (with no lock)
        SYM_STACK:    [] }                     # script stack (for RPN_EVAL)        

    return symbols


# ##################################################
# ### CLASS Button                               ###
# ##################################################

# class that defines a button.
# A button is a class containing all that's essential for a button.
class Button():
    def __init__(
        self, 
        x,                                   # The button column
        y,                                   # The button row
        script_str                           # The Script
        ):

        self.x = x
        self.y = y
        self.script_str = script_str         # The script
        self.validated = False               # Has the script been validated?
        self.symbols = None                  # The symbol table for the button
        self.script_lines = None             # the lines of the script
        self.thread = None                   # the thread associated with this button
        self.running = False                 # is the script running?
        self.is_async = False                # async execution flag
        self.coords = "(" + str(self.x) + ", " + str(self.y) + ")" # let's just do this the once eh?
    
    
    #  Do what is required to parse the script.  Parsing does not output any information unless it is an error 
    def Parse_script(self):
        if self.validated:                           # we don't want to repeat validation over and over
            return True
            
        if self.script_lines == None:                # A little setup if the script lines are not created
            self.script_lines = self.script_str.split('\n')  # Create the lines
            self.script_lines = [i.strip() for i in self.script_lines] # Strip extra blanks
        
            self.symbols = New_symbol_table()        # Create a shiny new symbol table
            self.is_async = False                    # default is NOT async

        err = True
        errors = 0                                   # no errors found

        for pass_no in (VS_PASS_1, VS_PASS_2):       # pass 1, collect info & syntax check, 
                                                     # pass 2 symbol check & assocoated processing
            for idx,line in enumerate(self.script_lines): # gen line number and text
                if self.Is_ignorable_line(line):
                    continue                         # don't process ignorable lines
                 
                cmd_txt = self.Split_cmd_text(line)  # get the name of the command

                if cmd_txt in VALID_COMMANDS:        # if first element is a command
                    command = VALID_COMMANDS[cmd_txt]# get the command itself
                    split_line = self.Split_text(command, cmd_txt, line) # now split the line appropriately
                    res = command.Parse(self, idx, split_line, pass_no);
                    if res != True:
                        if err == True:
                            err = res                # note the error
                        errors += 1                  # and 1 more error
                else:
                    msg = " Invalid command '" + cmd_txt + "' on line " + str(idx+1) + "."
                    if err == True:
                        err = (msg, line)            # note the error
                    print (msg)
                    errors += 1                      # and 1 more error

            print('Pass ' + str(pass_no) + ' complete.  ' + str(errors) + ' errors detected.')
            if err != True:
                break                                # errors prevent next pass

        return err                                   # success or failure 


    def Check_kill(self, killfunc=None):
        if not self.thread:
           print ("expecting a thread in ", self.coords)
           return False
           
        if self.thread.kill.is_set():
            print("[scripts] " + self.coords + " Recieved exit flag, script exiting...")
            self.thread.kill.clear()
            if not self.is_async:
                self.running = False
            if killfunc:
                killfunc()
            threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (self.x, self.y)).start()
            return True
        else:
            return False


    # a sleep method that works with the multiple threads

    def Safe_sleep(self, time, endfunc=None):
        while time > DELAY_EXIT_CHECK:
            sleep(DELAY_EXIT_CHECK)
            time -= DELAY_EXIT_CHECK
            if self.Check_kill(endfunc):
                return False
        if time > 0:
            sleep(time)
        if endfunc:
            endfunc()
        return True


    # some lines can be ignored.  These include blank lines and comments.  It's faster to identify them
    # before trying to process them than treat them as an exception afterwards.

    def Is_ignorable_line(self, line):
        line = line.strip()      # remove leading and trailing spaces
        if line != "":
            if line[0] == "-":
                return True      # non-blank lines starting with a hyphen are comments (and can be ignored)
            else:
                return False     # other non-blank lines are significant
        else:
            return True          # blank lines can be igmored


    def Schedule_script(self):
        global to_run
        
        if self.thread != None:
            if self.thread.is_alive():
                # @@@ The following code creates a problem if a script is looking for a second keypress
                # @@@ Maybe we need an option to make a script un-interruptable, or alternately require
                # @@@ *something* else (maybe ctrl-alt) to be pressed to allow the kill to take place.
                print("[scripts] " + self.coords + " Script already running, killing script....")
                self.thread.kill.set()
                return

        if (self.x, self.y) in [l[1:] for l in to_run]:
            print("[scripts] " + self.coords + " Script already scheduled, unscheduling...")
            indexes = [i for i, v in enumerate(to_run) if ((v[1] == self.x) and (v[2] == self.y))]
            for index in indexes[::-1]:
                temp = to_run.pop(index)
            return

        if self.is_async:
            print("[scripts] " + self.coords + " Starting asynchronous script in background...")
            self.thread = threading.Thread(target=run_script, args=())
            self.thread.kill = threading.Event()
            self.thread.start()
        elif not self.running:
            print("[scripts] " + self.coords + " No script running, starting script in background...")
            self.thread = threading.Thread(target=self.Run_script_and_run_next, args=())
            self.thread.kill = threading.Event()
            self.thread.start()
        else:
            print("[scripts] " + self.coords + " A script is already running, scheduling...")
            to_run.append((self.x, self.y))
            
        lp_colors.updateXY(self.x, self.y)


    def Run_next(self):
        global to_run
        global buttons

        if len(to_run) > 0:
            tup = to_run.pop(0)
            x = tup[0]
            y = tup[1]

            btn = buttons[x][y]
            btn.Schedule_script()


    def Run_script_and_run_next(self):
        self.Run_script()
        self.Run_next()
        
        
    def Line(self, idx):
        if self.script_lines and idx >=0 and idx < len(self.script_lines):
            return self.Fix_comment(self.script_lines[idx])
        else:
            return ""


    def Fix_comment(self, line):
        # Ensure there's a space after the comment character
        if len(line) > 1 and line[0] == "-" and line[1] != " ":
            return line[0] + " " + line[1:]
        else:
            return line


    def Split_cmd_text(self, line):
        # Get the command text
        line += ' '
        return line[0:line.find(" ")]


    def Split_text(self, command, cmd_txt, line):
        # Split line differently for "text" type commands
        if isinstance(command, command_base.Command_Text_Basic):
            # just split the command from the rest of the text
            return [cmd_txt, line[len(cmd_txt)+1:]]
        else:
            # for all other commands, split on spaces
            return line.split(" ")


    # run a script
    def Run_script(self):
        lp_colors.updateXY(self.x, self.y)
        
        if self.Validate_script() != True:
           return
           
        print("[scripts] " + self.coords + " Now running script...")
        
        self.running = not self.is_async

        cmd_txt = "RESET_REPEATS"             # before we run, we want to rest loop counters
        if cmd_txt in VALID_COMMANDS:
            command = VALID_COMMANDS[cmd_txt]  
            command.Run(self, -1, [cmd_txt])        
        
        if len(self.script_lines) > 0:
            self.running = True

            def Main_logic(idx):
                if self.Check_kill():
                    return idx + 1
                        
                line = self.Line(idx)
                
                # Handle completely blank lines
                if line == "":
                    return idx + 1

                # Get the command text
                cmd_txt = self.Split_cmd_text(line)

                # Now get the command object
                if cmd_txt in VALID_COMMANDS:
                    command = VALID_COMMANDS[cmd_txt]
                    
                    split_line = self.Split_text(command, cmd_txt, line)
                        
                    # now run the command 
                    return command.Run(self, idx, split_line)
                else:
                    print("[scripts] " + self.coords + "    Invalid command: '" + cmd_txt + "', skipping...")

                return idx + 1

            run = True
            idx = 0
            while run:
                idx = Main_logic(idx)
                if (idx < 0) or (idx >= len(self.script_lines)):
                    run = False
                    
            if not self.is_async:
                self.running = False
                
            threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (self.x, self.y)).start()
        
        print("[scripts] " + self.coords + " Script done running.")

        
    # validating a script consists of doing the checks that we do prior to running, but
    # we won't run it afterwards.
    def Validate_script(self):
        if self.validated or self.script_str == "":      # If valid or there is no script...
            self.validated = True
            return True                                  # ...validation succeeds!

        if self.Parse_script():                          # If parsing is OK
            self.validated = True                        # Script is valid

            if len(self.script_lines) > 0:               # look for async header and set flag
                cmd_txt = self.Split_cmd_text(self.script_lines[0])
                self.is_async = cmd_txt in HEADERS and HEADERS[cmd_txt].is_async
        else:
            self.symbols = None                          # otherwise destroy symbol table 

        return self.validated                            # and tell us the result            



buttons = [[Button(x, y, "") for y in range(9)] for x in range(9)]
to_run = []


# bind a button
def Bind(x, y, script_str, color):
    global to_run
    global buttons
    
    btn = Button(x, y, script_str)
    buttons[x][y] = btn

    if (x, y) in [l[1:] for l in to_run]:    # If this button is scheduled to run...
        indexes = [i for i, v in enumerate(to_run) if ((v[1] == x) and (v[2] == y))]  #... create a list of locations in the list for this button 
        for index in indexes[::-1]:          # and for each of them (in reverse order)
            temp = to_run.pop(index)         # Remove them from the list
        return # Why do we return here?

    schedule_script_bindable = lambda a, b: btn.Schedule_script()

    lp_events.bind_func_with_colors(x, y, schedule_script_bindable, color)
    files.layout_changed_since_load = True   # Mark the layout as changed


# unbind a button
def Unbind(x, y):
    global to_run
    global buttons

    lp_events.unbind(x, y)                   # Clear any events associated with the button
    
    btn = Button(x, y, "")                   # create the new blank button

    if (x, y) in [l[1:] for l in to_run]:    # If this button is scheduled to run...
        indexes = [i for i, v in enumerate(to_run) if ((v[1] == x) and (v[2] == y))]  #... create a list of locations in the list for this button 
        for index in indexes[::-1]:          # and for each of them (in reverse order)
            temp = to_run.pop(index)         # Remove them from the list
        buttons[x][y] = btn                  # Clear the button script
        return # WHY do we return here?

    if thread[x][y] != None:                 # If the button is actially executing
        thread[x][y].kill.set()              # then kill it
    
    buttons[x][y] = btn                      # Clear the button script
    
    files.layout_changed_since_load = True   # Mark the layout as changed


# swap details for two buttons  
def Swap(x1, y1, x2, y2):
    global text

    color_1 = lp_colors.curr_colors[x1][y1]  # Colour for btn #1
    color_2 = lp_colors.curr_colors[x2][y2]  # Colour for btn #2
    
    script_1 = buttons[x1, y1].script_str    # Script for btn #1                 
    script_2 = buttons[x2, y2].script_str    # Script for btn #2
    
    Unbind(x1, y1)                           # Unbind #1
    if script_2 != "":                       # If there is a script #2...
        Bind(x1, y1, script_2, color_2)      # ...bind it to #1
    lp_colors.updateXY(x1, y1)               # Update the colours for btn #1
    
    Unbind(x2, y2)                           # Do the reverse for #2
    if script_1 != "":
        Bind(x2, y2, script_1, color_1)
    lp_colors.updateXY(x2, y2)
    
    files.layout_changed_since_load = True   # Flag that the layout has changed


# Duplicate a button
def Copy(x1, y1, x2, y2):
    global buttons

    color_1 = lp_colors.curr_colors[x1][y1]  # Get colour of btn to be copied
    
    script_1 = buttons[x1, y1].script_str    # Get script to be copied
    
    Unbind(x2, y2)                           # Unbind the destination
    if script_1 != "":                       # If we're copying a button with a script...
        Bind(x2, y2, script_1, color_1)      # ...bind the details to the destination
    lp_colors.updateXY(x2, y2)               # Update the colours
    
    files.layout_changed_since_load = True   # Flag the layout as changed


# move a button
def Move(x1, y1, x2, y2):
    global buttons

    color_1 = lp_colors.curr_colors[x1][y1]  # Get source button colour
    
    script_1 = buttons[x1, y1].script_str    # Get source button script
    
    Unbind(x1, y1)                           # Unbind *both* buttons
    Unbind(x2, y2)
    
    if script_1 != "":                       # If the source had a script...
        Bind(x2, y2, script_1, color_1)      # ...bind it to the destination
    lp_colors.updateXY(x2, y2)               # Update the destination colours
    
    files.layout_changed_since_load = True   # And flag the layout as changed


# determine if a key is bound
def Is_bound(x, y):
    global buttons

    if buttons[x][y].script_str == "":       # If there is no script...
        return False                         # ...it's not bound
    else:
        return True                          # Otherwise it is


# Unbind all keys.  
def Unbind_all():
    global buttons
    global to_run

    lp_events.unbind_all()                   # Unbind all events
    text = [["" for y in range(9)] for x in range(9)] # Reienitialise all scripts to blank
    to_run = []                              # nothing queued to run
    
    for x in range(9):                       # For each column...
        for y in range(9):                   # ...and row
            btn = buttons[x][y]
            if btn.thread is not None:       # If there is a thread...
                if btn.thread.isAlive():     # ...and if the thread is alive...
                    btn.thread.kill.set()    # ...kill it

    files.curr_layout = None                 # There is no current layout
    files.layout_changed_since_load = False  # So mark it as unchanged
    

