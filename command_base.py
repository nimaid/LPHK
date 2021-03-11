import variables, kb
from constants import *

# ##################################################
# ### CLASS Command_Basic                        ###
# ##################################################

# Command_Basic is a class that describes a command
class Command_Basic:
    def __init__(
        self,
        name: str,            # The name of the command (what you put in the script)
        lib="LIB_UNSET",
        auto_validate=None,   # Definition of the input parameters
        auto_message=None,    # Definition of the message format
        ):

        # The information below MUST NOT be changed outside __init__    .
        # Remember - more than one command may be in execution at a time
        # and we rely on the parameters to the methods to contain things
        # unique to each one!  Local variables are fine, self.anything is BAD

        p = name.find(',')                    # is there a comma in the name?
        if p > 0:                             # yes!  must have a description
            self.name = name[:p].strip()      # extract the name part
            self.desc = name[p+1:].strip()    # and the description part
        else:
            self.name = name                  # the literal name of our command
            self.desc = ''                    # no description
        self.doc = []                         # no multi-line documentation

        self.lib = lib                        # the library we're part of
        self.auto_validate = auto_validate    # any auto-validation, if defined
        self.auto_message = auto_message      # format for any messages we need

        self.validate_init()

        self.valid_max_params = self.Calc_valid_max_params()     # calculate the max number of parmeters
        self.valid_num_params = self.Calc_valid_param_counts()   # calculate the set of valid numbers of parameters

        self.run_states = [RS_INIT, RS_GET, RS_INFO, RS_VALIDATE, RS_RUN, RS_FINAL]  # by default we'll do everything if you don't override
        self.validation_states = [VS_COUNT, VS_PASS_1, VS_PASS_2]                    # by default we'll do a count and both passes if you don't override


    def validate_init(self):
        # This helps validate the parameters passed to __init__.  It helps enforce the rules
        avl = self.auto_validate
        if avl != None:
            np = len(avl) - 1
            for p, av in enumerate(avl):
                if av[AV_TYPE][AVT_LAST] and p < np:          # variable type is "last" but it's not the last
                    raise Exception('ERROR in command "' + self.name + '" - the parameter #' + str(p+1) + ' (' + av[AVT_DESC] + ') is not the last parameter')
                if not (av[AV_VAR_OK] in av[AV_TYPE][AVT_MAX_VAR]):  # some types can't be passed variables
                    raise Exception('ERROR in command "' + self.name + '" - the parameter #' + str(p+1) + ' (' + av[AVT_DESC] + ') specifies a variable type that is not permittted')

    def Validate(
        # This is a low level validation routine.  If you take over this function you must take
        # responsibility for all validation.

        # If you have set up the auto_valudate structure, it will do most of the validation for you.
        # If you need to do more, you may be able to override a more specific routine.

        # This routine will be called twice, once for pass_no 1 and again for pass_no 2
        # Pass 1 is for general validation of literal commands and literal parameters, and also
        # for adding symbols (for example, labels).
        # Pass 2 is typically used for checking for the presence of symbols (labels, for example)

        # This method should return True if the validation was successful, otherwise it should
        # return a tuple of the error message and the line causing the error.
        self,
        btn,
        idx: int,
        split_line,
        pass_no            # pass_no 1 is a symbol gathering pass, pass_no 2 is a pass that requires
                           # symbols.  Any processing that does not set up labels should be done on
                           # pass 2. For example, goto can be checked on pass 2 to ensure the label
                           # exists
        ):

        try:
            # invalid return, but indicates nothing done yet.
            ret = None

            # If it's pass 1
            if pass_no == VS_PASS_1:
                # validate the count if required
                if VS_COUNT in self.validation_states:
                    ret = self.Partial_validate_step_count(ret, btn, idx, split_line)

                # do pass 1 validation if required
                if VS_PASS_1 in self.validation_states:
                    ret = self.Partial_validate_step_pass_1(ret, btn, idx, split_line)

            # if it's pass 2
            elif pass_no == VS_PASS_2:
                # call Pass 2 if required
                if VS_PASS_1 in self.validation_states:
                    ret = self.Partial_validate_step_pass_2(ret, btn, idx, split_line)

        except:
            import traceback
            traceback.print_exc()
            ret = ("", "")

        finally:
            if type(ret) == tuple:
                return ret
            elif ret == None or ((type(ret) == bool) and ret):
                return True
            else:
                return ("", "")


    def Partial_validate_step_count(self, ret, btn, idx, split_line):
        # Validation of the count is separated from the pass 1 validation because sometinmes
        # you want to override one but not the other.  You would override this if you have some
        # odd way of counting parameters, or the count depends on something complex.
        ret = self.Validate_param_count(ret, btn, idx, split_line)
        return ret


    def Partial_validate_step_pass_1(self, ret, btn, idx, split_line):
        # Pass 1 Validation is typically defined by the auto_validate structure set up in the
        # command initialisation.  You would override this if you haven't defined this, or the
        # structure cannot pass something important about the validation.  If you override this,
        # you may wish to call the ancestor first.
        ret = self.Validate_params(ret, btn, idx, split_line, AV_P1_VALIDATION)
        return ret


    def Partial_validate_step_pass_2(self, ret, btn, idx, split_line):
        # Pass 2 Validation is typically defined by the auto_validate structure set up in the
        # command initialisation.  You would override this if you haven't defined this, or the
        # structure cannot pass something important about the validation.  If you override this,
        # you may wish to call the ancestor first.
        ret = self.Validate_params(ret, btn, idx, split_line, AV_P2_VALIDATION)
        return ret


    def Parse(
        # Parse is pretty much a call to Validate, except the output of the validation is immediately printed.
        self,
        btn,
        idx: int,
        split_line,
        pass_no            # pass_no 1 is a symbol gathering pass, pass_no 2 is a pass that requires
                           # symbols.  Any processing that does not set up labels should be done on
                           # pass 2.  Fatal errors can be generated on pass 1 or 2 for invalid syntax.
                           # Since errors will cause the process to abort, it is permissable for
                           # the same error to be reported on both passes 1 and 2 (since you won't get
                           # past pass 1).
        ):

        ret = self.Validate(btn, idx, split_line, pass_no)

        if ((type(ret) == bool) and ret):
            return True

        if ret == None or ((type(ret) == bool) and not ret) or len(ret) != 2:
            ret = ("SYSTEM ERROR PARSING LINE " + str(idx) + ". '" + line + "' on pass " + str(pass_no), btn.Line(idx))

        if ret[0]:
            print(ret[0])

        return ret


    def Run(
        # The low level run command.  Override this if you want to take complete control of the execution of
        # the command.  Typically you'll want to override one of the Partial_run... methods or the Perform()
        # method

        # This should return idx+1 normally (this causes the script to continue at the next line (or exit
        # when it falls off the end.

        # If you wish to abort the script, you should return a value outside of the range of valid line numbers.
        # Typically -1 is returned, however in some cases a very high number can also be returned.

        # To cause the script to jump to a different line, simply return the line number you wish to go to.
        self,
        btn,
        idx: int,
        split_line
        ):

        try:
            ret = None  # this is an invalid return value, but it indicates nothing has happened yet

            if RS_INIT in self.run_states:  #  Do the initialisation if required (highly recommended)
                ret = self.Partial_run_step_init(ret, btn, idx, split_line)
                if ret == -1 or ((type(ret) == bool) and not ret):
                    return ret

            if RS_GET in self.run_states:   # Get the parameters if required
                ret = self.Partial_run_step_get(ret, btn, idx, split_line)
                if ret == -1 or ((type(ret) == bool) and not ret):
                    return ret

            if RS_INFO in self.run_states:   # Display info if required
                ret = self.Partial_run_step_info(ret, btn, idx, split_line)
                if ret == -1 or ((type(ret) == bool) and not ret):
                    return ret

            if RS_VALIDATE in self.run_states:  # Validate the parameters if required
                ret = self.Partial_run_step_validate(ret, btn, idx, split_line)
                if ret == -1 or ((type(ret) == bool) and not ret):
                    return ret

            if RS_RUN in self.run_states:  # Actualy do the command! (calls Perform()
                ret = self.Partial_run_step_run(ret, btn, idx, split_line)
                if ret == -1 or ((type(ret) == bool) and not ret):
                    return ret

        except:
            import traceback
            traceback.print_exc()
            ret = -1

        finally:
            if RS_FINAL in self.run_states:  # Do the finalisation if required (highly recommended)
                self.Partial_run_step_final(ret, btn, idx, split_line)

            # Make sure the return values are tidied up.
            if type(ret) == int:
                return ret
            elif ret == None or ((type(ret) == bool) and ret):
                return idx+1
            else:
                return -1


    def Partial_run_step_init(self, ret, btn, idx, split_line):
        # information about *this* run of the command MUST be in the symbol table

        # You might be tempted to not run the init if the variables below aren't needed,
        # however this could have consequences in the future, so it's best to run it.

        # If you need more temporary data, you can override this, call the ancestor, and
        # create what you need.
        #print(f"run_step_init '{split_line}', {self.Param_validation_count(len(split_line)-1)}")#@@@
        btn.symbols[SYM_PARAMS] = [self.name] + [None] * self.Param_validation_count(len(split_line)-1)
        #print(btn.symbols[SYM_PARAMS])#@@@
        btn.symbols[SYM_PARAM_CNT] = 0

        return ret


    def Partial_run_step_get(self, ret, btn, idx, split_line):
        # This gets the values from the command, including fetching variable values.
        # After this is run, parameters will be in the symbol table, but those coming
        # from variables will not have been validated.
        ret = self.Run_params(ret, btn, idx, split_line, VS_PASS_1)
        return ret


    def Partial_run_step_info(self, ret, btn, idx, split_line):
        # This step matches the number of parameters passed with the definitions for messages,
        # printing the matching message, or a default message if no matching message can be found.

        # If you have messages that don't fit a simple template (e.g. 2 different possible messages
        # for the same number of parameters then you're going to want to override this method.
        # If you're overriding the method, you will rarely want to call the ancestor method.
        msg = False
        if self.auto_message:
            params = btn.symbols[SYM_PARAMS]
            param_cnt = btn.symbols[SYM_PARAM_CNT]
            for msg_def in self.auto_message:
                if msg_def[AM_COUNT] == param_cnt:
                   print(AM_PREFIX.format(self.lib, btn.coords, str(idx+1)) + msg_def[AM_FORMAT].format(*params))
                   msg = True
                   break

        if not msg:
            print(AM_DEFAULT.format(self.lib, btn.coords, str(idx+1), self.name, str(params)))

        return ret


    def Partial_run_step_validate(self, ret, btn, idx, split_line):
        # This step performs run-time validation of values passed from variables.
        # Those that come from variables are checked using the validation method passed.
        ret = self.Run_params(ret, btn, idx, split_line, VS_PASS_2)
        return ret


    def Partial_run_step_run(self, ret, btn, idx, split_line):
        # This performs the running of the command.  Because this does nothing it is pretty much
        # ALWAYS overridden.  However, to make life easier, this function calls the Process()
        # method.  That's simpler to override.
        ret = self.Process(btn, idx, split_line)
        if ret == None:
            ret = idx + 1

        return ret


    def Partial_run_step_final(self, ret, btn, idx, split_line):
        # This removes stuff from the symbol table that isn't needed any more.  Whilst it may be fairly
        # superfluous at present, if you start to put more stuff in the symbol table during the execution
        # of a command this might start to get more important.

        # If you override this, it is conventional to call the ancestor function last, but there's no reason
        # at present that you must.
        del btn.symbols[SYM_PARAMS]
        del btn.symbols[SYM_PARAM_CNT]

        return ret


    def Process(self, btn, idx, split_line):
        # This is the default process called to run a command.  Override it to do something other than
        # nothing at runtime.

        # This is probably the most common method you will override.  It is designed in such a way that
        # you do not need to call the ancestor.
        pass                    # default process is to do nothing


    def Calc_valid_max_params(self):
        # Return the maximum number of parameters.  We can calculate this simply based on the number defined
        # in the auto_validate.  If you aren't using the auto_validate, then you may need to set this yourself
        # in the __init__()
        # if the last parameter is "last" then there is no maximum!
        avl = self.auto_validate
        if avl:
            if len(avl) == 0 or not avl[-1][AV_TYPE][AVT_LAST]:
                return len(avl)

        return None


    def Calc_valid_param_counts(self):
        # Return a set of numbers of parameters that are acceptable.  This is defined by which are optional
        # within the auto_validate structure.  If you're not using the auto_validate structure then you also
        # probably don't need this, but you'll need to do something to validate the correct number of parameters
        # have been passed in the validation (VS_COUNT)

        # This routine does not return it, but setting the counts to [n, None] indicates to the parameter number
        # validation routine that n or more parameters are acceptable -- this is great for comments etc.
        ret = None

        avl = self.auto_validate
        if avl:
            ret = []
            vn = len(avl)
            for i, av in enumerate(avl):
                if av[AV_OPTIONAL]:                   # if this one is optional
                    ret += [i]                        # then 1 fewer is OK

            if vn > 0 and avl[-1][AV_TYPE][AVT_LAST]:
                ret += [vn, None]                     # if the last parameter is a "last" parameter, there is no limit on parameters
            else:
                ret += [vn]                           # it's always valid to pass *all* the parameters

        return ret


    def Validate_param_count(self, ret, btn, idx, split_line):
        # Should only be called from pass 1 (actually within VS_COUNT that happens just prior to
        # VS_PASS_1

        # Whilst you can override this method, you're more likely to override the Validation_step_count()
        # method which does no more than just call this.
        if not (ret == None or ((type(ret) == bool) and ret)):
            return ret

        v = variables.Check_num_params(btn, self, idx, split_line)

        return v


    def Param_validation_count(self, n_passed):
        # This routine determines how many parameters to check.  In cases where there are unlimited parameters,
        # it will only recommend checking the number that exist.  Otherwise, all parameters will be checked.
        # This function improves efficiency.
        #print(f"vmp = {self.valid_max_params}, vnp = {self.valid_num_params}, n = {n_passed}")#@@@
        vmp = self.valid_max_params                     # what is the max number of parameters
        if vmp == None:
           vnp = self.valid_num_params                  # if there isn't a max, use the number of parameters
           if vnp == None or vnp[0] == None:            # if we really don't know
               v = 0                                    # assume 0
           elif vnp[-1] == None:                        # if there is an unlimited maximum
               v = vnp[-2]                              # use the max that we know
           else:
               return vnp[-1]                           # use the actual maximum
        else:
            v = vmp                                     # vmp is preferred though

        #print(f"vmp = {vmp}, v = {v}, n = {n_passed}")#@@@
        if (v == None) or (v < n_passed):
            return n_passed
        else:
            return v


    def Validate_params(self, ret, btn, idx, split_line, val_validation):
        # This command is called from both pass 1 and 2 of validation  It is really just a method to
        # call the validation of the parameters one by one.  If you haven't set up the maximum parameters
        # (if you haven't used the auto_validate structure) then you can override this to validate each
        # of your parameters.  You will need to remember that this gets called for both pass 1 and 2.
        if not (ret == None or ((type(ret) == bool) and ret)):
            return ret

        for i in range(self.Param_validation_count(len(split_line)-1)):
           ret = self.Validate_param_n(ret, btn, idx, split_line, val_validation, i+1)
           if not ((type(ret) == bool) and ret):
               return ret

        return ret


    def Validate_param_n(self, ret, btn, idx, split_line, val_validation, n):
        # This method validates parameters.  For custom parameters, you're best off defining new validation
        # methods (like the current variables.Validate_gt_zero()) unless you need access to the symbol
        # table.

        # Note that this function, because it runs during validation, accesses the split_line, not the
        # symbol table.

        # Where a variable type is defined as having "special" validation, that validation is currently
        # hard coded here.  It would be better to register validation routines, but...  later.
        if not (ret == None or ((type(ret) == bool) and ret)):
            return ret

        if n >= len(split_line):
            return ret

        if self.auto_validate == None or self.auto_validate == ():  # no auto validation can be done
            return ret

        if n <= len(self.auto_validate):
            # the normal auto-validation
            val = self.auto_validate[n-1]
        else:
            # special case for "last" parameters
            val = self.auto_validate[-1]

        opt = self.valid_num_params == [] or \
            self.valid_num_params[-1] == None or \
            (set(range(1,n)) & set(self.valid_num_params)) != []

        ret = variables.Check_generic_param(btn, self, idx, split_line, n, val, val_validation)

        # should we do special validation?
        if ret == None or ((type(ret) == bool) and ret):
            if val[AV_VAR_OK] == AVV_REQD:
                # check for valid variable name
                if not variables.valid_var_name(split_line[n]): # Is it a valid variable name?
                    return ("Invalid variable name", btn.Line(idx))

            elif val[AV_TYPE][AVT_SPECIAL]:
                if val_validation == AV_P1_VALIDATION:
                    if val[AV_TYPE] == PT_TARGET:                    # targets (label definitions) have pass 1 validation only
                        # check for duplicate label
                        if split_line[n] in btn.symbols[SYM_LABELS]: # Does the label already exist (that's bad)?
                            return ("Duplicate LABEL", btn.Line(idx))

                        # add label to symbol table                  # Add the new label to the labels in the symbol table
                        btn.symbols[SYM_LABELS][split_line[n]] = idx # key is label, data is line number
                    elif val[AV_TYPE] == PT_KEY:                     # Keys have pass 1 validation only
                        # check for valid key
                        if kb.sp(split_line[n]) == None:             # Does the key exist (if not, that's bad)?
                            return ("Unknown key", btn.Line(idx))
                    elif val[AV_TYPE] == PT_BOOL:                    # booleans have pass 1 validation only
                        # check for valid boolean value
                        if not (split_line[n].upper() in VALID_BOOL): # Is it a valid boolean?
                            return ("Invalid boolean value", btn.Line(idx))

                elif val_validation == AV_P2_VALIDATION:
                    if val[AV_TYPE] == PT_LABEL:                     # references (to a label) have pass 2 validation only
                        # check for existance of label
                        if split_line[n] not in btn.symbols[SYM_LABELS]:
                            return ("Target not found", btn.Line(idx))

            return True

        return (ret, btn.Line(idx))


    def Run_params(self, ret, btn, idx, split_line, pass_no):
        # This method gets the parameters.  Oddly enough it has 2 passes too.  The first pass simply gets the
        # variables, while the second pass gets them and does validation.

        # This method actually just calls the Run_Param_n method that does all the hard work for each parameter
        if ret == None:
            ret = True

        if pass_no == 1:
            param_cnt = len(split_line) - 1
            btn.symbols[SYM_PARAM_CNT] = param_cnt
            btn.symbols[SYM_PARAMS][0] = split_line[0]

            for i in range(self.Param_validation_count(param_cnt)):
                if i < param_cnt:
                    btn.symbols[SYM_PARAMS][i+1] = self.Run_param_n(ret, btn, idx, split_line, pass_no, i+1)

        elif pass_no == 2:
            # for pass 2 we don't try to validate null variables
            param_cnt = len(split_line) - 1
            for i in range(self.Param_validation_count(param_cnt)):
                if btn.symbols[SYM_PARAMS][i+1] != None:
                    ret = self.Run_param_n(ret, btn, idx, split_line, pass_no, i+1)

        return ret


    def Run_param_n(self, ret, btn, idx, split_line, pass_no, n):
        # This function gets called to firstly get the parameter (pass_no = 1) and then
        # to validate it (with pass_no = 2)

        # Note that pass 1 returns the variable value, where pass 2 returns a value indicating
        # if validation has passed.
        avl = self.auto_validate
        if avl:
            if n <= len(avl):
                av = avl[n-1]
            else:
                av = avl[-1]

            if pass_no == 1:
                v = split_line[n]
                #print("V1", v) #@@@

                if av[AV_VAR_OK] == AVV_YES:                                               # if a variable is allowed
                    if variables.valid_var_name(v):                                        # if it's a variable
                        v = variables.get_value(split_line[n], btn.symbols)                # get the value
                        #print("V2a", v) #@@@

                if av[AV_VAR_OK] != AVV_REQD:                                              # if it's not required (i.e. the variable name is not to be passed through)
                    if av[AV_TYPE] and av[AV_TYPE][AVT_CONV]:                              # if there is a type
                        #print("V2ba", v, type(v), av[AV_TYPE][AVT_CONV]) #@@@
                        v = av[AV_TYPE][AVT_CONV](v)                                       # convert the variable to that type
                        #print("V2bb", v) #@@@

                return v
            elif pass_no == 2:
                ok = ret

                if av[AV_P1_VALIDATION]:
                    #print("S", btn.symbols[SYM_PARAMS][n], idx, self.name, av[AV_DESCRIPTION], n, split_line[n]) #@@@
                    ok = av[AV_P1_VALIDATION](btn.symbols[SYM_PARAMS][n], idx, self.name, av[AV_DESCRIPTION], n, split_line[n])
                    if ok != True:
                        print("[" + self.lib + "] " + btn.coords + "  " + ok)
                        ret = -1

        return ret


    # How many parameters do we have?
    def Param_count(self, btn):
        return btn.symbols[SYM_PARAM_CNT]


    # Is there a parameter n?
    def Has_param(self, btn, n):
        if self.Param_count(btn) < n:
            return False

        val = btn.symbols[SYM_PARAMS][n]
        return not (val is None)


    # gets the value of the nth parameter (button is required for context).  Other is default value if param does not exist
    def Get_param(self, btn, n, other=None):
        # handle the repeating last parameter
        avl = len(self.auto_validate)
        m = min(n, avl)
        av = self.auto_validate[m-1]

        if self.Param_count(btn) > n:
           param = None
           #print("P-none", self.Param_count(btn), n)#@@@
        else:
           #print("P-n", self.Param_count(btn), n)#@@@
           param = btn.symbols[SYM_PARAMS][n]
        #print("P", param) #@@@
        if param == None:
            ret = other
            #print(f"ret- {ret}") #@@@
        else:
            if av[AV_VAR_OK] == AVV_REQD:
                #print("RQ") #@@@
                ret = variables.get(param, btn.symbols[SYM_LOCAL], btn.symbols[SYM_GLOBAL][1])
                #print(f"ret0 {ret}") #@@@
            else:
                #print("NRQ") #@@@
                if type(param) == str and av[AV_TYPE][AVT_DESC] in {PT_STR[AVT_DESC], PT_STRS[AVT_DESC]} and param[0:1] == '"':
                    ret = param[1:]
                    #print(f"ret1 {ret}") #@@@
                else:
                    ret = param
                    #print(f"ret2 {ret}") #@@@

        #print(f"get_param '{ret}', {type(ret)} --> '{av[AV_TYPE][AVT_CONV](ret)}', {type(av[AV_TYPE][AVT_CONV](ret))}using '{av[AV_TYPE][AVT_CONV]}'") #@@@
        return av[AV_TYPE][AVT_CONV](ret)


    # sets the value of the nth parameter (if it is a variable)
    def Set_param(self, btn, n, val):
        if self.Param_count(btn) < n:
            return

        param = btn.symbols[SYM_PARAMS][n]
        avl = len(self.auto_validate)
        m = min(n, avl)
        av = self.auto_validate[m-1]
        if av[AV_VAR_OK] == AVV_REQD:
            #print("SP", btn.symbols[SYM_PARAMS][n], val, btn.symbols) #@@@
            variables.Auto_store(btn.symbols[SYM_PARAMS][n], val, btn.symbols) # return result in variable


