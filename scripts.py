import threading, webbrowser, os, subprocess
from time import sleep
from functools import partial
import lp_events, lp_colors, kb, sound, ms, files, command_base, variables
from constants import *
from window import Redraw


# VALID_COMMAND is a dictionary of all commands available.
# it is initially empty because now we load it dynamically

VALID_COMMANDS = dict()


# GLOBALS is likewise empty until global variables get created

GLOBALS = dict()                  # the globals themselvs
GLOBAL_LOCK = threading.Lock()    # a lock for the globals to prevent simultaneous access


# Add a new command.  This removes any existing command of the same name from the VALID_COMMANDS
# and returns it as the result

def Add_command(
    a_command: command_base.Command_Basic            # the command or header to add
    ):

    if a_command.name in VALID_COMMANDS:             # or if it was a command
        p = VALID_COMMANDS.pop(a_command.name)       # pop that too
    else:                                            # otherwise
        p = None                                     # the return value will be None (we're not replacing anything)

    VALID_COMMANDS[a_command.name] = a_command       # add the new command

    return p                                         # return any replaced command


# Remove a command.  This could be useful in handling subroutines

def Remove_command(
    command_name  # the command to remove
    ):

    if command_name in VALID_COMMANDS:         # check command
        p = VALID_COMMANDS.pop(command_name)   # remove the command
    else:
        p = None                               # nothing to remove

    return p                                   # the thing we removed


# display info on all commands and headers

