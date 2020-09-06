import command_base, lp_events, scripts, variables, sys

lib = "cmds_rpnc" # name of this library (for logging)

# ##################################################
# ### CLASS RpnCalc_Rpn_Eval                     ###
# ##################################################

# class that defines the RPN_EVAL command.
# This command allows math to be performed on a simulated RPN calculator.
# This is useful because as a stack model it also provides the framework for 
# passing parameters to and from other routines if the stack is preserved
# in the symbol table.  In this version The output is to the log, but it
# is easily extended.
class RpnCalc_Rpn_Eval(command_base.Command_Basic):

    def add(self, 
        symbols,                   # the symbol table (stack, global vars, etc.)
        cmd,                       # the current command
        cmds):                     # the rest of the commands on the command line
        
        ret = 1                    # always initialise ret to 1, because the default is to 
                                   # step token by token along the expression
                                  
        a = variables.pop(symbols) # add requires 2 params, pop them off the stack...
        b = variables.pop(symbols) # 
        symbols['l_vars']['last x'] = a

        try:
            c = b+a                # RPN functions are defined as b (operator) a
        except:
            raise Exception("Error in addition: " + str(b) + " + " + str(a))  # error message in case of problem
            
        variables.push(symbols, c) # the result is pushed back on the stack
        
        return ret                 # and we return the number of tokens to skip (normally 1)
        

    def subtract(self, symbols, cmd, cmds):
        ret = 1
        a = variables.pop(symbols)
        b = variables.pop(symbols)
        symbols['l_vars']['last x'] = a

        try:
            c = b-a
        except:
            raise Exception("Error in subtraction: " + str(b) + " - " + str(a))
            
        variables.push(symbols, c)
        
        return ret


    def multiply(self, symbols, cmd, cmds):
        ret = 1
        a = variables.pop(symbols)
        b = variables.pop(symbols)
        symbols['l_vars']['last x'] = a

        try:
            c = b*a
        except:
            raise Exception("Error in multiplication: " + str(b) + " * " + str(a))
            
        variables.push(symbols, c)
        
        return ret


    def divide(self, symbols, cmd, cmds):
        ret = 1
        a = variables.pop(symbols)
        b = variables.pop(symbols)
        symbols['l_vars']['last x'] = a

        try:
            c = b/a
        except:
            raise Exception("Error in division: " + str(b) + " / " + str(a))  # Errors are highly possible here
            
        variables.push(symbols, c)
        
        return ret
 

    def i_div(self, symbols, cmd, cmds):
        ret = 1
        a = variables.pop(symbols)
        b = variables.pop(symbols)
        symbols['l_vars']['last x'] = a

        try:
            c = b//a
        except:
            raise Exception("Error in division: " + str(b) + " // " + str(a))  # Errors are highly possible here
            
        variables.push(symbols, c)
        
        return ret
 

    def mod(self, symbols, cmd, cmds):
        ret = 1
        a = variables.pop(symbols)
        b = variables.pop(symbols)
        symbols['l_vars']['last x'] = a

        try:
            c = b%a
        except:
            raise Exception("Error in mod: " + str(b) + " % " + str(a))  # Errors are highly possible here
            
        variables.push(symbols, c)
        
        return ret
 

    def view(self, symbols, cmd, cmds):
        # view the top of the stack (typically where results are)
        ret = 1
        print('Top of stack = ', variables.top(symbols, 1))       # we're going to peek at the top of the stack without popping
        
        return ret


    def view_s(self, symbols, cmd, cmds):
        # View the entire stack.  Probably a debugging tool.
        ret = 1
        print('Stack = ', symbols['stack'])                       # show the entire stack
        
        return ret


    def view_l(self, symbols, cmd, cmds):
        # View the local variables.  Probably a debugging tool.
        ret = 1
        print('Local = ', symbols['l_vars'])                      # show all local variables
        
        return ret


    def view_g(self, symbols, cmd, cmds):
        # View the global variables.  Probably a debugging tool.
        ret = 1
        with symbols['g_vars'][0]:                                # lock the globals while we do this
            print('Global = ', symbols['g_vars'][1])
        
        return ret


    def one_on_x(self, symbols, cmd, cmds):
        ret = 1
        a = variables.pop(symbols)
        symbols['l_vars']['last x'] = a

        try:
            variables.push(symbols, 1/a)
        except:
            raise Exception("Error in 1/x: " + str(a))  # Errors are highly possible here
            
        return ret
 

    def int_x(self, symbols, cmd, cmds):
        # get the integer part of x
        ret = 1
        a = variables.pop(symbols)
        symbols['l_vars']['last x'] = a

        try:
            variables.push(symbols, int(a))
        except:
            raise Exception("Error in '" + cmd + "' " + str(a))  # Errors are highly unlikely here
            
        return ret
 

    def frac_x(self, symbols, cmd, cmds):
        # get the fractionasl part of x
        ret = 1
        a = variables.pop(symbols)
        symbols['l_vars']['last x'] = a

        try:
            variables.push(symbols, a - int(a))
        except:
            raise Exception("Error in '" + cmd + "' " + str(a))  # Errors are highly unlikely here
            
        return ret
 

    def chs(self, symbols, cmd, cmds):
        ret = 1
        a = variables.pop(symbols)

        try:
            variables.push(symbols, -a)
        except:
            raise Exception("Error in chs: " + str(a))  # Errors are highly improbable here
            
        return ret
 

    def sqr(self, symbols, cmd, cmds):
        # calculates the square
        ret = 1
        a = variables.pop(symbols)
        symbols['l_vars']['last x'] = a

        try:
            c = a**2
        except:
            raise Exception("Error in squaring: " + str(a))
            
        variables.push(symbols, c)
        
        return ret


    def y_to_x(self, symbols, cmd, cmds):
        # calculates the square
        ret = 1
        a = variables.pop(symbols)
        b = variables.pop(symbols)
        symbols['l_vars']['last x'] = a

        try:
            c = b**a
        except:
           raise Exception("Error raising: " + str(b) + " to the " + str(a) + "th power")  # Errors are highly possible here

        variables.push(symbols, c)
        
        return ret


    def dup(self, symbols, cmd, cmds):
        # duplicates the value on the top of the stack
        ret = 1
        variables.push(symbols, variables.top(symbols, 1))
        
        return ret


    def pop(self, symbols, cmd, cmds):
        # removes top item from the stack
        ret = 1
        variables.pop(symbols)
        
        return ret


    def clst(self, symbols, cmd, cmds):
        # clears the stack
        ret = 1
        symbols['stack'].clear()
        
        return ret


    def last_x(self, symbols, cmd, cmds):
        # resurrects the last value of x that was "consumed" by an operation
        ret = 1
        try:
            a = symbols['l_vars']['last x']      # attempt to get the last-x value
        except:
            a = 0                                # default is zero
            
        variables.push(symbols, a)               # and push it onto the stack
        
        return ret


    def cl_l(self, symbols, cmd, cmds):
        # clears the stack
        ret = 1
        symbols['l_vars'].clear()
        
        return ret


    def stack_len(self, symbols, cmd, cmds):
        # clears the stack
        ret = 1
        variables.push(symbols, len(symbols['stack']))
        
        return ret


    def swap_x_y(self, symbols, cmd, cmds):
        # exchanges top two values on the stack
        ret = 1

        a = variables.pop(symbols)
        b = variables.pop(symbols)

        variables.push(symbols, a)
        variables.push(symbols, b)

        return ret


    def sto(self, symbols, cmd, cmds):
        # stores the value in local var if it exists, otherwise global var.  If neither, creates local
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)                    # what's the name of the variable?   
        a = variables.top(symbols, 1)                             # will be stored from the top of the stack

        with symbols['g_vars'][0]:                                # lock the globals while we do this
            if variables.is_defined(v, symbols['l_vars']):        # Is it local...
                variables.put(v, a, symbols['l_vars'])            # ...then store it locally
            elif variables.is_defined(v, symbols['g_vars'][1]):   # Is it global...
                variables.put(v, a, symbols['g_vars'][1])         # ...store it globally
            else:
                variables.put(v, a, symbols['l_vars'])            # default is to create new in locals
        
        return ret
        
        
    def sto_g(self, symbols, cmd, cmds):
        # stores the value on the top of the stack into the global variable named by the next token
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)                    # what's the name of the variable?     
        a = variables.top(symbols, 1)                             # will be stored from the top of the stack
        with symbols['g_vars'][0]:                                # lock the globals
           variables.put(v, a, symbols['g_vars'][1])              # and store it there
        
        return ret
        
        
    def sto_l(self, symbols, cmd, cmds):
        # stores the value on the top of the stack into the local variable named by the next token
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)   
        a = variables.top(symbols, 1)
        variables.put(v, a, symbols['l_vars'])
        
        return ret


    def rcl(self, symbols, cmd, cmds):
        # recalls a variable.  Try local first, then global
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)   
        with symbols['g_vars'][0]:                                # lock the globals while we do this
            a = variables.get(v, symbols['l_vars'], symbols['g_vars'][1])
        variables.push(symbols, a)
        
        return ret


    def rcl_l(self, symbols, cmd, cmds):
        # recalls a local variable (not overly useful, but avoids ambiguity)
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)   
        a = variables.get(v, symbols['l_vars'], None)
        variables.push(symbols, a)
        
        return ret
        

    def rcl_g(self, symbols, cmd, cmds):
        # recalls a global variable (useful if you define an identical local var)
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)   
        with symbols['g_vars'][0]:                                # lock the globals while we do this
            a = variables.get(v, None, symbols['g_vars'][1])      # grab the value from the global vars
        variables.push(symbols, a)                                # and push onto the stack
        
        return ret
        
    def x_eq_zero(self, symbols, cmd, cmds):
        # only continues eval if the top of the stack is 0
        if variables.top(symbols, 1) == 0:
            return 1
        else:
            return len(cmds)+1


    def x_ne_zero(self, symbols, cmd, cmds):
        # only continues eval if the top of the stack is not 0
        if variables.top(symbols, 1) != 0:
            return 1
        else:
            return len(cmds)+1


    def x_eq_y(self, symbols, cmd, cmds):
        # only continues eval if the two top values are equal
        if variables.top(symbols, 1) == variables.top(symbols, 2):
            return 1
        else:
            return len(cmds)+1


    def x_ne_y(self, symbols, cmd, cmds):
        # only continues eval if the two top values are not equal
        if variables.top(symbols, 1) != variables.top(symbols, 2):
            return 1
        else:
            return len(cmds)+1


    def x_gt_y(self, symbols, cmd, cmds):
        # only continue if the top value > the second value on the stack
        if variables.top(symbols, 1) > variables.top(symbols, 2):
            return 1
        else:
            return len(cmds)+1


    def x_ge_y(self, symbols, cmd, cmds):
        # only continue if the top value >= the second value on the stack
        if variables.top(symbols, 1) >= variables.top(symbols, 2):
            return 1
        else:
            return len(cmds)+1


    def x_lt_y(self, symbols, cmd, cmds):
        # only continue if the top value < the second value on the stack
        if variables.top(symbols, 1) < variables.top(symbols, 2):
            return 1
        else:
            return len(cmds)+1


    def x_le_y(self, symbols, cmd, cmds):
        # only continue if the top value <= the second value on the stack
        if variables.top(symbols, 1) <= variables.top(symbols, 2):
            return 1
        else:
            return len(cmds)+1


    def is_def(self, symbols, cmd, cmds):
        # only continue if the variable is defined (locally or globally is OK)
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)
        with symbols['g_vars'][0]:                                # lock the globals while we do this
            if variables.is_defined(v, symbols['g_vars'][1]) or variables.is_defined(v, symbols['l_vars']):
                return ret
            else:
                return len(cmds)+1


    def is_not_def(self, symbols, cmd, cmds):
        # only continue if the variable is not defined (either locally or globally)
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)
        with symbols['g_vars'][0]:                                # lock the globals while we do this
            if not (variables.is_defined(v, symbols['g_vars'][1]) or variables.is_defined(v, symbols['l_vars'])):
                return ret
            else:
                return len(cmds)+1


    def is_local_def(self, symbols, cmd, cmds):
        # only continue if the variable is defined locally
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)
        if variables.is_defined(v, symbols['l_vars']):
            return ret
        else:
            return len(cmds)+1


    def is_local_not_def(self, symbols, cmd, cmds):
        # only continue if the variable is not defined locally
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)
        if not variables.is_defined(v, symbols['l_vars']):
            return ret
        else:
            return len(cmds)+1


    def is_global_def(self, symbols, cmd, cmds):
        # only continue if the variable is defined globally
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)
        with symbols['g_vars'][0]:                                # lock the globals while we do this
            if variables.is_defined(v, symbols['g_vars'][1]):
                return ret
            else:
                return len(cmds)+1


    def is_global_not_def(self, symbols, cmd, cmds):
        # only continue if the variable is not defined globally
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)
        with symbols['g_vars'][0]:                                # lock the globals while we do this
            if not variables.is_defined(v, symbols['g_vars'][1]):
                return ret
            else:
                return len(cmds)+1


    def __init__(
        self, 
        ):

        super().__init__("RPN_EVAL")  # the name of the command as you have to enter it in the code

        self.operators = dict()
        self.operators["+"] = (self.add, 0)                 # +
        self.operators["-"] = (self.subtract, 0)            # -
        self.operators["*"] = (self.multiply, 0)            # *
        self.operators["/"] = (self.divide, 0)              # /
        self.operators["//"] = (self.i_div, 0)              # integer division
        self.operators["MOD"] = (self.mod, 0)               # modulus function
        self.operators["VIEW"] = (self.view, 0)             # View X
        self.operators["VIEW_S"] = (self.view_s, 0)         # View stack
        self.operators["VIEW_L"] = (self.view_l, 0)         # View local vars
        self.operators["VIEW_G"] = (self.view_g, 0)         # View global vars
        self.operators["1/X"] = (self.one_on_x, 0)          # 1/x
        self.operators["INT"] = (self.int_x, 0)             # integer portion of x
        self.operators["FRAC"] = (self.frac_x, 0)           # fractional part of x
        self.operators["CHS"] = (self.chs, 0)               # change sign of top of stack
        self.operators["SQR"] = (self.sqr, 0)               # **2
        self.operators["Y^X"] = (self.y_to_x, 0)            # **
        self.operators["DUP"] = (self.dup, 0)               # Duplicate top of stack
        self.operators["POP"] = (self.pop, 0)               # remove item from top of stack
        self.operators["CLST"] = (self.clst, 0)             # clear stack
        self.operators["LASTX"] = (self.last_x, 0)          # get the last value of x
        self.operators["CL_L"] = (self.cl_l, 0)             # clear local variables
        self.operators["STACK"] = (self.stack_len, 0)       # length of stack
        self.operators["X<>Y"] = (self.swap_x_y, 0)         # swap x and y
        self.operators[">"] = (self.sto, 1)                 # store
        self.operators[">L"] = (self.sto_l, 1)              # store local
        self.operators[">G"] = (self.sto_g, 1)              # store global
        self.operators["<"] = (self.rcl, 1)                 # recall
        self.operators["<L"] = (self.rcl_l, 1)              # recall local
        self.operators["<G"] = (self.rcl_g, 1)              # recall global
        self.operators["X=0?"] = (self.x_eq_zero, 0)        # is x zero?
        self.operators["X!=0?"] = (self.x_ne_zero, 0)       # is x not zero?
        self.operators["X=Y?"] = (self.x_eq_y, 0)           # is x = y?
        self.operators["X!=Y?"] = (self.x_ne_y, 0)          # is x != y?
        self.operators["X>Y?"] = (self.x_gt_y, 0)           # is x > y?
        self.operators["X>=Y?"] = (self.x_ge_y, 0)          # is x >= y?
        self.operators["X<Y?"] = (self.x_lt_y, 0)           # is x < y?
        self.operators["X<=Y?"] = (self.x_le_y, 0)          # is x <= y?
        self.operators["?"] = (self.is_def, 1)              # is var defined
        self.operators["!?"] = (self.is_not_def, 1)         # is var not defined
        self.operators["?L"] = (self.is_local_def, 1)       # is local var defined
        self.operators["!?L"] = (self.is_local_not_def, 1)  # is local var not defined
        self.operators["?G"] = (self.is_global_def, 1)      # is global var defined
        self.operators["!?G"] = (self.is_global_not_def, 1) # is global var not defined

    def Validate(
        self,
        idx: int,              # The current line number
        line,                  # The current line
        lines,                 # The current script
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:       # in Pass 1 we can do general syntax check and gather symbol definitions
            c_len = len(split_line)     # Number of tokens
            # check number of split_line
            if c_len < 2:
                return ("Line:" + str(idx+1) + " - Wrong number of parameters (at least 1 required) in " + self.name, line)

            i = 1                       # using a loop counter rather than an itterator because that makes the code similar to execution
          
            while i < c_len:  # for each item of the line of tokens
                cmd = split_line[i]     # get the current one
                
                n = None
                try:
                    n = float(cmd)      # we'll be happy with a float (since an int is a subset) 
                except ValueError:
                    pass
                else:
                    i += 1              # move along to the next token                    continue

                if n == None:
                    opr = cmd.upper()   # Convert to uppercase for searching
                    if opr in self.operators: # if it's valid
                        i = i + 1 + self.operators[opr][1]  # pull of additional parameters if required
                        if i > c_len:
                            return ("Line:" + str(idx+1) + " - Insufficient parameters after operator #" + str(i) + " '" + cmd + "' in " + self.name, line)                         
                    else:               # if invalid, report it
                        return ("Line:" + str(idx+1) + " - Invalid operator #" + str(i) + " '" + cmd + "' in " + self.name, line)                         
            
        return True 

 
    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    " + self.name + ": ", split_line[1:]) # coords[0] is the text "(x, y)"

        i = 1                       # using a loop counter rather than an itterator because it's hard to pass iters as params
      
        while i < len(split_line):  # for each item of the line of tokens
            cmd = split_line[i]     # get the current one
            
            n = None                # what we get if it's not a number
            try:
                n = int(cmd)        # is it an integer? 
            except ValueError:
                try:
                    n = float(cmd)  # how about a float? 
                except ValueError:
                    pass

            if n != None:           # if it was one of the above
                symbols['stack'].append(n) # ...put on the stack
                i += 1              # move along to the next token
            else:   
                opr = cmd.upper()       # Convert to uppercase for searching
                if opr in self.operators: # if it's valid
                    try:
                        i = i + self.operators[opr][0](symbols, opr, split_line[i:]) # run it
                    except:
                        print("Error in evaluation: '" + str(sys.exc_info()[1]) + "' at operator #" + str(i) + " on Line:" + str(idx+1) + " '" + cmd + "'")
                        break
                else:                   # if invalid, report it
                   print("Line:" + str(idx+1) + " - invalid operator #" + str(i) + " '" + cmd + "'")
                   break
        
        return idx+1                # Normal default exit to the next line


scripts.add_command(RpnCalc_Rpn_Eval())  # register the command

