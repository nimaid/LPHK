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

        super().__init__("-, Comment",
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
            "LABEL, Target for jumps (goto, loops, etc)",
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
        ret = super().Partial_validate_step_pass_1(ret, btn, idx, split_line)     # perform the original pass 1 validation

        if ret == None or ((type(ret) == bool) and ret):                          # if the original validation hasn't raised an error
            if self.loop_val_init_function:                                       # and if we have a validation
                self.loop_val_init_function(btn, idx, split_line)                 # then perform the additional validation
                ret = True                                                        # not sure why we always return true @@@

        return ret


    def Partial_validate_step_pass_2(self, ret, btn, idx, split_line):
        ret = super().Partial_validate_step_pass_2(ret, btn, idx, split_line)     # perform the original pass 2 validation

        if (ret == None or ((type(ret) == bool) and ret)):                        # if the original validation hasn't raised an error
            if self.label_preceeds and btn.symbols[SYM_LABELS][split_line[1]] > idx: # If the label must preceed the command, ensure that it is so!
                ret = ("Line:" + str(idx+1) + " - Target for " + self.name + " (" + split_line[1] + ") must preceed the command.", btn.Line(idx))

        return ret


    def Partial_run_step_info(self, ret, btn, idx, split_line):
        ret = super().Partial_run_step_info(ret, btn, idx, split_line)        # perform the original notification of a partial execution

        if self.valid_function == None or self.valid_function(btn):           # if no validation function, or it returns true, continue
            if self.test_function and self.next_function:                     # if there is a test function and it returns true
                if btn.symbols[SYM_REPEATS][idx] > 0:                         # if repeats remain
                    print(AM_PREFIX.format(self.lib, btn.coords, str(idx+1)) + "        " + str(btn.symbols[SYM_REPEATS][idx]) + " repeats left.")
                else:                                                         # if no repeats remain
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
        return lp_events.pressed[btn.x][btn.y]                         # Is the button pressed


    def Valid_key_unpressed(self, btn):
        return not self.Valid_key_pressed(btn)                         # is the button unpressed


    def Test_func_ge_zero(self, val):                                  # testing for a value >= 0
        return val >= 0


    def Next_decrement(self, val):                                     # Standard decrement function
        return val-1


    def Reset(self, btn, idx):
        btn.symbols[SYM_REPEATS][idx] = btn.symbols[SYM_ORIGINAL][idx] # standard function to reset a loop counter


    def Init_n(self, btn, idx, split_line):
        btn.symbols[SYM_ORIGINAL][idx] = int(split_line[2])            # set repeats to n (will cause n+1 loop executions)
        self.Reset(btn, idx)


    def Init_n_minus_1(self, btn, idx, split_line):                    # set repeats to n-1 (will cause n loop executions)
        btn.symbols[SYM_ORIGINAL][idx] = int(split_line[2])-1
        self.Reset(btn, idx)

    # do our best to make a and b comparable
    def Comparable(self, a, b):

        def either_is(a, b, c_type):
            return type(a) == c_type or type(b) == c_type

        a = self.strip_null(a)                                         # remove leading null indicating string literal
        b = self.strip_null(b)

        if isinstance(a, type(b)) or isinstance(b, type(a)):           # probably comparable
            return a, b

        if either_is(a, b, str):
            if either_is(a, b, int):
                try:
                    return int(a), int(b)
                except:
                    None

                try:
                    return float(a), float(b)
                except:
                    None

                try:
                    return str(a), str(b)
                except:
                    None
            elif either_is(a, b, float):
                try:
                    return float(a), float(b)
                except:
                    None

                try:
                    return str(a), str(b)
                except:
                    None
        elif either_is(a, b, float):
            if either_is(a, b, int):
                pass
            else:
                try:
                    return float(a), float(b)
                except:
                    None

                try:
                    return str(a), str(b)
                except:
                    None

        return a, b

    def a_eq_b(self, btn, first=2, second=3):
        a = self.Get_param(btn, first)
        b = self.Get_param(btn, second)

        a, b = self.Comparable(a, b)   # try our best to make a and b comparable

        try:
            if a == b:
                return True

        except:
            return False


    def a_ne_b(self, btn, first=2, second=3):
        a = self.Get_param(btn, first)
        b = self.Get_param(btn, second)

        a, b = self.Comparable(a, b)   # try our best to make a and b comparable

        try:
            if a != b:
                return True

        except:
            return True                  # this is an exception.  If we can't compare they can't be equal!


    def a_gt_b(self, btn, first=2, second=3):
        a = self.Get_param(btn, first)
        b = self.Get_param(btn, second)

        a, b = self.Comparable(a, b)   # try our best to make a and b comparable

        try:
            if a > b:
                return True

        except:
            return False


    def a_lt_b(self, btn, first=2, second=3):
        a = self.Get_param(btn, first)
        b = self.Get_param(btn, second)

        a, b = self.Comparable(a, b)   # try our best to make a and b comparable

        try:
            if a < b:
                return True

        except:
            return False


    def a_ge_b(self, btn, first=2, second=3):
        a = self.Get_param(btn, first)
        b = self.Get_param(btn, second)

        a, b = self.Comparable(a, b)   # try our best to make a and b comparable

        try:
            if a >= b:
                return True

        except:
            return False


    def a_le_b(self, btn, first=2, second=3):
        a = self.Get_param(btn, first)
        b = self.Get_param(btn, second)

        a, b = self.Comparable(a, b)   # try our best to make a and b comparable

        try:
            if a <= b:
                return True

        except:
            return False


# ##################################################
# ### CLASS Control_Goto_Label                   ###
# ##################################################

# class that defines the GOTO_LABEL command
class Control_Goto_Label(Control_Flow_Basic):
    def __init__(
        self
        ):

        super().__init__(
            "GOTO_LABEL, Unconditional jump to label",
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
# ### CLASS IF                                   ###
# ##################################################

# constants for comparisons
COMP_EQ     = ['EQ', '==', '=']
COMP_NE     = ['NE', "!=", "<>"]
COMP_GT     = ['GT', '>']
COMP_GE     = ['GE', '>=']
COMP_LT     = ['LT', '<']
COMP_LE     = ['LE', '<=']

COMPG_ALL = COMP_EQ + COMP_NE + COMP_GT + COMP_GE + COMP_LT + COMP_LE

# constants for action
ACT_GOTO    = ['GOTO']
ACT_RETURN  = ['RETURN']
ACT_END     = ['END']
ACT_ABORT   = ['ABORT']

ACTG_ALL = ACT_GOTO + ACT_RETURN + ACT_END + ACT_ABORT

# class that defines the IF command
class Control_If(Control_Flow_Basic):
    def __init__(
        self
        ):

        super().__init__(
            "IF, Tests a pair of values and takes an action if the result is True",
            LIB,
            (
            # Desc         Opt    Var     type      p1_val  p2_val
            ("A",          False, AVV_YES,PT_ANY,   None,   None), # a and b can be anything!
            ("Comp",       False, AVV_NO, PT_WORD,  None,   None), # comparison operator
            ("B",          False, AVV_YES,PT_ANY,   None,   None), # a and b can be anything!
            ("Action",     False, AVV_NO, PT_WORD,  None,   None), # GOTO, ABORT, RETURN, END
            ("Label",      True,  AVV_NO, PT_LABEL, None,   None), # required for GOTO
            ),
            (
            # num params, format string                           (trailing comma is important)
            (4,           "    if {1} {2} {3} then {4}"),
            (5,           "    if {1} {2} {3} then {4} {5}"),
            ),
            )

        self.doc = ["Based on the result of a comparison of 2 values, jump to a label "
                    "or RETURN/END/ABORT.",
                    "",
                    "The 2 values passed can be either constants or variables, and the "
                    "comparison operators are:",
                    "",
                    "~19",
                    "    EQ, =, or ==   Test the values for equality",
                    "    NE, !=, or <>  Test the values for inequality",
                    "    LE, or <=      Test if the first value is less than or equal to the second",
                    "    LT, or <       Test if the first value is less than the second",
                    "    GT, or >       Test if the first value is greater than the second",
                    "    GE, or >=      Test if the first value is greater than or equal to the second",
                    "~",
                    "If the result of th test is True, the `Action` is performed.  The actions are:",
                    ""
                    "~19",
                    "    GOTO `Label`   Transfer control to the label `Label`",
                    "    RETURN         Return from a subroutine or end a button script",
                    "    END            Stop execution of the script now (even from within a subroutine)",
                    "    ABORT          As for `END` but with the implication of error",
                    "~",
                    "",
                    "The `Label` parameter is required for `GOTO` action, and prohibited for other actions."]


    def Process(self, btn, idx, split_line):
        comp = self.Get_param(btn, 2)

        if comp in COMP_EQ:
            comp_p = self.a_eq_b
        elif comp in COMP_NE:
            comp_p = self.a_ne_b
        elif comp in COMP_GE:
            comp_p = self.a_ge_b
        elif comp in COMP_GT:
            comp_p = self.a_gt_b
        elif comp in COMP_LE:
            comp_p = self.a_le_b
        elif comp in COMP_LT:
            comp_p = self.a_lt_b

        res = comp_p(btn, 1)

        if not res:
            return idx+1

        act = self.Get_param(btn, 4)

        if act in ACT_RETURN:
            return -1
        elif act in ACT_END:
            btn.root.thread.kill.set()
            return -1
        elif act in ACT_ABORT:
            btn.root.thread.kill.set()
            return -1
        else:
            # perform a goto
            ret = btn.symbols[SYM_LABELS][btn.symbols[SYM_PARAMS][5]]
            return ret


    def Partial_validate_step_pass_1(self, ret, btn, idx, split_line):
        ret = super().Partial_validate_step_pass_1(ret, btn, idx, split_line)     # perform the original pass 1 validation

        if ret == None or ((type(ret) == bool) and ret):                          # if the original validation hasn't raised an error
            if not split_line[2] in COMPG_ALL:                                    # invalid subcommand
                c_ok = ', '.join(COMPG_ALL[:-1]) + ', or ' + COMPG_ALL[-1]
                s_err = f"Invalid comparison operator {split_line[2]} when expecting {c_ok}."
                return (s_err, btn.Line(idx))

            if not split_line[4] in ACTG_ALL:                                    # invalid subcommand
                c_ok = ', '.join(ACTG_ALL[:-1]) + ', or ' + ACTG_ALL[-1]
                s_err = f"Invalid action {split_line[4]} when expecting {c_ok}."
                return (s_err, btn.Line(idx))

            if (split_line[4] in ACT_GOTO) and (len(split_line) < 6):
                s_err = f"{split_line[4]} requires a label."
                return (s_err, btn.Line(idx))

            if not (split_line[4] in ACT_GOTO) and (len(split_line) >= 6):
                s_err = f"{split_line[4]} can not have a label ({split_line[6]})."
                return (s_err, btn.Line(idx))

        return ret


scripts.Add_command(Control_If())  # register the command


# ##################################################
# ### CLASS ASSERT                               ###
# ##################################################

# class that defines the ASSERT command
class Control_Assert(Control_Flow_Basic):
    def __init__(
        self
        ):

        super().__init__(
            "ASSERT, IF x comp y is not true, abort with message",
            LIB,
            (
            # Desc         Opt    Var     type      p1_val  p2_val
            ("A",          False, AVV_YES,PT_ANY,   None,   None), # a and b can be anything!
            ("comp",       False, AVV_NO, PT_WORD,  None,   None), # comparison operator
            ("B",          False, AVV_YES,PT_ANY,   None,   None), # a and b can be anything!
            ("Message",    True,  AVV_NO, PT_STR,   None,   None), # abort message
            ),
            (
            # num params, format string                           (trailing comma is important)
            (3,           "    if {1} {2} {3} fails, then abort"),
            (4,           "    if {1} {2} {3} fails, then abort with message {4}"),
            ),
            )


    def Process(self, btn, idx, split_line):
        comp = self.Get_param(btn, 2)

        if comp in COMP_EQ:
            comp_p = self.a_eq_b
        elif comp in COMP_NE:
            comp_p = self.a_ne_b
        elif comp in COMP_GE:
            comp_p = self.a_ge_b
        elif comp in COMP_GT:
            comp_p = self.a_gt_b
        elif comp in COMP_LE:
            comp_p = self.a_le_b
        elif comp in COMP_LT:
            comp_p = self.a_lt_b

        res = comp_p(btn, 1)

        if res:
            return idx+1

        message = self.Get_param(btn, 4)
        print(f'ASSERT `{self.Get_param(btn, 1)}` {comp} `{self.Get_param(btn, 3)}` fails: {message}')

        btn.root.thread.kill.set()
        return -1


    def Partial_validate_step_pass_1(self, ret, btn, idx, split_line):
        ret = super().Partial_validate_step_pass_1(ret, btn, idx, split_line)     # perform the original pass 1 validation

        if ret == None or ((type(ret) == bool) and ret):                          # if the original validation hasn't raised an error
            if not split_line[2] in COMPG_ALL:                                    # invalid subcommand
                c_ok = ', '.join(COMPG_ALL[:-1]) + ', or ' + COMPG_ALL[-1]
                s_err = f"Invalid comparison operator {split_line[2]} when expecting {c_ok}."
                return (s_err, btn.Line(idx))

        return ret


scripts.Add_command(Control_Assert())  # register the command


# ##################################################
# ### CLASS IF_EQ_GOTO                           ###
# ##################################################

# class that defines the IF_EQ_GOTO command
class Control_If_Eq_Goto(Control_Flow_Basic):
    def __init__(
        self
        ):

        super().__init__(
            "IF_EQ_GOTO, Goto label, if parameters 2 and 3 are equal",
            LIB,
            (
            # Desc         Opt    Var     type      p1_val  p2_val
            ("Label",      False, AVV_NO, PT_LABEL, None,   None),
            ("A",          False, AVV_YES,PT_ANY,   None,   None), # a and b can be anything!
            ("B",          False, AVV_YES,PT_ANY,   None,   None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (3,           "    if {2} == {3} Goto {1}"),
            ),
            "a == b",
            self.a_eq_b
            )

        self.deprecated = True
        self.deprecated_use = "This command is not recommended for new scripts.  Please use the more flexible `IF` command instead."


scripts.Add_command(Control_If_Eq_Goto())  # register the command


# ##################################################
# ### CLASS IF_NE_GOTO                           ###
# ##################################################

# class that defines the IF_NE_GOTO command
class Control_If_Ne_Goto(Control_Flow_Basic):
    def __init__(
        self
        ):

        super().__init__(
            "IF_NE_GOTO, Goto label, if parameters 2 and 3 are not equal",
            LIB,
            (
            # Desc         Opt    Var     type      p1_val  p2_val
            ("Label",      False, AVV_NO, PT_LABEL, None,   None),
            ("A",          False, AVV_YES,PT_ANY,   None,   None),
            ("B",          False, AVV_YES,PT_ANY,   None,   None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (3,           "    if {2} != {3} Goto {1}"),
            ),
            "a != b",
            self.a_ne_b
            )

        self.deprecated = True
        self.deprecated_use = "This command is not recommended for new scripts.  Please use the more flexible `IF` command instead."


scripts.Add_command(Control_If_Ne_Goto())  # register the command


# ##################################################
# ### CLASS IF_GT_GOTO                           ###
# ##################################################

# class that defines the IF_GT_GOTO command
class Control_If_Gt_Goto(Control_Flow_Basic):
    def __init__(
        self
        ):

        super().__init__(
            "IF_GT_GOTO, Goto label, if parameters 2 is greater than parameter 3",
            LIB,
            (
            # Desc         Opt    Var     type      p1_val  p2_val
            ("Label",      False, AVV_NO, PT_LABEL, None,   None),
            ("A",          False, AVV_YES,PT_ANY,   None,   None),
            ("B",          False, AVV_YES,PT_ANY,   None,   None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (3,           "    if {2} > {3} Goto {1}"),
            ),
            "a > b",
            self.a_gt_b
            )

        self.deprecated = True
        self.deprecated_use = "This command is not recommended for new scripts.  Please use the more flexible `IF` command instead."


scripts.Add_command(Control_If_Gt_Goto())  # register the command


# ##################################################
# ### CLASS IF_GE_GOTO                           ###
# ##################################################

# class that defines the IF_GE_GOTO command
class Control_If_Ge_Goto(Control_Flow_Basic):
    def __init__(
        self
        ):

        super().__init__(
            "IF_GE_GOTO, Goto label, if parameters 2 is greater than or equal to parameter 3",
            LIB,
            (
            # Desc         Opt    Var     type      p1_val  p2_val
            ("Label",      False, AVV_NO, PT_LABEL, None,   None),
            ("A",          False, AVV_YES,PT_ANY,   None,   None), #@@@ this splits strings!!!!! (it shouldn't)
            ("B",          False, AVV_YES,PT_ANY,   None,   None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (3,           "    if {2} >= {3} Goto {1}"),
            ),
            "a >= b",
            self.a_gt_b
            )

        self.deprecated = True
        self.deprecated_use = "This command is not recommended for new scripts.  Please use the more flexible `IF` command instead."


scripts.Add_command(Control_If_Ge_Goto())  # register the command


# ##################################################
# ### CLASS IF_LT_GOTO                           ###
# ##################################################

# class that defines the IF_LT_GOTO command
class Control_If_Lt_Goto(Control_Flow_Basic):
    def __init__(
        self
        ):

        super().__init__(
            "IF_LT_GOTO, Goto label, if parameters 2 is less than parameter 3",
            LIB,
            (
            # Desc         Opt    Var     type      p1_val  p2_val
            ("Label",      False, AVV_NO, PT_LABEL, None,   None),
            ("A",          False, AVV_YES,PT_ANY,   None,   None),
            ("B",          False, AVV_YES,PT_ANY,   None,   None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (3,           "    if {2} < {3} Goto {1}"),
            ),
            "a < b",
            self.a_lt_b
            )

        self.deprecated = True
        self.deprecated_use = "This command is not recommended for new scripts.  Please use the more flexible `IF` command instead."


scripts.Add_command(Control_If_Lt_Goto())  # register the command


# ##################################################
# ### CLASS IF_LE_GOTO                           ###
# ##################################################

# class that defines the IF_LE_GOTO command
class Control_If_Le_Goto(Control_Flow_Basic):
    def __init__(
        self
        ):

        super().__init__(
            "IF_LE_GOTO, Goto label, if parameters 2 is less than or equal to parameter 3",
            LIB,
            (
            # Desc         Opt    Var     type      p1_val  p2_val
            ("Label",      False, AVV_NO, PT_LABEL, None,   None),
            ("A",          False, AVV_YES,PT_ANY,   None,   None),
            ("B",          False, AVV_YES,PT_ANY,   None,   None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (3,           "    if {2} <= {3} Goto {1}"),
            ),
            "a <= b",
            self.a_le_b
            )

        self.deprecated = True
        self.deprecated_use = "This command is not recommended for new scripts.  Please use the more flexible `IF` command instead."


scripts.Add_command(Control_If_Le_Goto())  # register the command


# ##################################################
# ### CLASS Control_If_Pressed_Goto_Label        ###
# ##################################################

# class that defines the IF_PRESSED_GOTO_LABEL command
class Control_If_Pressed_Goto_Label(Control_Flow_Basic):
    def __init__(
        self
        ):

        super().__init__(
            "IF_PRESSED_GOTO_LABEL, Jump to label if initiating button still pressed",
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
            "IF_UNPRESSED_GOTO_LABEL, Jump to label if initiating button is NOT pressed",
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
            "REPEAT_LABEL, Jump to label a fixed number of times",
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
            "REPEAT, Repeat a block of code a fixed number of times (auto reset -- can be nested)",
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
            "IF_PRESSED_REPEAT_LABEL, Jump to a label a fixed number of times IF initiating button still pressed",
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
            "the button is not pressed",
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
            "IF_PRESSED_REPEAT, Repeat a block of code a fixed number of times IF originating button still pressed (auto reset -- can be nested)",
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
            "IF_UNPRESSED_REPEAT_LABEL, Jump to a label a fixed number of times IF initiating button released",
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
            "IF_UNPRESSED_REPEAT, Repeat a block of code a fixed number of times IF originating button is released (auto reset -- can be nested)",
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

        super().__init__("RESET_REPEATS, Resets all repeats to their initial values")


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
# ### CLASS Control_Return                        ###
# ##################################################

# class that defines the RETURN command
#
# This differs from END and ABORT (that will abort the execution of a button) in that will returnfrom a
# subroutine without exiting
class Control_Return(command_base.Command_Text_Basic):
    def __init__(
        self,
        ):

        super().__init__("RETURN, Returns from a subroutine or exits a script",
            LIB,
            "SCRIPT RETURNS" )


    def Process(self, btn, idx, split_line):
        return -1


scripts.Add_command(Control_Return())  # register the command


# ##################################################
# ### CLASS Control_End                          ###
# ##################################################

# class that defines the END command
#
# This command simply ends the current script.  I'm going to be working on subroutines, so this is a good
# start.  The parameters to this command are simply the message it will print.
# This is really like a comment that returns the next line as -1
class Control_End(Control_Return):
    def __init__(
        self,
        ):

        super().__init__()

        self.name = "END"
        self.desc = "Ends an execution unconditionally (including if called from a subroutine)"
        self.info_msg = "SCRIPT ENDED"


    def Process(self, btn, idx, split_line):
        btn.root.thread.kill.set()
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
        self.desc = "Aborts an execution unconditionally (including if called from a subroutine)"
        self.info_msg = "SCRIPT ABORTED"


scripts.Add_command(Control_Abort())  # register the command
