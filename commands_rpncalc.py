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

        try:
            c = b/a
        except:
            raise Exception("Error in division: " + str(b) + " / " + str(a))  # Errors are highly possible here
            
        variables.push(symbols, c)
        
        return ret
 

    def view(self, symbols, cmd, cmds):
        # view the top of the stack (typically where results are)
        ret = 1
        print('Top of stack = ', variables.top(symbols, 1))
        
        return ret


    def view_s(self, symbols, cmd, cmds):
        # View the entire stack.  Probably a debugging tool.
        ret = 1
        print('Stack = ', symbols['stack'])
        
        return ret


    def view_l(self, symbols, cmd, cmds):
        # View the local variables.  Probably a debugging tool.
        ret = 1
        print('Local = ', symbols['l_vars'])
        
        return ret


    def view_g(self, symbols, cmd, cmds):
        # View the global variables.  Probably a debugging tool.
        ret = 1
        print('Global = ', symbols['g_vars'])
        
        return ret


    def one_on_x(self, symbols, cmd, cmds):
        ret = 1
        a = variables.pop(g_symbols)

        try:
            variables.push(symbols, 1/a)
        except:
            raise Exception("Error in 1/x: " + str(a))  # Errors are highly possible here
            
        return ret
 

    def sqr(self, symbols, cmd, cmds):
        # calculates the square
        ret = 1
        a = variables.pop(symbols)

        try:
            c = a*a
        except:
            raise Exception("Error in squaring: " + str(a))
            
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
        ret, v = variables.next_cmd(ret, cmds)   
        a = variables.top(symbols, 1)

        if variables.is_defined(v, symbols['l_vars']):
            variables.put(v, a, symbols['l_vars'])
        elif variables.is_defined(v, symbols['g_vars']):
            variables.put(v, a, symbols['g_vars'])
        else:
            variables.put(v, a, symbols['l_vars'])
        
        return ret
        
        
    def sto_g(self, symbols, cmd, cmds):
        # stores the value on the top of the stack into the global variable named by the next token
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)   
        a = variables.top(symbols, 1)
        variables.put(v, a, symbols['g_vars'])
        
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
        a = variables.get(v, symbols['l_vars'], symbols['g_vars'])
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
        a = variables.get(v, None, symbols['g_vars'])
        variables.push(symbols, a)
        
        return ret
        
    def x_eq_zero(self, symbols, cmd, cmds):
        if variables.top(symbols, 1) == 0:
            return 1
        else:
            return len(cmds)+1


    def x_ne_zero(self, symbols, cmd, cmds):
        if variables.top(symbols, 1) != 0:
            return 1
        else:
            return len(cmds)+1


    def x_eq_y(self, symbols, cmd, cmds):
        if variables.top(symbols, 1) == variables.top(symbols, 2):
            return 1
        else:
            return len(cmds)+1


    def x_ne_y(self, symbols, cmd, cmds):
        if variables.top(symbols, 1) != variables.top(symbols, 2):
            return 1
        else:
            return len(cmds)+1


    def x_gt_y(self, symbols, cmd, cmds):
        if variables.top(symbols, 1) > variables.top(symbols, 2):
            return 1
        else:
            return len(cmds)+1


    def x_ge_y(self, symbols, cmd, cmds):
        if variables.top(symbols, 1) >= variables.top(symbols, 2):
            return 1
        else:
            return len(cmds)+1


    def x_lt_y(self, symbols, cmd, cmds):
        if variables.top(symbols, 1) < variables.top(symbols, 2):
            return 1
        else:
            return len(cmds)+1


    def x_le_y(self, symbols, cmd, cmds):
        if variables.top(symbols, 1) <= variables.top(symbols, 2):
            return 1
        else:
            return len(cmds)+1


    def is_def(self, symbols, cmd, cmds):
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)
        if variables.is_defined(v, symbols['g_vars']) or variables.is_defined(v, symbols['l_vars']):
            return ret
        else:
            return len(cmds)+1


    def is_not_def(self, symbols, cmd, cmds):
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)
        if not (variables.is_defined(v, symbols['g_vars']) or variables.is_defined(v, symbols['l_vars'])):
            return ret
        else:
            return len(cmds)+1


    def is_local_def(self, symbols, cmd, cmds):
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)
        if variables.is_defined(v, symbols['l_vars']):
            return ret
        else:
            return len(cmds)+1


    def is_local_not_def(self, symbols, cmd, cmds):
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)
        if not variables.is_defined(v, symbols['l_vars']):
            return ret
        else:
            return len(cmds)+1


    def is_global_def(self, symbols, cmd, cmds):
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)
        if variables.is_defined(v, symbols['g_vars']):
            return ret
        else:
            return len(cmds)+1


    def is_global_not_def(self, symbols, cmd, cmds):
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)
        if not variables.is_defined(v, symbols['g_vars']):
            return ret
        else:
            return len(cmds)+1


    def __init__(
        self, 
        ):

        super().__init__("RPN_EVAL")  # the name of the command as you have to enter it in the code

        self.operators = dict()
        self.operators["+"] = self.add                 # +
        self.operators["-"] = self.subtract            # -
        self.operators["*"] = self.multiply            # *
        self.operators["/"] = self.divide              # /
        self.operators["VIEW"] = self.view             # View X
        self.operators["VIEW_S"] = self.view_s         # View stack
        self.operators["VIEW_L"] = self.view_l         # View local vars
        self.operators["VIEW_G"] = self.view_g         # View global vars
        self.operators["1/X"] = self.one_on_x          # 1/x
        self.operators["SQR"] = self.sqr               # **
        self.operators["DUP"] = self.dup               # Duplicate top of stack
        self.operators["POP"] = self.pop               # remove item from top of stack
        self.operators["CLST"] = self.clst             # clear stack
        self.operators["CL_L"] = self.cl_l             # clear local variables
        self.operators["STACK"] = self.stack_len       # length of stack
        self.operators["X<>Y"] = self.swap_x_y         # swap x and y
        self.operators[">"] = self.sto                 # store
        self.operators[">L"] = self.sto_l              # store local
        self.operators[">G"] = self.sto_g              # store global
        self.operators["<"] = self.rcl                 # recall
        self.operators["<L"] = self.rcl_l              # recall local
        self.operators["<G"] = self.rcl_g              # recall global
        self.operators["X=0?"] = self.x_eq_zero        # is x zero?
        self.operators["X!=0?"] = self.x_ne_zero       # is x not zero?
        self.operators["X=Y?"] = self.x_eq_y           # is x = y?
        self.operators["X!=Y?"] = self.x_ne_y          # is x != y?
        self.operators["X>Y?"] = self.x_gt_y           # is x > y?
        self.operators["X>=Y?"] = self.x_ge_y          # is x >= y?
        self.operators["X<Y?"] = self.x_lt_y           # is x < y?
        self.operators["X<=Y?"] = self.x_le_y          # is x <= y?
        self.operators["?"] = self.is_def              # is var defined
        self.operators["!?"] = self.is_not_def         # is var not defined
        self.operators["?L"] = self.is_local_def       # is local var defined
        self.operators["!?L"] = self.is_local_not_def  # is local var not defined
        self.operators["?G"] = self.is_global_def      # is global var defined
        self.operators["!?G"] = self.is_global_not_def # is global var not defined

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
            # check number of split_line
            if len(split_line) < 2:
                return ("Wrong number of parameters (at least 1 required) in " + self.name, line)

        # I'm not going to parse the commands at the moment.

        return True            # return True if there is no error 

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + lib + "] " + coords[0] + "    " + self.name + ": ", split_line[1:]) # coords[0] is the text "(x, y)"

        i = 1                       # using a loop counter rath erthan an itterator because it's hard to pass iters as params
        while i < len(split_line):  # for each item of the line of tokens
            cmd = split_line[i]     # get the current one
            
            try:
                n = float(cmd)      # numbers get... 
            except ValueError:
                pass
            else:
                symbols['stack'].append(n) # ...put on the stack
                i += 1              # move along to the next token
                continue

            opr = cmd.upper()       # Convert to uppercase for searching
            if opr in self.operators: # if it's valid
                try:
                    i = i + self.operators[opr](symbols, opr, split_line[i:]) # run it
                except:
                    print("Error in evaluation: '" + str(sys.exc_info()[1]) + "' at operator #" + str(i) + " '" + cmd + "'")
                    break
            else:                   # if invalid, report it
               print("invalid operator #" + str(i) + " '" + cmd + "'")
               break
        
        return idx+1           # Normal default exit to the next line


scripts.add_command(RpnCalc_Rpn_Eval())  # register the command

