import command_base, lp_events, scripts, variables
from constants import *

LIB = "cmds_ctrl" # name of this library (for logging)

# ##################################################
# ### CLASS Control_Comment                      ###
# ##################################################

# class that defines the comment command (single quote at beginning of line)
# this is special because it has some different handling in the main code
# to allow it to work without a space following it
class Control_Comment(command_base.Command_Text_Basic):
    def __init__(
        self, 
        ):

        super().__init__("-",  # the name of the command as you have to enter it in the code
            LIB,
            "-" )


scripts.Add_command(Control_Comment())  # register the command


# ##################################################
# ### CLASS Control_Label                        ###
# ##################################################

# class that defines the LABEL command (a target of GOTO's etc)
class Control_Label(command_base.Command_Basic):
    def __init__(        
        self 
        ):

        super().__init__(
            "LABEL",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var     type       p1_val  p2_val 
            ("Label",      False, AVV_NO, PT_TARGET, None,   None), 
            ),
            (
            # num params, format string                           (trailing comma is important)
            (1,           "    Label {1}"), 
            ) )


scripts.Add_command(Control_Label())  # register the command


# ##################################################
# ### CLASS Control_Flow_Basic                   ###
# ##################################################

# class that defines an object that can handle flow control
#
# THIS IS NOT REGISTERED.  IT IS AN ANCESTOR CLASS FOR OTHER MORE POWERFUL COMMANDS
class Control_Flow_Basic(command_base.Command_Basic):
    def __init__(
        self, 
        name: str,                   # The name of the command (what you put in the script)
        lib=LIB,
        auto_validate=None,          # Definition of the input parameters
        auto_message=None,           # Definition of the message format
        invalid_message=None,        # Info message if invalid  
        valid_function=None,         # Test to be performed to determine validity
        label_preceeds=False,        # must the label preceed this line
        reset=False,                 # do we do reset at end of loop?
        loop_val_init_function=None, # How to initialize the loop counter
        next_function=None,          # Passed the current value, return the next
        test_function=None           # Test to be performed before looping None = loop always
        ):

        super().__init__(name,  # the name of the command as you have to enter it in the code
            lib,
            auto_validate,
            auto_message);
            
        # note that it is safe to have these extra variables in the class, as they are
        # constant for a given child class.
        self.invalid_message = invalid_message
        self.valid_function = valid_function
        self.label_preceeds = label_preceeds
        self.reset = reset
        self.loop_val_init_function = loop_val_init_function
        self.next_function = next_function
        self.test_function = test_function


    def Partial_validate_step_pass_1(self, ret, btn, idx, split_line):
        ret = super().Partial_validate_step_pass_1(ret, btn, idx, split_line)
        
        if ret == None or ((type(ret) == bool) and ret):
            if self.loop_val_init_function:
                self.loop_val_init_function(btn, idx, split_line)
                ret = True
            
        return ret


    def Partial_validate_step_pass_2(self, ret, btn, idx, split_line):
        ret = super().Partial_validate_step_pass_2(ret, btn, idx, split_line)
        
        if (ret == None or ((type(ret) == bool) and ret)):
            if self.label_preceeds and btn.symbols[SYM_LABELS][split_line[1]] > idx:
                ret = ("Line:" + str(idx+1) + " - Target for " + self.name + " (" + split_line[1] + ") must preceed the command.", btn.Line(idx))
            
        return ret

        
    def Partial_run_step_info(self, ret, btn, idx, split_line):
        ret = super().Partial_run_step_info(ret, btn, idx, split_line)
        
        if self.valid_function == None or self.valid_function(btn):           # if no validation function, or it returns true, continue
            if self.test_function and self.next_function:
                if btn.symbols[SYM_REPEATS][idx] > 0:
                    print(AM_PREFIX.format(self.lib, btn.coords, str(idx+1)) + "        " + str(btn.symbols[SYM_REPEATS][idx]) + " repeats left.")
                else:
                    print(AM_PREFIX.format(self.lib, btn.coords, str(idx+1)) + "        No repeats left, not repeating.")        
        else:
            print(self.invalid_message)

        return ret
        

    def Process(self, btn, idx, split_line):
        ret = idx+1    # if all else fails!

        if self.valid_function == None or self.valid_function(btn): # if no validation function, or it returns true, continue
            
            if self.next_function:                                         # if we can calc the next value of the loop
                val = btn.symbols[SYM_REPEATS][idx]                        # get this value
                btn.symbols[SYM_REPEATS][idx] = self.next_function(val)    # and calculate the next
            
            if not (self.test_function or self.next_function):             # it's either both or none at the moment, if neither
                ret = btn.symbols[SYM_LABELS][btn.symbols[SYM_PARAMS][1]]  # this is unconditional
            elif (self.test_function and self.next_function):              # if both, then we can do the test
                if self.test_function(val-1):
                    ret = btn.symbols[SYM_LABELS][btn.symbols[SYM_PARAMS][1]]  # jump if test succeeds
                else:
                    if self.reset:
                        self.Reset(btn, idx)                               # potential reset if it doesn't

        return ret
            

    def Valid_key_pressed(self, btn):
        return lp_events.pressed[btn.x][btn.y]
        
        
    def Valid_key_unpressed(self, btn):
        return not self.Valid_key_pressed(btn)
        
        
    def Test_func_ge_zero(self, val):
        return val >= 0
        
        
    def Next_decrement(self, val):
        return val-1
        
        
    def Reset(self, btn, idx):
        btn.symbols[SYM_REPEATS][idx] = btn.symbols[SYM_ORIGINAL][idx]
    

    def Init_n(self, btn, idx, split_line):
        btn.symbols[SYM_ORIGINAL][idx] = int(split_line[2])
        self.Reset(btn, idx)
    

    def Init_n_minus_1(self, btn, idx, split_line):
        btn.symbols[SYM_ORIGINAL][idx] = int(split_line[2])-1
        self.Reset(btn, idx)