def Dump_commands(style=DS_NORMAL):
    def checkindent(line, oldindent, defaultindent):
        skip = False
        newindent = oldindent

        if line[:1] == '~':
            if line[1:] == '':
                newindent = defaultindent
                skip = True
            else:
                try:
                    newindent = defaultindent + int(line[1:])
                    skip = True
                except:
                    pass

        return newindent, skip

    def wrap_line(s, indent=0, wrap=80):
        import textwrap

        pre = s[:indent]
        post = s[indent:]
        wrapped = textwrap.wrap(post, width=wrap-indent)
        sep = '\n' + ' '*indent
        return pre + sep.join(wrapped)

    def get_name(c):
        if isinstance(c, command_base.Command_Basic):
            return c.name
        elif isinstance(c, Button):
            return c.coords
        else:
            return "ERROR"

    def get_desc(c):
        ret = ''
        if isinstance(c, command_base.Command_Basic):
            if hasattr(c, 'desc') and not callable(c.desc):
                ret = c.desc
            if hasattr(c, 'btn') and not callable(c.btn) and c.btn:
                if c.btn.desc != "":
                    ret = c.btn.desc
        elif isinstance(c, Button):
            ret = c.desc
        else:
            ret = "ERROR"

        return ret

    def dump_name(c_type, c):
        l = f"    {c_type} \"{get_name(c)}\""
        desc = get_desc(c)
        if desc == "":
            print(l)
        else:
            l = l + ' - '
            print(wrap_line(l + desc, len(l)))

    def dump_deprecated(c_type, c):
        ret = []
        if isinstance(c, command_base.Command_Basic) or isinstance(c, Button):
            if c.deprecated:
                print("        Deprecated")
                if c.deprecated_use != "":
                    print(wrap_line(" "*12 + c.deprecated_use, 12))
                else:
                    print(wrap_line(" "*12 + "This command may not exist in future versions of LPHK.", 12))

    def get_doc(c):
        ret = []
        if isinstance(c, command_base.Command_Basic):
            if hasattr(c, 'doc') and not callable(c.doc):
                ret = c.doc
            if hasattr(c, 'btn') and not callable(c.btn) and c.btn:
                if c.btn.doc != []:
                    ret = c.btn.doc
        elif isinstance(c, Button):
            ret = c.doc
        else:
            ret = ["ERROR"]

        return ret

    def dump_doc(c):
        doc = get_doc(c)
        if doc != []:
            print("        Notes")
            indent = 12
            for n in doc:
                indent, skip = checkindent(n, indent, 12)
                if not skip:
                    print(wrap_line(" "*12 + n, indent))

    def dump_ancestory(c):
        print("        Ancestory")
        print(f"            {type(c)}")
        a = type(c).__bases__[0]
        while a != object:
            print(f"            {a}")
            a = a.__bases__[0]

    def dump_params(c):
        if isinstance(c, command_base.Command_Basic):
            print("        Parameters")
            if c.auto_validate == None:
                print("            Parameters undocumented (Auto-validation is not defined)")
            elif len(c.auto_validate) == 0:
                print("            No parameters")
            else:
                for v in c.auto_validate:
                    print(f"            {v[AV_DESCRIPTION]} - {v[AV_TYPE][AVT_DESC]}", end="")

                    if v[AV_OPTIONAL]:
                        print(" (opt),", end="")
                    else:
                        print(" (reqd),", end="")

                    if v[AV_VAR_OK] == AVV_NO:
                        print(" constant only")
                    elif v[AV_VAR_OK] == AVV_YES:
                        print(" variable permitted")
                    elif v[AV_VAR_OK] == AVV_REQD:
                        print(" variable required (possible return value)")
                    else:
                        print(" UNKNOWN VALUE")

    def dump_source(c, hide_doc):

        def print_source(lines):
            print("        Source")
            for i, line in enumerate(lines):
                if hide_doc and line.lstrip().split()[:1] in [['@NAME'], ['@DESC'], ['@DOC'], ['@DOC+']]:
                    continue
                l = f"            {i+1:3}: "
                p = line.lstrip().find(" ") + len(line) - len(line.lstrip()) + 1
                print(wrap_line(l+line, len(l)+p))

        if isinstance(c, commands_subroutines.Subroutine):
            print_source(c.routine)
        elif isinstance(c, Button):
            print_source(c.script_lines)

    def dump(c_type, c, style):
        dump_name(c_type, c)
        dump_deprecated(c_type, c)
        dump_doc(c)
        if D_DEBUG in style:
            dump_ancestory(c)
        dump_params(c)
        if D_SOURCE in style:
            dump_source(c, D_NO_SRC_DOC in style)

        print()

    import commands_subroutines

    if D_HEADERS in style:
        print("HEADERS")
        print()
        for cmd in VALID_COMMANDS:
            if isinstance(VALID_COMMANDS[cmd], command_base.Command_Header):
                dump("Header", VALID_COMMANDS[cmd], style)

    if D_COMMANDS in style:
        print("COMMANDS")
        print()
        for cmd in VALID_COMMANDS:
            if not (isinstance(VALID_COMMANDS[cmd], commands_subroutines.Subroutine) or \
                isinstance(VALID_COMMANDS[cmd], command_base.Command_Header)):
                dump("Command", VALID_COMMANDS[cmd], style)

    if D_SUBROUTINES in style:
        print("SUBROUTINES")
        print()
        for cmd in VALID_COMMANDS:
            if isinstance(VALID_COMMANDS[cmd], commands_subroutines.Subroutine):
                dump("Subroutine", VALID_COMMANDS[cmd], style)

    if D_BUTTONS in style:
        print("BUTTONS")
        print()
        global buttons
        for x in range(9):
            for y in range(9):
                btn = buttons[x][y]
                if btn.script_str != "":
                    dump("Button", btn, style)


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
        script_str,                          # The Script
        root = None,                         # Who called us
        name = ''                            # name of this button (subroutine)
        ):

        self.x = x
        self.y = y
        self.is_button = x >= 0 and y >= 0   # It's a button if it has valid (non-negative) coordinates, otherwise it must be a subroutine
        self.script_str = script_str         # The script
        self.colour = None                   # default is no colour

        self.name = None
        self.Set_name(name)                  # only for subroutines at present, but useful to print a caption for a button?
        self.desc = ""
        self.doc = []

        self.validated = False               # Has the script been validated?
        self.symbols = None                  # The symbol table for the button
        self.script_lines = None             # the lines of the script
        self.thread = None                   # the thread associated with this button
        self._running = False                # is the script running?
        self.is_async = False                # async execution flag

        self.invalid_on_load = False         # flag for button found invalid on load from stored layout

        # The "root" is the button that is scheduled.  This allows subroutines to check if the
        # initiating button has been killed.
        if root == None:                     # if we are not being called
            self.root = self                 # then we are the root
        else:                                # otherwise
            self.root = root                 # the caller is the root

        self.deprecated = False              # by default, buttons (remember that subroutines are buttons!) are not deprecated
        self.deprecated_use = ""             # allow text to specify a replacement


    # let us set/change the name of a button
    def Set_name(self, name):
        update = self.name != None                             # it is initialisation if the original contents is None
        self.name = name                                       # update the name

        self.coords = ''                                       # Start the process of updating the coords

        if self.is_button:                                     # include actual coords if it is actually a button
            self.coords += "(" + str(self.x+1) + ',' + str(self.y+1) + ")" # let's just do this the once eh?
        if self.name != "":                                    # If it has a name, let's include that too
            self.coords = " ".join([self.name, self.coords])   # remember that subroutines don't have coordinates

        if update and self.is_button:                          # no need to update the window on initialisation
            Redraw(self.x, self.y)                             # and we only need to update this button


    def running(self, set_to=None):
        if type(set_to) == bool and set_to != self._running:
            self._running = set_to
            Redraw(self.x, self.y)                             # redraw the canvas when the button run status is changed

        return self._running


    #  Do what is required to parse the script.  Parsing does not output any information unless it is an error
    def Parse_script(self, full_parse=True):
        if self.validated:                           # we don't want to repeat validation over and over
            return True

        self.colour = None                           # no colour from the script

        if self.script_lines == None:                # A little setup if the script lines are not created
            if isinstance(self.script_str, list):    # Subroutines already have this as a list of lines
                self.script_lines = self.script_str  # Copy the lines
            else:                                    # But commands just have the raw stream from a file
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
                    if full_parse or isinstance(command, command_base.Command_Header):
                        split_line = self.Split_text(command, cmd_txt, line) # now split the line appropriately

                        if type(split_line) == tuple:
                            if err == True:
                               err = split_line
                               errors += 1
                        else:
                            res = command.Parse(self, idx, split_line, pass_no);
                            if res != True:
                                if err == True:
                                    err = res        # note the error
                                errors += 1          # and 1 more error
                else:
                    msg = " Invalid command '" + cmd_txt + "' on line " + str(idx+1) + "."
                    if err == True:
                        err = (msg, line)            # note the error
                    print (msg)
                    errors += 1                      # and 1 more error

            if err != True:
                if full_parse:
                    if self.is_button:
                        print('Pass ' + str(pass_no) + ' complete for button ' + self.coords + '.  ' + str(errors) + ' errors detected.')
                    else:
                        print('Pass ' + str(pass_no) + ' complete for subroutine ' + self.coords +'.  ' + str(errors) + ' errors detected.')
                else:
                    if self.is_button:
                        print('Pass ' + str(pass_no) + ' (partial) for button ' + self.coords + '.  ' + str(errors) + ' errors detected.')
                    else:
                        print('Pass ' + str(pass_no) + ' (partial) for subroutine ' + self.coords +'.  ' + str(errors) + ' errors detected.') # should never happen!
                break                                # errors prevent next pass

        return err                                   # success or failure


    #  copies parsed info from self to new_btn
    def Copy_parsed(self, new_btn, name="SUB"):
        new_btn.script_lines = self.script_lines                             # Copy the lines
        new_btn.coords = "(" + name + ")"                                    # set the name

        new_btn.symbols = New_symbol_table()
        new_btn.symbols[SYM_REPEATS] = self.symbols[SYM_REPEATS].copy()      # copy the repeats
        new_btn.symbols[SYM_ORIGINAL] = self.symbols[SYM_ORIGINAL].copy()    # and the original values
        new_btn.symbols[SYM_LABELS] = self.symbols[SYM_LABELS].copy()        # and the position of labels

        new_btn.is_async = self.is_async                                     # default is NOT async
        new_btn.validated = self.validated                                   # Need to copy over the validation flag (it should be True at this point)


    # check "self" for death notification
    def Check_self_kill(self, killfunc=None):
        if not self.thread:
           print ("expecting a thread in ", self.coords)
           return False

        if self.thread.kill.is_set():
            if self.running():                 # now we don't clear this, we need to ignore multiple reports
                print("[scripts] " + self.coords + " Recieved exit flag, script exiting...")
                #self.thread.kill.clear()
                if not self.is_async:
                    self.running(False)
                if killfunc:
                    killfunc()
                threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (self.x, self.y)).start()
            return True
        else:
            return False


    # Check_kill now checks the root button for death notifications
    def Check_kill(self, killfunc=None):
        return self.root.Check_self_kill(killfunc)


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
        # @@@ may be worth checking to see if it's a subroutine.  Because subroutines shouldn't use this
        global to_run

        if self.thread != None:
            if self.thread.is_alive():
                # @@@ The following code creates a problem if a script is looking for a second keypress
                # @@@ Maybe we need an option to make a script un-interruptable, or alternately require
                # @@@ *something* else (maybe ctrl-alt) to be pressed to allow the kill to take place.
                print("[scripts] " + self.coords + " Script already running, killing script....")
                self.thread.kill.set()
                return

        if self.invalid_on_load:  # don't schedule invalid code
            return

        if (self.x, self.y) in [l[1:] for l in to_run]:
            print("[scripts] " + self.coords + " Script already scheduled, unscheduling...")
            indexes = [i for i, v in enumerate(to_run) if ((v[1] == self.x) and (v[2] == self.y))]
            for index in indexes[::-1]:
                temp = to_run.pop(index)
            return

        if self.is_async:
            print("[scripts] " + self.coords + " Starting asynchronous script in background...")
            self.thread = threading.Thread(target=Run_script, args=())
            self.thread.kill = threading.Event()
            self.thread.start()
        elif not self.running():
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
            def split1(line):                     # just strip off a single (non-quoted) parameter
                param = line.split()[0]           # get the parameter
                line = line[len(param):].strip()  # strip off the parameter

                return param, line                # return the parameter and the rest of the line

            # grab a quoted string from the line passed.  Handles embedded quotes
            def strip_quoted(line):
                l2 = line                                 # a copy of the line we can edit
                q = l2[0]                                 # the first character is assumed to be a quote
                out = ''                                  # nothing to output yet
                l2 = l2[1:]                               # strip the quote from the string
                while len(l2) > 0:                        # while something remains in the line
                    if l2[0] == q:                        # if the quote is repeated
                        if len(l2) == 1 or l2[1] == ' ':  # and if it's the last character or followed by a space
                            l2 = l2[1:].strip()           # clean up the rest of the string
                            return True, out, l2          # return success
                        elif len(l2) > 1 and l2[1] == q:  # if we have 2 quotes in a row
                            out += q                      # then this is literally a quote
                            l2 = l2[2:]                   # but we need to clean up 2 characters this time
                        else:
                            return False, out, line       # any other quote-related stuff must be an error
                    else:                                 # for non-quote characters
                        out += l2[0]                      # we just pass them through to the output string
                        l2 = l2[1:]                       # and strip them off.

                return False, out, line                   # if we fall through, that's an error (no closing quote)

            # for all other commands, split on spaces
            if isinstance(command, command_base.Command_Basic):
                pline = line                              # something we can alter
                avl = command.auto_validate
                if avl != None and len(avl) > 0:
                    cmd, pline = split1(pline)            # the command is always a simple split
                    sline = [cmd]                         # add it to the return variable

                    n = -1                                # initialise parameter number pointer to one before the first
                    while len(pline) > 0:                 # keep stripping parameters while the line has some content
                        n += 1                            # point to the next parameters
                        if n < len(avl):                  # if this parameter has an auto-validation
                            av = avl[n]                   # then grab it
                        else:                             # otherwise the last parameter must allow for multiple values
                            av = avl[-1]                  # so take the last auto-validation

                        desc = av[AV_TYPE][AVT_DESC]      # get the description of the parameter type (not the description of the parameter!)

                        if (desc == PT_STR[AVT_DESC]) or (desc == PT_STRS[AVT_DESC]) or \
                           (desc == PT_ANY[AVT_DESC]):                                  # Is this one that wants quoted strings?
                            if pline[0] in ['"', "'", '`']:                             # if so, does it start with an acceptable quote?
                               if av[AV_VAR_OK] == AVV_REQD:                            # it's a problem if a variable is required
                                   return ('Error, quoted string not permitted for param #' + str(n+1), line) # literal not expected
                               else:
                                   ok, param, pline = strip_quoted(pline)               # otherwise we can strip off a quoted string
                                   if ok:                                               # and if that suceeded
                                       sline += ['\0'+param]                            # we'll add it as the parameter value.  Note we add a leading null to distinguish it from a variable
                                   else:
                                       return ('Error in quoted string for param #' + str(n+1), line) # This is generally something to do with the closing quote
                            else:                                                       # if we want a quoted string, but value doesn't start with a quote
                                if av[AV_VAR_OK] != AVV_NO:                             # Are we allowed to pass a variable?
                                    param = pline.split()[0]                            # then that's OK, just strip off an un-quoted string
                                    pline = pline[len(param):].strip()                  # and clean up the line (@@@ why not use strip1()??)
                                    if not variables.valid_var_name(param):             # but check it's a valid variable name
                                        if desc == PT_ANY[AVT_DESC]:                    # PT_ANY will accept non-variables as strings
                                            sline += [param]                            # we'll add it as the parameter value.  Note we don't add a leading "
                                                                                        # because we can try to interpret it as numeric later on
                                        else:
                                            return ('Error in variable for param #' + str(n+1), line) # if it's not a string and not a variable...
                                    else:
                                        sline += [param]                                # add it to the list of parameters if it's OK
                                else:
                                    return ('Error starting quoted string for param#' + str(n+1), line) # This is generally a missing initial quote

                        elif desc == PT_LINE[AVT_DESC]:    # the rest of the line (regardless of spaces)
                            sline += [line]                # just grab the rest of the line
                            pline = ""                     # and leave nothing behind

                        else:                              # in all other cases
                            param = pline.split(" ")[0]    # just strip the first unquoted parameter (@@@ why not use strip1()???)
                            sline += [param]
                            pline = pline[len(param):].strip()

                    return sline                           # return a list of command and parameters

                else:
                    # without autovalidate we just split on spaces
                    return line.split(" ")


    # run a script
    def Run_script(self):
        # @@@ maybe check we're not a subroutine (subroutines should not use this)
        lp_colors.updateXY(self.x, self.y)

        if self.Validate_script() != True:
           return

        print("[scripts] " + self.coords + " Now running script...")

        self.running(not self.is_async)

        cmd_txt = "RESET_REPEATS"                                         # before we run, we want to rest loop counters
        if cmd_txt in VALID_COMMANDS:
            command = VALID_COMMANDS[cmd_txt]
            command.Run(self, -1, [cmd_txt])

        if len(self.script_lines) > 0:
            self.running(True)

            def Main_logic(idx):                                          # the main logic to run a line of a script
                if self.Check_kill():                                     # first check to see if we've been asked to die
                    return idx + 1                                        # we just return the next line, @@@ returning -1 is better

                line = self.Line(idx)                                     # get the line of the script

                # Handle completely blank lines
                if line == "":
                    return idx + 1

                # Get the command text
                cmd_txt = self.Split_cmd_text(line)                       # Just get the command name leaving the line intact

                # Now get the command object
                if cmd_txt in VALID_COMMANDS:                             # make sure it's a valid command
                    command = VALID_COMMANDS[cmd_txt]                     # get the command object that will execute the command

                    split_line = self.Split_text(command, cmd_txt, line)  # get all the parameters as a list, including quoted parameters

                    if type(split_line) == tuple:                         # bad news if we get a tuple rather than a list
                        print("[scripts] " + self.coords + "    Error in: '" + cmd_txt + "' - "  + split_line[0] + ", skipping...")
                    else:
                        # now run the command
                        return command.Run(self, idx, split_line)         # otherwise we can ask the command to execute itself with the parameters we've parsed out
                else:
                    print("[scripts] " + self.coords + "    Invalid command: '" + cmd_txt + "', skipping...")

                return idx + 1                                            # defaut action is to ask for the next line

            run = True                                                    # flag that we're running
            idx = 0                                                       # point at the first line
            while run:                                                    # and while we're still running
                idx = Main_logic(idx)                                     # run the current line
                if (idx < 0) or (idx >= len(self.script_lines)):          # if the next line isn't valid
                    run = False                                           # then we're not going to keep running!

            if not self.is_async:                                         # async commands don't just end
                self.running(False)                                       # they have to say they're not running

            threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (self.x, self.y)).start() # queue up a request to update the button colours

        print("[scripts] " + self.coords + " Script ended.")              # and print (log?) that the script is complete


    # run a subroutine.  This is a simplified version of running a script because the script takes care of being scheduled and killed
    # @@@ this is so close to run_script that it probably should be merged with it at some point -- after I know its working
    def Run_subroutine(self):
        # @@@ maybe check that we **are** a subroutine first.  This is for subroutines ONLY
        if self.Validate_script() != True:                                # validates if not validated
           return

        print("[scripts] " + self.coords + " Now running subroutine ...")

        self.running(not self.is_async)                                   # @@@ not sure a async subroutine makes sense

        cmd_txt = "RESET_REPEATS"                                         # before we run, we want to rest loop counters
        if cmd_txt in VALID_COMMANDS:
            command = VALID_COMMANDS[cmd_txt]
            command.Run(self, -1, [cmd_txt])

        if len(self.script_lines) > 0:
            self.running(True)

            def Main_logic(idx):                                          # the main logic to run a line of a script
                if self.Check_kill():                                     # first check on our death notification
                    return idx + 1                                        # we just return the next line, @@@ returning -1 is better

                line = self.Line(idx)                                     # get the line of the script

                # Handle completely blank lines
                if line == "":
                    return idx + 1

                # Get the command text
                cmd_txt = self.Split_cmd_text(line)                       # Just get the command name leaving the line intact

                # Now get the command object
                if cmd_txt in VALID_COMMANDS:                             # make sure it's a valid command
                    command = VALID_COMMANDS[cmd_txt]                     # get the command object that will execute the command

                    split_line = self.Split_text(command, cmd_txt, line)  # get all the parameters as a list, including quoted parameters

                    if type(split_line) == tuple:                         # bad news if we get a tuple rather than a list
                        print("[scripts] " + self.coords + "    Error in: '" + cmd_txt + "' - "  + split_line[0] + ", skipping...")
                    else:
                        # now run the command
                        return command.Run(self, idx, split_line)         # otherwise we can ask the command to execute itself with the parameters we've parsed out
                else:
                    print("[scripts] " + self.coords + "    Invalid command: '" + cmd_txt + "', skipping...")

                return idx + 1                                            # defaut action is to ask for the next line

            run = True                                                    # flag that we're running
            idx = 0                                                       # point at the first line
            while run:                                                    # and while we're still running
                idx = Main_logic(idx)                                     # run the current line
                if (idx < 0) or (idx >= len(self.script_lines)):          # if the next line isn't valid
                    run = False                                           # then we're not going to keep running!

            if not self.is_async:                                         # async commands don't just end @@@ again, not sure this makes sense for subroutines
                self.running(False)                                       # they have to say they're not running

        print("[scripts] " + self.coords + " Subroutine ended.")          # and print (log?) that the script is complete


    # validating a script consists of doing the checks that we do prior to running, but
    # we won't run it afterwards.
    def Validate_script(self, full_validate=True):
        if not self.validated:                           # reset script-nominated colour before validation
            self.colour = None
            
        if self.validated or self.script_str == "":      # If valid or there is no script...
            self.validated = True
            return True                                  # ...validation succeeds!

        validation = self.Parse_script(full_parse=full_validate) # parse the script
        if validation == True:                           # If parsing is OK
            self.validated = full_validate               # Script is valid

            if len(self.script_lines) > 0:               # look for async header and set flag
                cmd_txt = self.Split_cmd_text(self.script_lines[0])
                self.is_async = cmd_txt in VALID_COMMANDS and \
                    isinstance(VALID_COMMANDS[cmd_txt], command_base.Command_Header) and \
                    VALID_COMMANDS[cmd_txt].is_async
        else:
            self.symbols = None                          # otherwise destroy symbol table
            return validation

        return self.validated                            # and tell us the result


