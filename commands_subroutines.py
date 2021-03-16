import command_base, commands_header, scripts, variables, param_convs
from constants import *

LIB = "cmds_subr" # name of this library (for logging)

# Note that this command module does not define a set of commands as such, but implements a method
# of calling subroutines by enabling a script to be registrered as a regular command.
# As such, it needs to define a new header, and a class that will be instansiated once for each
# subroutine that is loaded.

# ##################################################
# ### CLASS Header_Sub_Name                      ###
# ##################################################

# This is a dummy header.  It is interpreted for real when a subroutine is loaded,
# but is ignored in the normal running of commands
class Header_Sub_Name(command_base.Command_Header):
    def __init__(
        self,
        ):

        super().__init__(SUBROUTINE_HEADER + ", Defines a subroutine name and parameters")


    # Dummy validate routine.  Simply says all is OK (unless you try to do it in a real button!)
    def Validate(
        self,
        btn,
        idx: int,              # The current line number
        split_line,            # The current line, split
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:
            if btn.is_button:
                return ("Line:" + str(idx+1) + " - The header '" + split_line[0] + "' is only permitted in a subroutine.", btn.Line(idx))

        return True

scripts.Add_command(Header_Sub_Name())  # register the header


# ##################################################
# ### CLASS Subroutine_Define                    ###
# ##################################################

# class that defines the CALL:xxxx command (runs a subroutine).  This parses the routine (pass 1 and 2 validation)
# and adds it as a command if the parsing suceeds.  It can then be called just like any other command
class Subroutine(command_base.Command_Basic):
    def __init__(
        self,
        Name,              # The name of the command
        Params,            # The parameter tuple
        Lines              # The text of the subroutine/function
        ):

        super().__init__(SUBROUTINE_PREFIX + Name + ", Define a subroutine that can be called with named parameters", 
            LIB,
            Params,
            (
            # num params, format string                           (trailing comma is important)
            (0,           "    Call "+ Name),
            ) )

        self.routine = Lines           # the routine to execute
        self.btn = scripts.Button(-1, -1, self.routine, None, Name) # we retain this so we only have to validate it once.  executions use a deep-ish copy
        
        self.doc = ["This header is used to define a subroutine.  Subroutines are loaded",
                    "separately from button scripts and can be saved in layouts.",
                    "",
                    "A subroutine header consists of the the text `@SUB` followed by the",
                    "name of the subroutine, and then the parameters for the subroutine",
                    "",
                    "A simple subtoutine `DO_STUFF` that is called without patameters would",
                    "be defined as follows:",
                    "",
                    "      @SUB DO_STUFF",
                    "",
                    "This would be followed by a script to so whatever the subroutine needs",
                    "to do.",
                    "",
                    "A calling script would call this subroutine using:",
                    "",
                    "      CALL:DO_STUFF",
                    "",
                    "After completion of the subroutine, control would pass to the statement",
                    "following the call unless an END or ABORT statement was reached, or",
                    "the operator cancelled the routine by pressing the Launchpad button",
                    "a second time."
                    "",
                    "Subroutines have their own stacks and local variables as well as access",
                    "to global variables.  For access to information within the calling",
                    "script, and to return information back to the calling script either",
                    "global variables or parameters can be used.",
                    "",
                    "Parameters are defined by placing legal variable names following the",
                    "subroutine name on the @SUB line.  An example is:",
                    "",
                    "      @SUB DO_STUFF a b",
                    "",
                    "This defines a subroutine that takes 2 positional parameters.  By",
                    "default they are integers, and they are passed by value (that is",
                    "any changes to their values are not passed back to the calling",
                    "routine.",
                    "",
                    "This subroutine cound be called using a script as follows:",
                    "",
                    "      CALL:DO_IT 42 var2",
                    "",
                    "Because the the parameters are passed by value, constants or variables",
                    "can be used in the call.  In this case, in the subroutine, the local",
                    "variable `a` would have the value 42, and the local variable `b`",
                    "would be set to the value of the variable `var2` from the calling",
                    "script.",
                    "",
                    "Parameters can also be defined with special modifiers that change this",
                    "default behaviour.  One way of applying these modifiers to parameters",
                    "is by following the parameter name with a `+` followed by the modifiers.",
                    "",
                    "The modifiers are:",
                    "      `%` or `I` - defines the variable as an integer number",
                    "      `#` or `F` - defines the variable as a float or real number",
                    "      `$` or `S` - defines the variable as a string",
                    "      `!` or `B` - defines the variable as a boolean (not fully implemented)",
                    "      `K`        - defines the variable as a key (not fully implemented)",
                    "      `-` or `O` - defines the variable as optional",
                    "      `@` or `R` - defines the variable as call by reference (more later)",
                    "",
                    "An example using these modifiers is as follows:",
                    "",
                    "      @SUB DO_MORE a+I b+FO c+R$",
                    "",
                    "These parameters are:",
                    "",
                    "      a+I        - the parameter `a` that is an integer (and required)",
                    "      b+FO       - the parameter `b` that is an optional floating point",
                    "      c+R$       - a required call-by reference string variable `c`",
                    "",
                    "Valid calls to this subroutine are as follows:",
                    "",
                    "      CALL:DO_MORE 12",
                    "      CALL:DO_MORE x 12.5 line",
                    "",
                    "The first call passes the required first parameter, but not the second",
                    "optional parameter.  Because the second parameter was not passed, no",
                    "more paramters are required.  The subroutine would see the variable `a`",
                    "have the value 12, the variable `b`, 0.0, and the variable `c` would be",
                    "a blank string.  Attempts to change the value of `c` would succeed, but",
                    "no variable in the calling routine would be affected.",
                    "",
                    "The second call passes the required first parameter (a variable this",
                    "time), a value of 12.5 for the second parameter, and the variable",
                    "`line` as the final required parameter.  Because the second (optional)",
                    "parameter was passed, the next parameter (being required) was mandatory.",
                    "Within the subroutine, `a` would have the value of `x` in the calling",
                    "routine, `b` would have the value of 12.5, and `c` would have the value",
                    "of the variable `line` in the calling routine.  Changing the value of",
                    "`c` will also change the value of `line` in the calling routine.",
                    "",
                    "This method of applying modifiers to variables can be simplified for all",
                    "modifiers that are not permitted in variable names.  These can also be",
                    "placed before or after the parameter name the following functionally",
                    "identical subroutine definition:",
                    "",
                    "      @SUB DO_MORE a% -b# @c$",
                    "",
                    "Subroutines are placed in text files and loaded using the Subroutine|Load",
                    "menu option.  Note that multiple subroutines can be placed in a single",
                    "file.  In this case they must be separated by a line consisting of `===`.",
                    "",
                    "Subroutines can call other subroutines and can probably be called",
                    "recursively.  A script will fail to load if it depends on a subroutine",
                    "that is not present.  Similarly, subroutines that depend on other",
                    "subroutines will fail to load if those subroutines are not available.",
                    "",
                    "During execution of a subroutine the command RETURN will immediately",
                    "return control to the calling script or subroutine.  The commands END",
                    "and ABORT will stop execution immediately without returning to the caller.",
                    "",
                    "Parameter names follow the same rules as variable names.  They must satart",
                    "with an alpha character, and may then be followed by any number of",
                    "alpha-numeric characters and underscores (`_`)."]
                     

    # process for a subroutine handles parameter passing and then passes off the process to the script in a "dummy" button
    def Process(self, btn, idx, split_line):
        sub_btn = scripts.Button(-1, -1, self.routine, btn.root, self.name) # create a new button and pass the script to it

        self.btn.Copy_parsed(sub_btn, self.name)                 # copy the info created when parsed

        variables.Local_store('sub__np', self.Param_count(btn), sub_btn.symbols) # number of parameters passed

        d = variables.Local_recall('sub__d', btn.symbols)        # get current call depth
        d = param_convs._int(d)                                  # create an integer from it
        variables.Local_store('sub__d', d+1, sub_btn.symbols)    # and pass that + 1

        #@@@ will fail with multiple parameters at the end!
        #Which is not so much of a problem because there is no way to name or retrieve them currently

        for n in range(self.Param_count(btn)):                   # for all the params passed
            pn = self.Get_param(btn, n+1)                        # get the param
            variables.Local_store(self.auto_validate[n][AV_DESCRIPTION], pn, sub_btn.symbols) # and store it

        sub_btn.Run_subroutine()

        for n in range(self.Param_count(btn)):                   # for all the params passed
            if self.auto_validate[n][AV_VAR_OK] == AVV_REQD:     # if this is passed by reference
                pn = variables.Local_recall(self.auto_validate[n][AV_DESCRIPTION], sub_btn.symbols) # get the variable
                self.Set_param(btn, n+1, pn)                     # and store it


    # This is not the parse routine called for validation!  @@@ not used???
    def Parse_Sub(self):
        try:
            script_validate = self.btn.Parse_script() #@@@ does not raise an error
        except:
            self.popup(w, "Script Validation Error", self.error_image, "Fatal error while attempting to validate script.\nPlease see LPHK.log for more information.", "OK")
            raise


MOD_TRANS = str.maketrans('-%#$!@', 'OIFSBR')            # standardise the modifiers
MOD_CONSOLIDATE = str.maketrans('MOIFSBRV', 'MMIIIIVV')  # consoidate the modifiers
VALID_CONSOLIDATED = {"M", "I", "V"}                     # set of all valid consolidate modifiers


def Get_Name_And_Params(lines, sub_n, fname):
    # Have we found a line with @SUB?
    found = False

    for lin_num, line in enumerate(lines):
        line = line.strip()
        if line == '' or line[0] == '-':
            pass                            # ignore blank lines and comments
        elif line.split()[0] != SUBROUTINE_HEADER:
            return '', f'Error - Subroutine does not start with an {SUBROUTINE_HEADER} header on line {lin_num+1} of subroutine {sub_n} in "{fname}"', lin_num
        else:
            found = True
            break

    # Not finding the header is a bad problem
    if not found:
        return '', f'Error - Subroutine has no content up to line {lin_num+1} of subroutine {sub_n} in "{fname}"', lin_num

    # do we have a name?
    sline = line.split()
    if len(sline) < 2:
        return '', f'Error - Subroutine does not have a name on line {lin_num+1} of subroutine {sub_n} in "{fname}"', lin_num

    # this is the name
    name = sline[1]
    if name != name.upper():
        return '', f'Error - Subroutine name is not UPPERCASE on line {lin_num+1} of subroutine "{name}" in "{fname}"', lin_num

    # now work on the parameters
    params = ()

    # for each parameter
    for p_num, param in enumerate(sline[2:]):
        mods = ''                   # No modifiers yet
        var = param                 # so everything else is the variable name

        # first find leading modifiers
        for c in param:
            if not variables.valid_var_name('A'+c):
                mods += c
                var = var[1:]
            else:
                break

        # next look for anything after a "+"
        p = var.find('+')
        if p >= 0:
            mods += var[p+1:]
            var = var[:p]
        
        if not variables.valid_var_name(var): # if there's no '+', look for trailing modifiers without one
            l = len(var)
            while l > 1:
                if not variables.valid_var_name(var):
                    mods += var[-1]
                    var = var[:-1]
                else:
                    break
                l -= 1

        if var == '' or not variables.valid_var_name(var):
            return name, f'Error - Parameter "{var}" is not a valid name on line {lin_num+1} of subroutine "{name}" in "{fname}"', lin_num

        # Standardise modifiers
        mods = mods.upper().translate(MOD_TRANS)

        # Consolidate the modifiers
        modc = mods.translate(MOD_CONSOLIDATE)
        modcs = set(modc)

        if modcs > VALID_CONSOLIDATED:
            e = modcs - VALID_CONSOLIDATED
            return name, f'Error - Invalid modifier {modcs - VALID_CONSOLIDATED} specified on line {lin_num+1} of subroutine "{name}" in "{fname}"', lin_num

        # check for duplicate modifiers
        if len(modc) != len(set(modc)):
            return name, f'Error - Duplicate modifiers specified on line {lin_num+1} of subroutine "{name}" in "{fname}"', lin_num

        #      Desc Opt    Var      type    p1_val p2_val
        prm = [var, False, AVV_YES, PT_INT, None,  None]

        if mods.find('O') >= 0:
            prm[1] = True             # parameter is optional

        if mods.find('R') >= 0:
            prm[2] = AVV_REQD         # pass by reference is a required variable

        if mods.find('F') >= 0:
            prm[3] = PT_FLOAT         # parameter is a float
        elif mods.find('S') >= 0:
            prm[3] = PT_STR           # parameter is a string
        elif mods.find('K') >= 0:
            prm[3] = PT_KEY           # parameter is a key
            prm[2] = AVV_NO           # must be a constant
            if mods.find('R') >= 0:
                return name, f'Error - Key cannot be passed by reference on line {lin_num+1} of subroutine "{name}" in "{fname}"', lin_num
        elif mods.find('B') >= 0:
            prm[3] = PT_BOOL          # parameter is a boolean

        params += (tuple(prm),)       # add a new parameter

    return name, params, lin_num+1    # return the subroutine name, valid list of parameters, and the next line number


def Add_Function(lines, sub_n, fname):
    # This function is passed a list of lines.  The first non-comment line must define the header

    # first let's parse out the header to get the name and the parameters
    name, params, lin = Get_Name_And_Params(lines, sub_n, fname)
    if isinstance(params, str):
        return False, name, params

    NewCommand = Subroutine(name, params, lines)                # Create a new command object for this subroutine

    if NewCommand:
        if NewCommand.name in scripts.VALID_COMMANDS:           # does this command already exist?
            old_cmd = scripts.VALID_COMMANDS[NewCommand.name]   # get the command we will be replacing
        else:
            old_cmd = None                                      # if not, nothing to replace

        try:
            scripts.Add_command(NewCommand)                     # Add the command before we parse (to allow recursion)
            script_validation = NewCommand.btn.Validate_script()# and validate with the internal btn held in the command.
        except:
            print("[subroutines] Fatal error while attempting to validate script.\nPlease see LPHK.log for more information.")
            raise

        if script_validation != True:                           # if thre is an error in validation
            if old_cmd:                                         # and there is a replaced command
                scripts.Add_command(NewCommand)                 # put the old command back
            pass # @@@ there must be more to do! :-) This is the error return
        else:
            pass # @@@ this is the success return.  There must be more to do!

    return True, NewCommand.name, params