# ##################################################
# ### CLASS Control_Goto_Label                   ###
# ##################################################

# class that defines the GOTO_LABEL command
class Control_Goto_Label(Control_Flow_Basic):
    def __init__(
        self 
        ):

        super().__init__(
            "GOTO_LABEL",   # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var     type      p1_val  p2_val 
            ("Label",      False, AVV_NO, PT_LABEL, None,   None), 
            ),
            (
            # num params, format string                           (trailing comma is important)
            (1,           "    Goto label {1}"), 
            ) )  # don't even need the additional parameters!


scripts.Add_command(Control_Goto_Label())  # register the command


# ##################################################
# ### CLASS Control_If_Pressed_Goto_Label        ###
# ##################################################

# class that defines the IF_PRESSED_GOTO_LABEL command
class Control_If_Pressed_Goto_Label(Control_Flow_Basic):
    def __init__(
        self 
        ):

        super().__init__(
            "IF_PRESSED_GOTO_LABEL",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # desc         opt    var     type      p1_val                      p2_val 
            ("label",      False, AVV_NO, PT_LABEL, None,                       None), 
            ),
            (
            # num params, format string                           (trailing comma is important)
            (1,           "    if pressed goto label {1}"), 
            ),
            "the button is not pressed",
            self.Valid_key_pressed
            )


scripts.Add_command(Control_If_Pressed_Goto_Label())  # register the command


# ##################################################
# ### CLASS Control_If_Unpressed_Goto_Label      ###
# ##################################################

# class that defines the IF_UNPRESSED_GOTO_LABEL command
class Control_If_Unpressed_Goto_Label(Control_Flow_Basic):
    def __init__(
        self 
        ):

        super().__init__(
            "IF_UNPRESSED_GOTO_LABEL",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # desc         opt    var     type      p1_val                      p2_val 
            ("label",      False, AVV_NO, PT_LABEL, None,                       None), 
            ),
            (
            # num params, format string                           (trailing comma is important)
            (1,           "    if unpressed goto label {1}"), 
            ),
            "the button is pressed",
            self.Valid_key_unpressed
            )


