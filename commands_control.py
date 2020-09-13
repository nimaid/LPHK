import command_base, lp_events, scripts, variables
from constants import *

LIB = "cmds_ctrl" # name of this library (for logging)

# ##################################################
# ### CLASS Control_Comment                      ###
# ##################################################

# class that defines the comment command (single quote at beginning of line)
# this is special because it has some different handling in the main code
# to allow it to work without a space following it
class Control_Comment(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("-",  # the name of the command as you have to enter it in the code
            LIB,
            (),
            () )

        # this command does not have a standard list of fields, so we need to do some stuff manually
        self.valid_max_params = 32767      # There is no maximum, but this is a reasonable limit!
        self.valid_num_params = [0, None]  # zero or more is OK

        #self.run_states = [RS_INIT, RS_INFO, RS_FINAL] # No need to do anything at all for a comment, but let's display it
        #self.validation_states = []                    # And no validation either
            

scripts.add_command(Control_Comment())  # register the command


# ##################################################
# ### CLASS Control_Label                        ###
# ##################################################

# class that defines the LABEL command (a target of GOTO's etc)
class Control_Label(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("LABEL",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var    type       p1_val  p2_val 
            ("Label",      False, False, PT_TARGET, None,   None), 
            ),
            (
            # num params, format string                           (trailing comma is important)
            (1,           "    Label {1}"), 
            ) )

        #self.run_states = [RS_INIT, RS_INFO, RS_FINAL] # No need to do anything at all for a label, but let's display it
        #self.validation_states = [VS_PASS_1]           # We need to do pass 1 validation


scripts.add_command(Control_Label())  # register the command


# ##################################################
# ### CLASS Control_Goto_Label                   ###
# ##################################################

# class that defines the GOTO_LABEL command
class Control_Goto_Label(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("GOTO_LABEL",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var    type      conv  p1_val  p2_val 
            ("Label",      False, False, PT_LABEL, None,   None), 
            ),
            (
            # num params, format string                           (trailing comma is important)
            (1,           "    Goto label {1}"), 
            ) )


    def Process(self, idx, split_line, symbols, coords, is_async):
        return symbols[SYM_LABELS][symbols[SYM_PARAMS][1]]         # we simply return the line number the label is on


scripts.add_command(Control_Goto_Label())  # register the command


# ##################################################
# ### CLASS Control_If_Pressed_Goto_Label        ###
# ##################################################

# class that defines the IF_PRESSED_GOTO_LABEL command
class Control_If_Pressed_Goto_Label(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("IF_PRESSED_GOTO_LABEL",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var    type      conv  p1_val  p2_val 
            ("Label",      False, False, PT_LABEL, None,   None), 
            ),
            (
            # num params, format string                           (trailing comma is important)
            (1,           "    If pressed goto label {1}"), 
            ) )

        
    def Process(self, idx, split_line, symbols, coords, is_async):
        if lp_events.pressed[coords[BC_X]][coords[BC_Y]]:       # if key is pressed
            return symbols[SYM_LABELS][symbols[SYM_PARAMS][1]]  # and we return the line number the label is on


scripts.add_command(Control_If_Pressed_Goto_Label())  # register the command


# ##################################################
# ### CLASS Control_If_Unpressed_Goto_Label      ###
# ##################################################

# class that defines the IF_UNPRESSED_GOTO_LABEL command
class Control_If_Unpressed_Goto_Label(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("IF_UNPRESSED_GOTO_LABEL",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var    type      conv  p1_val  p2_val 
            ("Label",      False, False, PT_LABEL, None,   None), 
            ),
            (
            # num params, format string                           (trailing comma is important)
            (1,           "    If unpressed goto label {1}"), 
            ) )

        
    def Process(self, idx, split_line, symbols, coords, is_async):
        if not lp_events.pressed[coords[BC_X]][coords[BC_Y]]:   # if key is pressed
            return symbols[SYM_LABELS][symbols[SYM_PARAMS][1]]  # and we return the line number the label is on


scripts.add_command(Control_If_Unpressed_Goto_Label())  # register the command


# ##################################################
# ### CLASS Control_Repeat_Label                 ###
# ##################################################

# class that defines the REPEAT_LABEL command
class Control_Repeat_Label(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("REPEAT_LABEL",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var    type      p1_val                      p2_val 
            ("Label",      False, False, PT_LABEL, None,                       None), 
            ("Repeats",    False, False, PT_INT,   variables.Validate_gt_zero, None), 
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2,           "    Repeat label {1}, {2} times max"), 
            ) )

        
    def Partial_validate_step_pass_1(self, ret, idx, line, lines, split_line, symbols):
        ret = super().Partial_validate_step_pass_1(ret, idx, line, lines, split_line, symbols)
        
        if ret == None or ret == True:
            symbols[SYM_REPEATS][idx] = int(split_line[2])
            symbols[SYM_ORIGINAL][idx] = int(split_line[2])
            ret = True
            
        return ret

        
    def Partial_run_step_info(self, ret, idx, split_line, symbols, coords, is_async):
        # Oddly enough, we want the original info message too.
        ret = super().Partial_run_step_info(ret, idx, split_line, symbols, coords, is_async)
        
        if symbols[SYM_REPEATS][idx] > 0:
            print(AM_PREFIX.format(self.lib, coords[BC_TEXT], str(idx+1)) + "        " + str(symbols[SYM_REPEATS][idx]) + " repeats left.")
        else:
            print(AM_PREFIX.format(self.lib, coords[BC_TEXT], str(idx+1)) + "        No repeats left, not repeating.")

        return ret


    def Process(self, idx, split_line, symbols, coords, is_async):
        
        if symbols[SYM_REPEATS][idx] > 0:
            symbols[SYM_REPEATS][idx] = symbols[SYM_REPEATS][idx] - 1
            return symbols[SYM_LABELS][symbols[SYM_PARAMS][1]]
            
        return True


