# operations needed to access variables  

# NOTE that any locking is the responsibility of the calling code!


# Note that popping a value from an empty stack returns 0.  An alternative is
# to return an error
def pop(syms):
    # return the top valie from the stack (and remove it)
    try:
        return syms['stack'].pop()      # take the top value from the stack in the supplied symbol table
    except:
        return 0
        # raise Exception("Stack empty")

 
def push(syms, val):
    # put val on to the top of the stack
    syms['stack'].append(val)           # Push a value onto the stack in the supplied symbol table

 
# the top of the stack will also return 0 for an empty stack.   Alternatively it could
# return an error.
def top(syms, i):
    # peek at the top value of the stack without removing it (for i=1, y:i=2, z:i=3...)
    try:
        return syms['stack'][-i]
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
    
    
# check the number of variables allowed
def check_num(split_line, lens, idx, line, name):
    n = len(split_line)-1
    if n in lens:              
        return True                  # it's OK
    
    msg = "Line:" + str(idx+1) + " - Incorrect number of parameters (" + str(n) + ") supplied. "
    if len(lens) == 0:
        msg += "No valid number of parameters"
    elif len(lens) == 1:
        msg += str(lens[0])
    else:
        msg += ", ".join([str(el) for el in lens[0:-1]]) + ", " + str(lens[-1])    
       
    msg += " required for command '" + name + "'."     
    
    return (msg, line)


# check a parameter
def check_param(split_line, p, desc, idx, name, line, var_ok):
    try:
        temp = int(split_line[p])
    except:
        if not (var_ok and valid_var_name(split_line[p])):   # a variable is OK here
            return ("Line:" + str(idx+1) + " - '" + name + "' " + desc + " '" + split_line[p] + "' not valid.", line)

    return True 


# get the value of a parameter
def get_value(n, symbols):
    v = split_line[n]
    if valid_var_name(v):
        g_vars = symbols['g_vars']
        with g_vars[0]:                                # lock the globals while we do this
            v = variables.get(v, symbols['l_vars'], g_vars[1])
            
    return v
