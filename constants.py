# Constants used all over the place.  An excuse to use "from constants import *"

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
AV_VAR_OK         = 2
AV_TYPE           = 3  # This is a tuple
AVT_DESC    = 0        # and this is what is inside the tuple
AVT_CONV    = 1
AVT_SPECIAL = 2
AV_P1_VALIDATION  = 4
AV_P2_VALIDATION  = 5

# constants for parameter types
#              desc      conv   special  (special means additional auto-validation
PT_INT      = ("int",    int,   False)
PT_FLOAT    = ("float",  float, False)
PT_TEXT     = ("text",   str,   False)
PT_LABEL    = ("label",  str,   True)       # Note that this is for a reference to a label, not the definition of a label!
PT_TARGET   = ("target", str,   True)       # Note that this is for the definition of a target (e.g. creating a label)
PT_KEY      = ("key",    str,   True)       # This is a key literal

# constants for auto_message
AM_COUNT  = 0
AM_FORMAT = 1

AM_PREFIX  = "[{0}] {1}  Line:{2}"
AM_DEFAULT = AM_PREFIX + "     {3} parameters ({4})"

# Misc constants
COLOR_PRIMED = 5 #red
COLOR_FUNC_KEYS_PRIMED = 9 #amber
EXIT_UPDATE_DELAY = 0.1
DELAY_EXIT_CHECK = 0.025