# define the buttons structure here.  Note that subroutines will likely be a different sort of button, so this may change
buttons = [[Button(x, y, "") for y in range(9)] for x in range(9)]
to_run = []


# bind a button (Note that you can pass a validated button as script_str too)
def Bind(x, y, script_str, color):
    global to_run
    global buttons

    if isinstance(script_str, Button):       # if a button was passed
        btn = script_str                     # then we can skipp the button creation
        btn.x = x
        btn.y = y
        btn.Set_name(btn.name)               # force recalc of coords
    else:
        btn = Button(x, y, script_str)
        try:
            btn.Validate_script()
        except:
            pass

    buttons[x][y] = btn

    if (x, y) in [l[1:] for l in to_run]:    # If this button is scheduled to run...
        indexes = [i for i, v in enumerate(to_run) if ((v[1] == x) and (v[2] == y))]  #... create a list of locations in the list for this button
        for index in indexes[::-1]:          # and for each of them (in reverse order)
            temp = to_run.pop(index)         # Remove them from the list
        return # @@@ Why do we return here?

    schedule_script_bindable = lambda a, b: btn.Schedule_script() # @@@ What is this doing?

    lp_events.bind_func_with_colors(x, y, schedule_script_bindable, color)
    files.layout_changed_since_load = True   # Mark the layout as changed
    Redraw(x, y)


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
        files.layout_changed_since_load = True   # Mark the layout as changed
        return # WHY do we return here?

    if btn.thread != None:                   # If the button is actially executing
        thread.kill.set()                    # then kill it

    buttons[x][y] = btn                      # Clear the button script

    files.layout_changed_since_load = True   # Mark the layout as changed
    Redraw(x, y)