scripts.Add_command(Control_If_Unpressed_Goto_Label())  # register the command


# ##################################################
# ### CLASS Control_Repeat_Label                 ###
# ##################################################

# class that defines the REPEAT_LABEL command
class Control_Repeat_Label(Control_Flow_Basic):
    def __init__(
        self 
        ):

        super().__init__(
            "REPEAT_LABEL",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # desc         opt    var     type      p1_val                      p2_val 
            ("Label",      False, AVV_NO, PT_LABEL, None,                       None), 
            ("Repeats",    False, AVV_NO, PT_INT,   variables.Validate_gt_zero, None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2,           "    Repeat label {1}, {2} times max"), 
            ),
            None,
            None,
            False,
            False,
            self.Init_n,
            self.Next_decrement,
            self.Test_func_ge_zero
            )


scripts.Add_command(Control_Repeat_Label())  # register the command


# ##################################################
# ### CLASS Control_Repeat                       ###
# ##################################################

# class that defines the REPEAT command.  This operates more like a 
# traditional repeat/until by causing the code to repeat n times (rather than
# n+1, and it resets the counter at the end
class Control_Repeat(Control_Flow_Basic):
    def __init__(
        self 
        ):

        super().__init__(
            "REPEAT",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # desc         opt    var     type      p1_val                      p2_val 
            ("Label",      False, AVV_NO, PT_LABEL, None,                       None), 
            ("Repeats",    False, AVV_NO, PT_INT,   variables.Validate_gt_zero, None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2, "    Repeat {1}, {2} times max"), 
            ),
            None,
            None,
            True,
            True,
            self.Init_n_minus_1,
            self.Next_decrement,
            self.Test_func_ge_zero
            )


scripts.Add_command(Control_Repeat())  # register the command


# ##################################################
# ### CLASS Control_If_Pressed_Repeat_Label      ###
# ##################################################

# class that defines the IF_PRESSED_REPEAT_LABEL command.
class Control_If_Pressed_Repeat_Label(Control_Flow_Basic):
    def __init__(
        self 
        ):

        super().__init__(
            "IF_PRESSED_REPEAT_LABEL",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # desc         opt    var     type      p1_val                      p2_val 
            ("label",      False, AVV_NO, PT_LABEL, None,                       None), 
            ("Repeats",    False, AVV_NO, PT_INT,   variables.Validate_gt_zero, None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2, "    If key is pressed repeat label {1}, {2} times max"), 
            ),
            "the button is umpressed",
            self.Valid_key_pressed,
            False,
            False,
            self.Init_n,
            self.Next_decrement,
            self.Test_func_ge_zero
            )


scripts.Add_command(Control_If_Pressed_Repeat_Label())  # register the command


# ##################################################
# ### CLASS Control_If_Pressed_Repeat            ###
# ##################################################

# class that defines the IF_PRESSED command.  This operates more like a 
# traditional repeat/until by causing the code to repeat n times (rather than
# n+1, and it resets the counter at the end
class Control_If_Pressed_Repeat(Control_Flow_Basic):
    def __init__(
        self 
        ):

        super().__init__(
            "IF_PRESSED_REPEAT_LABEL",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # desc         opt    var     type      p1_val                      p2_val 
            ("label",      False, AVV_NO, PT_LABEL, None,                       None), 
            ("Repeats",    False, AVV_NO, PT_INT,   variables.Validate_gt_zero, None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2, "    If key is not pressed repeat label {1}, {2} times max"), 
            ),
            "the button is not pressed",
            self.Valid_key_pressed,
            True,
            True,
            self.Init_n,
            self.Next_decrement,
            self.Test_func_ge_zero
            )


scripts.Add_command(Control_If_Pressed_Repeat())  # register the command


# ##################################################
# ### CLASS Control_If_Unpressed_Repeat_Label    ###
# ##################################################