scripts.add_command(Control_Repeat_Label())  # register the command


# ##################################################
# ### CLASS Control_Repeat                       ###
# ##################################################

# class that defines the REPEAT command.  This operates more like a 
# traditional repeat/until by causing the code to repeat n times (rather than
# n+1, and it resets the counter at the end
class Control_Repeat(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("REPEAT")  # the name of the command as you have to enter it in the code

    def Validate(
        self,
        idx: int,              # The current line number
        line,                  # The current line
        lines,                 # The current script
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:       # in Pass 1 we can do general syntax check and gather symbol definitions
            if len(split_line) != 3:
                return ("Line:" + str(idx+1) + " - '" + split_line[0] + "' needs both a label name and how many times to repeat.", line)

            try:
                temp = int(split_line[2])
                if temp < 1:
                    return ("Line:" + str(idx+1) + " - " + split_line[0] + " requires a minimum of 1 repeat.", line)
                else:
                    symbols[SYM_REPEATS][idx] = int(split_line[2])-1
                    symbols[SYM_ORIGINAL][idx] = int(split_line[2])-1
            except:
               return ("Line:" + str(idx+1) + " - " + split_line[0] + " number of repeats '" + split_line[2] + "' not valid.", line)

        if pass_no == 2:       # in Pass 2 we can check to make sure referenced symbols exist
            if split_line[1] not in symbols[SYM_LABELS]:
                return ("Line:" + str(idx+1) + " - Target not found for " + self.name, line)

            if symbols[SYM_LABELS][split_line[1]] > idx:
                return ("Line:" + str(idx+1) + " - Target for " + self.name + " must preceed the command.", line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + LIB + "] " + coords[BC_TEXT] + "  Line:" + str(idx+1) + "    Repeat LABEL " + split_line[1] + " " + \
            split_line[2] + " times max")

        if symbols[SYM_REPEATS][idx] > 0:
            print("[" + LIB + "] " + coords[BC_TEXT] + "  Line:" + str(idx+1) + "        " + str(symbols[SYM_REPEATS][idx]) + " repeats left.")
            symbols[SYM_REPEATS][idx] -= 1
            return symbols[SYM_LABELS][split_line[1]]
        else:
            print("[" + LIB + "] " + coords[BC_TEXT] + "  Line:" + str(idx+1) + "        No repeats left, not repeating.")
            symbols[SYM_REPEATS][idx] = symbols[SYM_ORIGINAL][idx] # makes this behave like a normal loop
        return idx+1


scripts.add_command(Control_Repeat())  # register the command


# ##################################################
# ### CLASS Control_If_Pressed_Repeat_Label      ###
# ##################################################

# class that defines the IF_PRESSED_REPEAT_LABEL command
class Control_If_Pressed_Repeat_Label(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("IF_PRESSED_REPEAT_LABEL")  # the name of the command as you have to enter it in the code

    def Validate(
        self,
        idx: int,              # The current line number
        line,                  # The current line
        lines,                 # The current script
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:       # in Pass 1 we can do general syntax check and gather symbol definitions
            if len(split_line) != 3:
                return ("Line:" + str(idx+1) + " - '" + split_line[0] + "' needs both a label name and how many times to repeat.", line)

            try:
                temp = int(split_line[2])
                if temp < 1:
                    return ("Line:" + str(idx+1) + " - '" + split_line[0] + " requires a minimum of 1 repeat.", line)
                else:
                    symbols[SYM_REPEATS][idx] = int(split_line[2])
                    symbols[SYM_ORIGINAL][idx] = int(split_line[2])
            except:
                return ("Line:" + str(idx+1) + " - " + split_line[0] + " number of repeats '" + split_line[2] + "' not valid.", line)

        if pass_no == 2:       # in Pass 2 we can check to make sure referenced symbols exist
            if split_line[1] not in symbols[SYM_LABELS]:
                return ("Line:" + str(idx+1) + " - Target not found for " + self.name, line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + LIB + "] " + coords[BC_TEXT] + "  Line:" + str(idx+1) + "    If key is pressed repeat label " + split_line[1] + " " + split_line[2] + " times max")

        if not split_line[1] in symbols[SYM_LABELS]:          # The label should always exist
            print("Line:" + str(idx+1) + " - Missing LABEL '" + split_line[1] + "'")  # otherwise an error
            return -1
        else:
            if lp_events.pressed[coords[BC_X]][coords[BC_Y]]:
                if symbols[SYM_REPEATS][idx] > 0:
                    print("[" + LIB + "] " + coords[BC_TEXT] + "  Line:" + str(idx+1) + "        " + str(symbols[SYM_REPEATS][idx]) + " repeats left.")
                    symbols[SYM_REPEATS][idx] -= 1
                    return symbols[SYM_LABELS][split_line[1]]
                else:
                    print("[" + LIB + "] " + coords[BC_TEXT] + "  Line:" + str(idx+1) + "        No repeats left, not repeating.")

        return idx+1


scripts.add_command(Control_If_Pressed_Repeat_Label())  # register the command


# ##################################################
# ### CLASS Control_If_Pressed_Repeat            ###
# ##################################################

# class that defines the IF_PRESSED command.  This operates more like a 
# traditional repeat/until by causing the code to repeat n times (rather than
# n+1, and it resets the counter at the end
class Control_If_Pressed_Repeat(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("IF_PRESSED_REPEAT")  # the name of the command as you have to enter it in the code

    def Validate(
        self,
        idx: int,              # The current line number
        line,                  # The current line
        lines,                 # The current script
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:       # in Pass 1 we can do general syntax check and gather symbol definitions
            if len(split_line) != 3:
                return ("Line:" + str(idx+1) + " - '" + split_line[0] + "' needs both a label name and how many times to repeat.", line)

            try:
                temp = int(split_line[2])
                if temp < 1:
                    return ("Line:" + str(idx+1) + " - " + split_line[0] + " requires a minimum of 1 repeat.", line)
                else:
                    symbols[SYM_REPEATS][idx] = int(split_line[2])-1
                    symbols[SYM_ORIGINAL][idx] = int(split_line[2])-1
            except:
                return ("Line:" + str(idx+1) + " - " + split_line[0] + " number of repeats '" + split_line[2] + "' not valid.", line)

        if pass_no == 2:       # in Pass 2 we can check to make sure referenced symbols exist
            if split_line[1] not in symbols[SYM_LABELS]:
                return ("Line:" + str(idx+1) + " - Target not found for " + self.name, line)

            if symbols[SYM_LABELS][split_line[1]] > idx:
                return ("Line:" + str(idx+1) + " - Target for " + self.name + " must preceed the command.", line)


        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + LIB + "] " + coords[BC_TEXT] + "  Line:" + str(idx+1) + "    If key is pressed repeat " + split_line[1] + " " + split_line[2] + " times max")

        if not split_line[1] in symbols[SYM_LABELS]:          # The label should always exist
            print("Line:" + str(idx+1) + " - Missing LABEL '" + split_line[1] + "'")  # otherwise an error
            return -1
        else:
            if lp_events.pressed[coords[BC_X]][coords[BC_Y]]:
                if symbols[SYM_REPEATS][idx] > 0:
                    print("[" + LIB + "] " + coords[BC_TEXT] + "  Line:" + str(idx+1) + "        " + str(symbols[SYM_REPEATS][idx]) + " repeats left.")
                    symbols[SYM_REPEATS][idx] -= 1
                    return symbols[SYM_LABELS][split_line[1]]
                else:
                    print("[" + LIB + "] " + coords[BC_TEXT] + "  Line:" + str(idx+1) + "        No repeats left, not repeating.")
                    symbols[SYM_REPEATS][idx] = symbols[SYM_ORIGINAL][idx] # for a normal repeat statement

        return idx+1


scripts.add_command(Control_If_Pressed_Repeat())  # register the command


# ##################################################
# ### CLASS Control_If_Unpressed_Repeat_Label    ###
# ##################################################

# class that defines the IF_UNPRESSED_REPEAT_LABEL command.
class Control_If_Unpressed_Repeat_Label(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("IF_UNPRESSED_REPEAT_LABEL")  # the name of the command as you have to enter it in the code

    def Validate(
        self,
        idx: int,              # The current line number
        line,                  # The current line
        lines,                 # The current script
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:       # in Pass 1 we can do general syntax check and gather symbol definitions
            if len(split_line) != 3:
                return ("Line:" + str(idx+1) + " - '" + split_line[0] + "' needs both a label name and how many times to repeat.", line)

            try:
                temp = int(split_line[2])
                if temp < 1:
                    return ("Line:" + str(idx+1) + " - " + split_line[0] + " requires a minimum of 1 repeat.", line)
                    symbols[SYM_REPEATS][idx] = int(split_line[2])
                    symbols[SYM_ORIGINAL][idx] = int(split_line[2])
            except:
               return ("Line:" + str(idx+1) + " - " + split_line[0] + " number of repeats '" + split_line[2] + "' not valid.", line)

        if pass_no == 2:       # in Pass 2 we can check to make sure referenced symbols exist
            if split_line[1] not in symbols[SYM_LABELS]:
                return ("Line:" + str(idx+1) + " - Target not found for " + self.name, line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + LIB + "] " + coords[BC_TEXT] + "  Line:" + str(idx+1) + "    If key is not pressed repeat label " + split_line[1] + " " + split_line[2] + " times max")

        if not split_line[1] in symbols[SYM_LABELS]:          # The label should always exist
            print("  Line:" + str(idx+1) + " Missing LABEL '" + split_line[1] + "'")  # otherwise an error
            return -1
        else:
            if not lp_events.pressed[coords[BC_X]][coords[BC_Y]]:
                if symbols[SYM_REPEATS][idx] > 0:
                    print("[" + LIB + "] " + coords[BC_TEXT] + "  Line:" + str(idx+1) + "        " + str(symbols[SYM_REPEATS][idx]) + " repeats left.")
                    symbols[SYM_REPEATS][idx] -= 1
                    return symbols[SYM_LABELS][split_line[1]]
                else:
                    print("[" + LIB + "] " + coords[BC_TEXT] + "  Line:" + str(idx+1) + "        No repeats left, not repeating.")

        return idx+1


scripts.add_command(Control_If_Unpressed_Repeat_Label())  # register the command


# ##################################################
# ### CLASS Control_If_Unpressed_Repeat          ###
# ##################################################

# class that defines the IF_UNPRESSED_REPEAT command.  This operates more like a 
# traditional repeat/until by causing the code to repeat n times (rather than
# n+1, and it resets the counter at the end
class Control_If_Unpressed_Repeat(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("IF_UNPRESSED_REPEAT")  # the name of the command as you have to enter it in the code

    def Validate(
        self,
        idx: int,              # The current line number
        line,                  # The current line
        lines,                 # The current script
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:       # in Pass 1 we can do general syntax check and gather symbol definitions
            if len(split_line) != 3:
                return ("Line:" + str(idx+1) + " - '" + split_line[0] + "' needs both a label name and how many times to repeat.", line)

            try:
                temp = int(split_line[2])
                if temp < 1:
                    return ("Line:" + str(idx+1) + " - " + split_line[0] + " requires a minimum of 1 repeat.", line)
                    symbols[SYM_REPEATS][idx] = int(split_line[2])-1
                    symbols[SYM_ORIGINAL][idx] = int(split_line[2])-1
            except:
               return ("Line:" + str(idx+1) + " - " + split_line[0] + " number of repeats '" + split_line[2] + "' not valid.", line)

        if pass_no == 2:       # in Pass 2 we can check to make sure referenced symbols exist
            if split_line[1] not in symbols[SYM_LABELS]:
                return ("Line:" + str(idx+1) + " - Target not found for " + self.name, line)

            if symbols[SYM_LABELS][split_line[1]] > idx:
                return ("Line:" + str(idx+1) + " - Target for " + self.name + " must preceed the command.", line)


        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + LIB + "] " + coords[BC_TEXT] + "  Line:" + str(idx+1) + "    If key is not pressed repeat " + split_line[1] + " " + split_line[2] + " times max")

        if not split_line[1] in symbols[SYM_LABELS]:          # The label should always exist
            print("missing LABEL '" + split_line[1] + "'")  # otherwise an error
            return -1
        else:
            if not lp_events.pressed[coords[BC_X]][coords[BC_Y]]:
                if symbols[SYM_REPEATS][idx] > 0:
                    print("[" + LIB + "] " + coords[BC_TEXT] + "  Line:" + str(idx+1) + "        " + str(symbols[SYM_REPEATS][idx]) + " repeats left.")
                    symbols[SYM_REPEATS][idx] -= 1
                    return symbols[SYM_LABELS][split_line[1]]
                else:
                    print("[" + LIB + "] " + coords[BC_TEXT] + "  Line:" + str(idx+1) + "        No repeats left, not repeating.")
                    symbols[SYM_REPEATS][idx] = symbols[SYM_ORIGINAL][idx] # to behave more normal

        return idx+1


scripts.add_command(Control_If_Unpressed_Repeat())  # register the command


# ##################################################
# ### CLASS Control_Reset_Repeats                ###
# ##################################################

# class that defines the RESET_REPEATS command
class Control_Reset_Repeats(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("RESET_REPEATS")  # the name of the command as you have to enter it in the code

    def Validate(
        self,
        idx: int,              # The current line number
        line,                  # The current line
        lines,                 # The current script
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if len(split_line) > 1:
            return ("Line:" + str(idx+1) + " - Too many arguments for command '" + split_line[0] + "'.", line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + LIB + "] " + coords[BC_TEXT] + "  Line:" + str(idx+1) + "    Reset all repeats")

        for i in symbols[SYM_REPEATS]:
             symbols[SYM_REPEATS][i] = symbols[SYM_ORIGINAL][i]

        return idx+1


scripts.add_command(Control_Reset_Repeats())  # register the command