# swap details for two buttons
def Swap(x1, y1, x2, y2):
    global text

    color_1 = lp_colors.curr_colors[x1][y1]  # Colour for btn #1
    color_2 = lp_colors.curr_colors[x2][y2]  # Colour for btn #2

    btn_1 = buttons[x1][y1]                  # btn #1
    btn_2 = buttons[x2][y2]                  # btn #2

    Unbind(x1, y1)                           # Unbind #1
    if btn_2.script_str != "":               # If there is a script #2...
        Bind(x1, y1, btn_2, color_2)         # ...bind it to #1
    lp_colors.updateXY(x1, y1)               # Update the colours for btn #1

    Unbind(x2, y2)                           # Do the reverse for #2
    if btn_1.script_str != "":
        Bind(x2, y2, btn_1, color_1)
    lp_colors.updateXY(x2, y2)

    files.layout_changed_since_load = True   # Flag that the layout has changed


# Duplicate a button
def Copy(x1, y1, x2, y2):
    global buttons

    color_1 = lp_colors.curr_colors[x1][y1]  # Get colour of btn to be copied

    script_1 = buttons[x1][y1].script_str    # Get script to be copied

    Unbind(x2, y2)                           # Unbind the destination
    if script_1 != "":                       # If we're copying a button with a script...
        Bind(x2, y2, script_1, color_1)      # ...bind the details to the destination
    lp_colors.updateXY(x2, y2)               # Update the colours

    files.layout_changed_since_load = True   # Flag the layout as changed


