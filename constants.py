# Constants used all over the place.  An excuse to use "from constants import *"

# Get platform information
PLATFORMS = [   {"search_string": "win", "name_string": "windows"},
                {"search_string": "linux", "name_string": "linux"},
                {"search_string": "darwin", "name_string": "macintosh"} ]
PLATFORM = None
for plat in PLATFORMS:
    import sys
    if sys.platform.startswith(plat["search_string"]):
        PLATFORM = plat["name_string"]
        break
if PLATFORM == None:
    PLATFORM = "other"

# Symbol table constants
SYM_REPEATS   = "repeats"     # current value for loops
SYM_ORIGINAL  = "original"    # initial values for loops
SYM_LABELS    = "labels"      # location of labels
SYM_MOUSE     = "m_pos*"      # save location of mouse
SYM_LOCAL     = "l_vars"      # local variables for script
SYM_GLOBAL    = "g_vars"      # global variables and lock
SYM_STACK     = "stack"       # stack for script
SYM_PARAMS    = "params"      # params for script
SYM_PARAM_CNT = "param_cnt"   # count of params passed to command

# constants for run state
RS_INIT     = 0
RS_GET      = 1
RS_INFO     = 2
RS_VALIDATE = 3
RS_RUN      = 4
RS_FINAL    = 5

# constants for validation state
VS_COUNT  = 0   # Count is done prior to pass 1
VS_PASS_1 = 1
VS_PASS_2 = 2

# Constants for auto validation
AV_DESCRIPTION    = 0
AV_OPTIONAL       = 1

AV_VAR_OK         = 2  # this is no longer boolean
AVV_NO    = 0          # only literals
AVV_YES   = 1          # var permitted (pass by value)
AVV_REQD  = 2          # var required (pass by reference)

AV_TYPE           = 3  # This is a tuple
AVT_DESC    = 0        # and this is what is inside the tuple
AVT_CONV    = 1
AVT_SPECIAL = 2
AVT_LAST    = 3
AVT_MAX_VAR = 4

AVVS_ALL = {AVV_NO, AVV_YES, AVV_REQD}  # allow any option
AVVS_NO =  {AVV_NO}                     # only allow literals
AVVS_YES = {AVV_YES, AVV_REQD}          # AVV_YES is potentially ambiguous!
AVVS_AMB = {AVV_NO, AVV_REQD}           # These are not ambiguous

AV_P1_VALIDATION  = 4
AV_P2_VALIDATION  = 5

# constants for parameter types
#              desc      conv   special last  var (special means additional auto-validation, last means MUST be last, var is the max AV_VAR allowed)
PT_INT      = ("int",    int,   False, False, AVVS_ALL)
PT_FLOAT    = ("float",  float, False, False, AVVS_ALL)
PT_STR      = ("str",    str,   True,  False, AVVS_ALL)        # a quoted string
PT_STRS     = ("strs",   str,   True,  True,  AVVS_ALL)        # 1 or more quoted strings
PT_LINE     = ("line",   str,   True,  True,  AVVS_NO)         # the rest of the line following first preceeding whitespace
PT_TEXT     = ("text",   str,   False, False, AVVS_AMB)        # a string without whitespace @@@ DEPRECATED
PT_LABEL    = ("label",  str,   True,  False, AVVS_NO)         # Note that this is for a reference to a label, not the definition of a label!
PT_TARGET   = ("target", str,   True,  False, AVVS_NO)         # Note that this is for the definition of a target (e.g. creating a label)
PT_KEY      = ("key",    str,   True,  False, AVVS_NO)         # This is a key literal
PT_BOOL     = ("bool",   str,   True,  False, AVVS_ALL)        # True/False, Yes/No, Y/N, nonzero/zero <-- for variables

# constants for auto_message
AM_COUNT  = 0
AM_FORMAT = 1

AM_PREFIX  = "[{0}] {1}  Line:{2}"
AM_DEFAULT = AM_PREFIX + "     {3} parameters ({4})"

# constants for boolean values
VALID_BOOL_TRUE  = ["TRUE", "YES"]
VALID_BOOL_FALSE = ["FALSE", "NO"]
VALID_BOOL       = VALID_BOOL_TRUE + VALID_BOOL_FALSE

# Misc constants
COLOR_PRIMED = 5 #red
COLOR_FUNC_KEYS_PRIMED = 9 #amber
EXIT_UPDATE_DELAY = 0.1
DELAY_EXIT_CHECK = 0.025

SUBROUTINE_PREFIX = "CALL:"
