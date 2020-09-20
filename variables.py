from constants import *

# operations needed to access variables  

# NOTE that any locking is the responsibility of the calling code!


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
    return vbls and name.lower() in vbls


# This returns 0 if the variable is not defined.  An alternative is to return an error
def get(name, l_vbls, g_vbls):
    # get a variable.  look in one symbol table, then the next.
    # this allows an order to be defined to get local vars then global
    name = name.lower()
    
    if is_defined(name, l_vbls):    # First look in the local symbol table (if defined)
        return l_vbls[name]
    if is_defined(name, g_vbls):    # then the global one
        return g_vbls[name]
    return 0 
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


# variable names should start with an alpha character
def valid_var_name(v):
    return len(v) > 0 and ord(v[0].upper()) in range(ord('A'), ord('Z')+1)


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
            return (error_msg(idx, name, desc, p, None, 'required ' + val[AV_TYPE][AVT_DESC] + ' parameter not present'), btn.line[idx])
    
    try:
        temp = val[AV_TYPE][AVT_CONV](split_line[p])
    except:
        if val[AV_VAR_OK] and valid_var_name(split_line[p]):   # a variable is OK here
            return True
        return (error_msg(idx, cmd.name, val[AV_DESCRIPTION], p, split_line[p], 'not a valid ' + val[AV_TYPE][AVT_DESC]), btn.line[idx])

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
            return (error_msg(idx, name, desc, p, None, 'required parameter not present'), btn.line[idx])
    
    try:
        temp = conv(split_line[p])
    except:
        if var_ok and valid_var_name(split_line[p]):   # a variable is OK here
            return True
        return (error_msg(idx, name, desc, p, split_line[p], 'not valid'), btn.line[idx])

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
    if v:
        if float(v) != 0:
            return True
        else:
            return error_msg(idx, name, desc, p, param, 'must not be zero')
    else:
        return error_msg(idx, name, desc, p, param, 'must be an integer')

        
def Validate_gt_zero(v, idx, name, desc, p, param):
    if v:
        if v > 0:
            return True
        else:
            return error_msg(idx, name, desc, p, param, 'must be greater than zero')
    else:
        return error_msg(idx, name, desc, p, param, 'must be an integer')
        
        
def Validate_ge_zero(v, idx, name, desc, p, param):
    if v:
        if v >= 0:
            return True
        else:
            return error_msg(idx, name, desc, p, param, 'must not be less than zero')
    else:
        return error_msg(idx, name, desc, p, param, 'must be an integer')
        


