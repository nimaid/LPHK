from constants import *
import variables, param_convs
import re

# operations needed to access variables

# NOTE that any locking is the responsibility of the calling code!

# Regular expression for validating variable names
VALID_RE = re.compile('^[A-Za-z][A-Za-z0-9_]*$')

# Note that popping a value from an empty stack returns 0.  An alternative is
# to return an error
def pop(syms):
    # return the top valie from the stack (and remove it)
    try:
        return syms[SYM_STACK].pop()      # take the top value from the stack in the supplied symbol table
    except:
        return 0
        # raise Exception("Stack empty")


def push(syms, val):
    # put val on to the top of the stack
    syms[SYM_STACK].append(val)           # Push a value onto the stack in the supplied symbol table


# the top of the stack will also return 0 for an empty stack.   Alternatively it could
# return an error.
def top(syms, i):
    # peek at the top value of the stack without removing it (for i=1, y:i=2, z:i=3...)
    try:
        return syms[SYM_STACK][-i]
    except:
        return 0
        #raise Exception("Stack empty")


def is_defined(name, vbls):
    # is the variable defined in the symbol library
    return vbls and str(name).lower() in vbls


def undef(name, vbls):
    # remove a variable from the symbol library (existing or not)
    try:
        del vbls[str(name).lower()]
    except:
        pass


# gets a variable using the default conversion of None if the variable is undefined.
def get(name, l_vbls, g_vbls, default=param_convs._None):
    # get a variable.  look in one symbol table, then the next.
    # this allows an order to be defined to get local vars then global
    # the optional default allows a value other than None to be returned if the variable is undefined
    name = str(name).lower()

    if is_defined(name, l_vbls):    # First look in the local symbol table (if defined)
        return l_vbls[name]
    if is_defined(name, g_vbls):    # then the global one
        return g_vbls[name]
    return default(None)                  # return default value (rather than always 0)
    # raise Exception("Variable not found")


def put(name, val, vbls):
    # store a value in a named variable in a specific variable list
    vbls[name.lower()] = val


# if you try to grab an argument where no more exists, an error will result
def next_cmd(ret, cmds):
    # pull the next value from the commands list and return incremented result
    try:
        v = cmds[ret]   # we get the next element
    except:
        raise Exception("Can't get next element.")
    else:
        return ret+1, v # and we return an updated pointer and the removed element


# variable names should start with an alpha character and contain only alpha numeric and underscores
def valid_var_name(v):
    return isinstance(v, str) and VALID_RE.match(v)


# return a properly formatted error message
def error_msg(idx, name, desc, p, param, err):
    ret = "Line:" + str(idx+1) + " -"

    if name:
        ret += " '" + name + "'"
    if desc:
        ret +=  " " + desc
    if p:
        ret += " : param#" + str(p)
    if param:
        if p:
            ret += " '" + param + "'"
        else:
            ret += " (" + param + ")"
    if err:
        ret += " " + err

    ret += "."

    return ret


# check the number of parameters allowed
def Check_num_params(btn, cmd, idx, split_line):
    # cmd.valid_num_params is an array of valid numbers of parameters
    # it will be None if you've taken control of handling the parameters yourself.
    # if you set it to [n, None] that means any number of parameters from n to infinity!

    if cmd.valid_num_params == None:      # if this is undefined
        return True       # anything is valid

    ln = len(cmd.valid_num_params)
    n = len(split_line)-1
    if ln == 2 and cmd.valid_num_params[1] == None:
        if n >= cmd.valid_num_params[0]:
            return True
    elif n in cmd.valid_num_params:
        return True

    # create a properly formatted error message
    if len(cmd.valid_num_params) == 0:
        msg = "Has no valid number of parameters described. "
        return (error_msg(idx, cmd.name, msg, None, None, "Please correct the definition"), btn.Line(idx))

    msg = "Incorrect number of parameters"
    if cmd.valid_num_params == [0]:
        return (error_msg(idx, cmd.name, msg, str(n), "supplied.  None are permitted"), btn.Line(idx))
    else:
        cnt = ""
        if len(cmd.valid_num_params) == 1:
            cnt += str(cmd.valid_num_params[0])
        elif len(cmd.valid_num_params) == 2 and cmd.valid_num_params[1] == None:
            cnt += str(cmd.valid_num_params[0]) + " or more"
        else:
            cnt += ", ".join([str(el) for el in cmd.valid_num_params[0:-1]]) + ", or " + str(cmd.valid_num_params[-1])

    return (error_msg(idx, cmd.name, msg, None, str(n), "supplied, " + cnt + " are required"), btn.Line(idx))