# Delete a button
def Del(x1, y1, x2, y2):
    global buttons

    if x1 != x2 or y1 != y2:
        return

    Unbind(x2, y2)                           # Unbind the destination
    lp_colors.updateXY(x2, y2)               # Update the colours

    files.layout_changed_since_load = True   # Flag the layout as changed


# move a button
def Move(x1, y1, x2, y2):
    global buttons
    if (x1, y1) == (x2, y2):
        return

    color_1 = lp_colors.curr_colors[x1][y1]  # Get source button colour

    btn_1 = buttons[x1][y1]                  # Get source button script

    Unbind(x1, y1)                           # Unbind *both* buttons
    Unbind(x2, y2)

    if btn_1.script_str != "":               # If the source had a script...
        Bind(x2, y2, btn_1, color_1)         # ...bind it to the destination
    lp_colors.updateXY(x2, y2)               # Update the destination colours

    files.layout_changed_since_load = True   # And flag the layout as changed


# determine if a key is bound
def Is_bound(x, y):
    global buttons

    if buttons[x][y].script_str == "":       # If there is no script...
        return False                         # ...it's not bound
    else:
        return True                          # Otherwise it is


# kill all threads
def kill_all():
    global buttons
    global to_run

    to_run = []                              # nothing queued to run

    for x in range(9):                       # For each column...
        for y in range(9):                   # ...and row
            btn = buttons[x][y]
            if btn.thread is not None:       # If there is a thread...
                if btn.thread.isAlive():     # ...and if the thread is alive...
                    btn.thread.kill.set()    # ...kill it


# Unbind all keys.
def Unbind_all():
    lp_events.unbind_all()                   # Unbind all events

    for x in range(9):
        for y in range(9):
            Unbind(x, y)

    #text = [["" for y in range(9)] ] # Reienitialise all scripts to blank

    kill_all()                               # stop everything running

    files.curr_layout = None                 # There is no current layout
    files.layout_changed_since_load = False  # So mark it as unchanged


# Unload all subroutines.
def Unload_all(unload_subroutines=True):
    kill_all()                               # stop everything running

    subs = []                                # list of subroutines to remove
    for cmd in VALID_COMMANDS:               # for all the commands that exist
        if cmd.startswith(SUBROUTINE_PREFIX):# if this command is a subroutine
            subs += [cmd]                    # add the command to the list

    if unload_subroutines:
        for cmd in subs:                     # for each subroutine we've found
            Remove_command(cmd)              # remove it

    files.layout_changed_since_load = True   # mark layout as changed

    files.validate_all_buttons()             # ensure buttons are valid


