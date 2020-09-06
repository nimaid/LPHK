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