# class that defines the IF_UNPRESSED_REPEAT_LABEL command.
class Control_If_Unpressed_Repeat_Label(Control_Flow_Basic):
    def __init__(
        self 
        ):

        super().__init__(
            "IF_UNPRESSED_REPEAT_LABEL",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # desc         opt    var     type      p1_val                      p2_val 
            ("label",      False, AVV_NO, PT_LABEL, None,                       None), 
            ("Repeats",    False, AVV_NO, PT_INT,   variables.Validate_gt_zero, None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2, "    If key is not pressed repeat label {1}, {2} times max"), 
            ),
            "the button is pressed",
            self.Valid_key_unpressed,
            False,
            False,
            self.Init_n,
            self.Next_decrement,
            self.Test_func_ge_zero
            )


scripts.Add_command(Control_If_Unpressed_Repeat_Label())  # register the command


# ##################################################
# ### CLASS Control_If_Unpressed_Repeat          ###
# ##################################################

# class that defines the IF_UNPRESSED_REPEAT command.  This operates more like a 
# traditional repeat/until by causing the code to repeat n times (rather than
# n+1, and it resets the counter at the end
class Control_If_Unpressed_Repeat(Control_Flow_Basic):
    def __init__(
        self 
        ):

        super().__init__(
            "IF_UNPRESSED_REPEAT",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # desc         opt    var     type      p1_val                      p2_val 
            ("label",      False, AVV_NO, PT_LABEL, None,                       None), 
            ("Repeats",    False, AVV_NO, PT_INT,   variables.Validate_gt_zero, None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2, "    If key is not pressed repeat {1}, {2} times max"), 
            ),
            "the button is pressed",
            self.Valid_key_unpressed,
            True,
            True,
            self.Init_n_minus_1,
            self.Next_decrement,
            self.Test_func_ge_zero
            )
    

scripts.Add_command(Control_If_Unpressed_Repeat())  # register the command


# ##################################################
# ### CLASS Control_Reset_Repeats                ###
# ##################################################

# class that defines the RESET_REPEATS command
#
# Here's a command that could just be defined into action, but the 
# basic implementation using the low level interface is so simple.
class Control_Reset_Repeats(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("RESET_REPEATS")  # the name of the command as you have to enter it in the code


    def Validate(
        self,
        btn,
        idx: int,              # The current line number
        split_line,            # The current line, split
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if len(split_line) > 1:
            return ("Line:" + str(idx+1) + " - Too many arguments for command '" + split_line[0] + "'.", btn.Line(idx))

        return True


    def Run(
        self,
        btn,
        idx: int,              # The current line number
        split_line             # The current line, split
        ):

        print("[" + LIB + "] " + btn.coords + "  Line:" + str(idx+1) + "    Reset all repeats")

        for i in btn.symbols[SYM_REPEATS]:
             btn.symbols[SYM_REPEATS][i] = btn.symbols[SYM_ORIGINAL][i]

        return idx+1


scripts.Add_command(Control_Reset_Repeats())  # register the command


# ##################################################
# ### CLASS Control_End                          ###
# ##################################################

# class that defines the END command
#
# This command simply ends the current script.  I'm going to be working on subroutines, so this is a good
# start.  The parameters to this command are simply the message it will print.
# This is really like a comment that returns the next line as -1
class Control_End(command_base.Command_Text_Basic):
    def __init__(
        self, 
        ):

        super().__init__("END",  # the name of the command as you have to enter it in the code
            LIB,
            "SCRIPT ENDED" )
       
       
    def Process(self, btn, idx, split_line):
        return -1


scripts.Add_command(Control_End())  # register the command


# ##################################################
# ### CLASS Control_Abort                        ###
# ##################################################

# class that defines the ABORT command
#
# This is effectively the same as END, but the message (and the implication) is different
class Control_Abort(Control_End):
    def __init__(
        self, 
        ):
        
        super().__init__()

        self.name = "ABORT"
        self.info_msg = "SCRIPT ABORTED"


scripts.Add_command(Control_Abort())  # register the command