# ##################################################
# ### CLASS Command_Text_Basic                   ###
# ##################################################

# class that defines an object that can handle just text after the command
class Command_Text_Basic(Command_Basic):
    def __init__(
        self,
        name: str,                  # The name of the command (what you put in the script)
        lib,
        info_msg):                  # what we display before the text

        super().__init__(name,      # the name of the command as you have to enter it in the code
            lib,
            (
            # Desc         Opt    Var      type       p1_val                        p2_val
            ("Param",      False, AVV_NO,  PT_TEXT,   None,                         None),
            ),
            () )

        # this command does not have a standard list of fields, so we need to do some stuff manually
        self.valid_max_params = 32767      # There is no maximum, but this is a reasonable limit!
        self.valid_num_params = [0, None]  # zero or more is OK

        if "{1}" in info_msg:
            self.info_msg = info_msg       # customised message text before parameter text
        else:
            self.info_msg = info_msg + " {1}"


    def Partial_run_step_info(self, ret, btn, idx, split_line):
        print(AM_PREFIX.format(self.lib, btn.coords, str(idx+1)) + "    " + self.info_msg.format("", btn.symbols[SYM_PARAMS][1]))


# ##################################################
# ### CLASS Command_Header                       ###
# ##################################################

# Command_Header is a class specifically defining a header command
class Command_Header(Command_Basic):

    def __init__(
        self,
        name: str,           # The name of the command (what you put in the script)
        is_async: bool,      # is this async?
        lib="LIB_UNSET",
        auto_validate=None
        ):

        super().__init__(name, lib, auto_validate)
        self.is_async = is_async

    def Validate(
        self,
        btn,
        idx: int,
        split_line,
        pass_no
        ):

        #if idx != 0:
        #   return ("ERROR on line " + btn.Line(idx) + ". " + self.name + " must only appear on line 1.", -1)

        return (None, 0)