# check a generic parameter
def Check_generic_param(btn, cmd, idx, split_line, p, val, val_validation):
    temp = None

    if p >= len(split_line):
        if val[AV_OPTIONAL]:
            return True
        else:
            return (error_msg(idx, name, desc, p, None, 'required ' + val[AV_TYPE][AVT_DESC] + ' parameter not present'), split_line[p])

    try:
        temp = val[AV_TYPE][AVT_CONV](split_line[p])
    except:
        if val[AV_VAR_OK] in AVVS_YES and valid_var_name(split_line[p]):   # a variable is OK here
            return True
        else:
            return (error_msg(idx, cmd.name, val[AV_DESCRIPTION], p, split_line[p], 'not a valid ' + val[AV_TYPE][AVT_DESC]), split_line[p])

    if val[val_validation]:
        return val[val_validation](temp, idx, cmd.name, val[AV_DESCRIPTION], p, split_line[p])

    return True


# @@@ deprecated
def Check_numeric_param(split_line, p, desc, idx, name, line, validation, optional=False, var_ok=True):
    temp = None

    if p >= len(split_line):
        if optional:
            return True
        else:
            return (error_msg(idx, name, desc, p, None, 'required parameter not present'), btn.Line(idx))

    try:
        temp = conv(split_line[p])
    except:
        if var_ok and valid_var_name(split_line[p]):   # a variable is OK here
            return True
        return (error_msg(idx, name, desc, p, split_line[p], 'not valid'), btn.Line(idx))

    if validation:
        return validation(temp, idx, name, desc, p, split_line[p])

    return True


# get the value of a parameter
def get_value(v, symbols):
    if valid_var_name(v):
        g_vars = symbols[SYM_GLOBAL]
        with g_vars[0]:                                # lock the globals while we do this
            v = get(v, symbols[SYM_LOCAL], g_vars[1])

    return v


def Validate_non_zero(v, idx, name, desc, p, param):
    # make sure we have something that can be made numeric!
    try:
       v = float(v)
    except:
        return error_msg(idx, name, desc, p, param, 'must be numeric')

    # then do the test
    if float(v) != 0:
        return True
    else:
        return error_msg(idx, name, desc, p, param, 'must not be zero')


def Validate_gt_zero(v, idx, name, desc, p, param):
    # make sure we have something that can be made numeric!
    try:
       v = float(v)
    except:
        return error_msg(idx, name, desc, p, param, 'must be numeric')

    # then do the test
    if v > 0:
        return True
    else:
        return error_msg(idx, name, desc, p, param, 'must be greater than zero')


def Validate_ge_zero(v, idx, name, desc, p, param):
    # make sure we have something that can be made numeric!
    try:
       v = float(v)
    except:
        return error_msg(idx, name, desc, p, param, 'must be numeric')

    # then do the test
    if v >= 0:
        return True
    else:
        return error_msg(idx, name, desc, p, param, 'must not be less than zero')


def Auto_store(v_name, value, symbols):
    # automatically stores the variable in the "right" place
    with symbols[SYM_GLOBAL][0]:                                # lock the globals while we do this
        if is_defined(v_name, symbols[SYM_LOCAL]):              # Is it local...
            put(v_name, value, symbols[SYM_LOCAL])              # ...then store it locally
        elif is_defined(v_name, symbols[SYM_GLOBAL][1]):        # Is it global...
            put(v_name, value, symbols[SYM_GLOBAL][1])          # ...store it globally
        else:
            put(v_name, value, symbols[SYM_LOCAL])              # default is to create new in locals


def Local_store(v_name, value, symbols):
    # stores the variable locally
    put(v_name, value, symbols[SYM_LOCAL])                      # and store it locally


def Global_store(v_name, value, symbols):
    # stores the variable globally
    with symbols[SYM_GLOBAL][0]:                                # lock the globals while we do this
        put(v_name, value, symbols[SYM_GLOBAL][1])              # and store it globally


def Auto_recall(v_name, symbols):
    # automatically recalls the variable from the "right" place
    with symbols[SYM_GLOBAL][0]:                                # lock the globals while we do this
        a = variables.get(v_name, symbols[SYM_LOCAL], symbols[SYM_GLOBAL][1]) # try local, then global

    return a


def Local_recall(v_name, symbols):
    # automatically recalls the local variable
    a = variables.get(v_name, symbols[SYM_LOCAL], None)         # get the value from the local vars
    return a


def Global_recall(v_name, symbols):
    # automatically recalls the global variable
    with symbols[SYM_GLOBAL][0]:                                # lock the globals while we do this
        a = variables.get(v_name, None, symbols[SYM_GLOBAL][1]) # grab the value from the global vars

    return a
