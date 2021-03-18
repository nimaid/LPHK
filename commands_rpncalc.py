import command_base, lp_events, scripts, variables, sys, param_convs
from constants import *

LIB = "cmds_rpnc" # name of this library (for logging)

# note that if you don't like RPN and prefer to write algebraic expressions
# all you need to do is create a command that converts algebraic commands to
# postfix (RPN) and you can use the RPN evaluator to process it.

# ##################################################
# ### CLASS RpnCalc_Rpn_Eval                     ###
# ##################################################

# class that defines the RPN_EVAL command.
# This command allows math to be performed on a simulated RPN calculator.
# This is useful because as a stack model it also provides the framework for
# passing parameters to and from other routines if the stack is preserved
# in the symbol table.  In this version The output is to the log, but it
# is easily extended.
class Rpn_Eval(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("RPN_EVAL",  # the name of the command as you have to enter it in the code
        LIB)

        # this command does not have a standard list of fields, so we need to do some stuff manually
        self.valid_max_params = 255        # There is no maximum, but this is a reasonable limit!
        self.valid_num_params = [1, None]  # one or more is OK

        self.run_states = [RS_INIT, RS_RUN, RS_FINAL]  # No need for anything other than running.
        self.validation_states = [VS_PASS_1]         # No need for anything other than the first pass

        # Create a register for the sub-commands
        self.operators = dict()

        # Now register the operators
        self.Register_operators()


    # We can simply override the first pass validation
    def Partial_validate_step_pass_1(self, ret, btn, idx, split_line):
        # validate the number of parameters
        ret = self.Validate_param_count(ret, btn, idx, split_line)

        if ((type(ret) == bool) and ret):
            c_len = len(split_line)     # Number of tokens
            i = 1
            while i < c_len:            # for each item of the line of tokens
                cmd = split_line[i]     # get the current one

                n = None
                try:
                    n = float(cmd)      # we'll be happy with a float (since an int is a subset)
                except ValueError:
                    pass
                else:
                    i += 1              # move along to the next token
                    continue

                if n == None:
                    opr = cmd.upper()   # Convert to uppercase for searching
                    if opr in self.operators: # if it's valid
                        for p in range(self.operators[opr][1]):
                            if i + p + 1 >= c_len:
                                return ("Line:" + str(idx+1) + " - Insufficient tokens for parameter#" + str(p+1) + " of operator #" + str(i) + " '" + cmd + "' in " + self.name, btn.Line(idx))
                            else:
                                param = split_line[i+p+1]
                                if not variables.valid_var_name(param):
                                    return ("Line:" + str(idx+1) + " - parameter#" + str(p+1) + " '" + param + "' of operator #" + str(i) + " '" + cmd + " must start with alpha character in " + self.name, btn.Line(idx))
                        i = i + 1 + self.operators[opr][1]  # pull of additional parameters if required
                        if i > c_len:
                            return ("Line:" + str(idx+1) + " - Insufficient parameters after operator #" + str(i) + " '" + cmd + "' in " + self.name, btn.Line(idx))
                    else:               # if invalid, report it
                        return ("Line:" + str(idx+1) + " - Invalid operator #" + str(i) + " '" + cmd + "' in " + self.name, btn.Line(idx))

        return ret


    # define how to process.  We could override something at a lower level, but
    # this retains any initialisation and finalization and simplifies return
    # requirements
    def Process(self, btn, idx, split_line):
        print("[" + self.lib + "] " + btn.coords + "  Line:" + str(idx+1) + "    " + self.name + ": ", split_line[1:]) # btn.coords is the text "(x, y)"

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
                btn.symbols[SYM_STACK].append(n) # ...put on the stack
                i += 1              # move along to the next token
                continue

            opr = cmd.upper()       # Convert to uppercase for searching
            if opr in self.operators: # if it's valid
                try:
                    # capture the return value from the operator
                    o_ret = self.operators[opr][0](btn.symbols, opr, split_line[i:]) # run it

                    # boolean returns are special
                    if type(o_ret) == bool:
                        if o_ret:
                            # True just does a normal "go to next"
                            i = i + self.operators[opr][1] + 1
                        else:
                            # but False aborts the execution of the RPN calc AND terminates the script
                            print("Line:" + str(idx+1) + " - RPN terminates script")
                            return -1
                    else:
                        # non-boolean returns are simply indications to skip ahead the appropriate amount
                        i = i + o_ret
                except:
                    print("Error in evaluation: '" + str(sys.exc_info()[1]) + "' at operator #" + str(i) + " on Line:" + str(idx+1) + " '" + cmd + "'")
                    break
            else:                   # if invalid, report it
               print("Line:" + str(idx+1) + " - invalid operator #" + str(i) + " '" + cmd + "'")
               break

        return idx+1                # Normal default exit to the next line


    # register all the operators for RPN_EVAL:
    def Register_operators(self):
        #              operator     function               # params
        self.operators["+"]      = (self.add,               0) # +
        self.operators["-"]      = (self.subtract,          0) # -
        self.operators["*"]      = (self.multiply,          0) # *
        self.operators["/"]      = (self.divide,            0) # /
        self.operators["//"]     = (self.i_div,             0) # integer division
        self.operators["MOD"]    = (self.mod,               0) # modulus function
        self.operators["VIEW"]   = (self.view,              0) # View X
        self.operators["VIEW_S"] = (self.view_s,            0) # View stack
        self.operators["VIEW_L"] = (self.view_l,            0) # View local vars
        self.operators["VIEW_G"] = (self.view_g,            0) # View global vars
        self.operators["1/X"]    = (self.one_on_x,          0) # 1/x
        self.operators["INT"]    = (self.int_x,             0) # integer portion of x
        self.operators["FRAC"]   = (self.frac_x,            0) # fractional part of x
        self.operators["CHS"]    = (self.chs,               0) # change sign of top of stack
        self.operators["SQR"]    = (self.sqr,               0) # **2
        self.operators["Y^X"]    = (self.y_to_x,            0) # **
        self.operators["DUP"]    = (self.dup,               0) # Duplicate top of stack
        self.operators["POP"]    = (self.pop,               0) # remove item from top of stack
        self.operators["CLST"]   = (self.clst,              0) # clear stack
        self.operators["LASTX"]  = (self.last_x,            0) # get the last value of x
        self.operators["CL_L"]   = (self.cl_l,              0) # clear local variables
        self.operators["STACK"]  = (self.stack_len,         0) # length of stack
        self.operators["X<>Y"]   = (self.swap_x_y,          0) # swap x and y
        self.operators[">"]      = (self.sto,               1) # store
        self.operators[">L"]     = (self.sto_l,             1) # store local
        self.operators[">G"]     = (self.sto_g,             1) # store global
        self.operators["<"]      = (self.rcl,               1) # recall
        self.operators["<L"]     = (self.rcl_l,             1) # recall local
        self.operators["<G"]     = (self.rcl_g,             1) # recall global
        self.operators["X=0?"]   = (self.x_eq_zero,         0) # is x zero?
        self.operators["X!=0?"]  = (self.x_ne_zero,         0) # is x not zero?
        self.operators["X=Y?"]   = (self.x_eq_y,            0) # is x = y?
        self.operators["X!=Y?"]  = (self.x_ne_y,            0) # is x != y?
        self.operators["X>Y?"]   = (self.x_gt_y,            0) # is x > y?
        self.operators["X>=Y?"]  = (self.x_ge_y,            0) # is x >= y?
        self.operators["X<Y?"]   = (self.x_lt_y,            0) # is x < y?
        self.operators["X<=Y?"]  = (self.x_le_y,            0) # is x <= y?
        self.operators["?"]      = (self.is_def,            1) # is var defined
        self.operators["!?"]     = (self.is_not_def,        1) # is var not defined
        self.operators["?L"]     = (self.is_local_def,      1) # is local var defined
        self.operators["!?L"]    = (self.is_local_not_def,  1) # is local var not defined
        self.operators["?G"]     = (self.is_global_def,     1) # is global var defined
        self.operators["!?G"]    = (self.is_global_not_def, 1) # is global var not defined
        self.operators["ABORT"]  = (self.abort_script,      0) # abort the script (not just the rpn calc)
        self.operators["SUBSTR"] = (self.substr,            0) # x gets str(z)[x:y]


    def add(self,
        symbols,                   # the symbol table (stack, global vars, etc.)
        cmd,                       # the current command
        cmds):                     # the rest of the commands on the command line

        ret = 1                    # always initialise ret to 1, because the default is to
                                   # step token by token along the expression

        a = variables.pop(symbols) # add requires 2 params, pop them off the stack...
        b = variables.pop(symbols) #
        symbols[SYM_LOCAL]['last x'] = a

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
        symbols[SYM_LOCAL]['last x'] = a

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
        symbols[SYM_LOCAL]['last x'] = a

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
        symbols[SYM_LOCAL]['last x'] = a

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
        symbols[SYM_LOCAL]['last x'] = a

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
        symbols[SYM_LOCAL]['last x'] = a

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
        print('Stack = ', symbols[SYM_STACK])                       # show the entire stack

        return ret


    def view_l(self, symbols, cmd, cmds):
        # View the local variables.  Probably a debugging tool.
        ret = 1
        print('Local = ', symbols[SYM_LOCAL])                      # show all local variables

        return ret


    def view_g(self, symbols, cmd, cmds):
        # View the global variables.  Probably a debugging tool.
        ret = 1
        with symbols[SYM_GLOBAL][0]:                                # lock the globals while we do this
            print('Global = ', symbols[SYM_GLOBAL][1])

        return ret


    def one_on_x(self, symbols, cmd, cmds):
        ret = 1
        a = variables.pop(symbols)
        symbols[SYM_LOCAL]['last x'] = a

        try:
            variables.push(symbols, 1/a)
        except:
            raise Exception("Error in 1/x: " + str(a))  # Errors are highly possible here

        return ret


    def int_x(self, symbols, cmd, cmds):
        # get the integer part of x
        ret = 1
        a = variables.pop(symbols)
        symbols[SYM_LOCAL]['last x'] = a

        try:
            variables.push(symbols, int(a))
        except:
            raise Exception("Error in '" + cmd + "' " + str(a))  # Errors are highly unlikely here

        return ret


    def frac_x(self, symbols, cmd, cmds):
        # get the fractionasl part of x
        ret = 1
        a = variables.pop(symbols)
        symbols[SYM_LOCAL]['last x'] = a

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
        symbols[SYM_LOCAL]['last x'] = a

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
        symbols[SYM_LOCAL]['last x'] = a

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
        symbols[SYM_STACK].clear()

        return ret


    def last_x(self, symbols, cmd, cmds):
        # resurrects the last value of x that was "consumed" by an operation
        ret = 1
        try:
            a = symbols[SYM_LOCAL]['last x']      # attempt to get the last-x value
        except:
            a = 0                                # default is zero

        variables.push(symbols, a)               # and push it onto the stack

        return ret


    def cl_l(self, symbols, cmd, cmds):
        # clears the stack
        ret = 1
        symbols[SYM_LOCAL].clear()

        return ret


    def stack_len(self, symbols, cmd, cmds):
        # returns stack length
        ret = 1
        variables.push(symbols, len(symbols[SYM_STACK]))

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
        ret, v = variables.next_cmd(ret, cmds)                      # what's the name of the variable?
        a = variables.top(symbols, 1)                               # will be stored from the top of the stack

        variables.Auto_store(v, a, symbols)                          # "auto store" the value

        return ret


    def sto_g(self, symbols, cmd, cmds):
        # stores the value on the top of the stack into the global variable named by the next token
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)                      # what's the name of the variable?
        a = variables.top(symbols, 1)                               # will be stored from the top of the stack
        with symbols[SYM_GLOBAL][0]:                                # lock the globals
           variables.put(v, a, symbols[SYM_GLOBAL][1])              # and store it there

        return ret


    def sto_l(self, symbols, cmd, cmds):
        # stores the value on the top of the stack into the local variable named by the next token
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)
        a = variables.top(symbols, 1)
        variables.put(v, a, symbols[SYM_LOCAL])

        return ret


    def rcl(self, symbols, cmd, cmds):
        # recalls a variable.  Try local first, then global
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)
        with symbols[SYM_GLOBAL][0]:                                               # lock the globals while we do this
            a = variables.get(v, symbols[SYM_LOCAL], symbols[SYM_GLOBAL][1], param_convs._any) # as an integer
        variables.push(symbols, a)

        return ret


    def rcl_l(self, symbols, cmd, cmds):
        # recalls a local variable (not overly useful, but avoids ambiguity)
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)
        a = variables.get(v, symbols[SYM_LOCAL], None, param_convs._any)        # as an integer
        variables.push(symbols, a)

        return ret


    def rcl_g(self, symbols, cmd, cmds):
        # recalls a global variable (useful if you define an identical local var)
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)
        with symbols[SYM_GLOBAL][0]:                                            # lock the globals while we do this
            a = variables.get(v, None, symbols[SYM_GLOBAL][1], param_convs._any)# grab the value from the global vars as an integer
        variables.push(symbols, a)                                              # and push onto the stack

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
        with symbols[SYM_GLOBAL][0]:                                # lock the globals while we do this
            if variables.is_defined(v, symbols[SYM_GLOBAL][1]) or variables.is_defined(v, symbols[SYM_LOCAL]):
                return ret
            else:
                return len(cmds)+1


    def is_not_def(self, symbols, cmd, cmds):
        # only continue if the variable is not defined (either locally or globally)
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)
        with symbols[SYM_GLOBAL][0]:                                # lock the globals while we do this
            if not (variables.is_defined(v, symbols[SYM_GLOBAL][1]) or variables.is_defined(v, symbols[SYM_LOCAL])):
                return ret
            else:
                return len(cmds)+1


    def is_local_def(self, symbols, cmd, cmds):
        # only continue if the variable is defined locally
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)
        if variables.is_defined(v, symbols[SYM_LOCAL]):
            return ret
        else:
            return len(cmds)+1


    def is_local_not_def(self, symbols, cmd, cmds):
        # only continue if the variable is not defined locally
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)
        if not variables.is_defined(v, symbols[SYM_LOCAL]):
            return ret
        else:
            return len(cmds)+1


    def is_global_def(self, symbols, cmd, cmds):
        # only continue if the variable is defined globally
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)
        with symbols[SYM_GLOBAL][0]:                                # lock the globals while we do this
            if variables.is_defined(v, symbols[SYM_GLOBAL][1]):
                return ret
            else:
                return len(cmds)+1


    def is_global_not_def(self, symbols, cmd, cmds):
        # only continue if the variable is not defined globally
        ret = 1
        ret, v = variables.next_cmd(ret, cmds)
        with symbols[SYM_GLOBAL][0]:                                # lock the globals while we do this
            if not variables.is_defined(v, symbols[SYM_GLOBAL][1]):
                return ret
            else:
                return len(cmds)+1


    def abort_script(self, symbols, cmd, cmds):
        # cause the script to be aborted
        return False


    def substr(self, symbols, cmd, cmds):
        # does a substring
        x = variables.pop(symbols)
        y = variables.pop(symbols)
        z = variables.pop(symbols)

        r = str(z)[y:x]
        variables.push(symbols, r)

        return 1


scripts.Add_command(Rpn_Eval())  # register the command


# ##################################################
# ### CLASS RPN_SET                              ###
# ##################################################

# class that defines the RPN_SET command -- Sets a variable to a string value (or a heap of appended string values)
class Rpn_Set(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("RPN_SET, Sets a string to the concatenation of all the variables passed to it",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("Variable",   False, AVV_REQD, PT_STR,  None,                       None),
            ("Value",      False, AVV_YES,  PT_STRS, None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2,           "    Assign '{2}' to variable {1}"),
            ) )


    def Process(self, btn, idx, split_line):
        val = ''
        for i in range(2, self.Param_count(btn)+1): # for each parameter (after the first)
            val += str(self.Get_param(btn, i))      # append all the values (force to string)
        self.Set_param(btn, 1, val)                 # pass the combined string back


scripts.Add_command(Rpn_Set())  # register the command


# constants for RPN_CLEAR
RC_GLOBALS = "GLOBALS"
RC_LOCALS = "LOCALS"
RC_GLOBAL = "GLOBAL"
RC_LOCAL = "LOCAL"
RC_STACK = "STACK"
RC_VARS = "VARS"
RC_VAR = "VAR"
RC_ALL = "ALL"

RCG_GLOBAL = [RC_GLOBALS, RC_VARS, RC_ALL]
RCG_LOCAL = [RC_LOCALS, RC_VARS, RC_ALL]
RCG_STACK = [RC_STACK, RC_ALL]
RCG_G_VAR = [RC_GLOBAL, RC_VAR]
RCG_L_VAR = [RC_LOCAL, RC_VAR]
RCG_ANY_VAR = [RC_GLOBAL, RC_LOCAL, RC_VAR]
RCG_ALL = [RC_ALL, RC_VARS, RC_GLOBALS, RC_LOCALS, RC_VAR, RC_GLOBAL, RC_LOCAL, RC_STACK]

# ##################################################
# ### CLASS RPN_CLEAR                            ###
# ##################################################

# class that defines the RPN_CLEAR command -- clears variables
class Rpn_Clear(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("RPN_CLEAR, Clear variables or stack",
            LIB,
            (
            # Desc         Opt    Var       type      p1_val                      p2_val
            ("Function",   False, AVV_NO,   PT_WORD,  None,                       None),
            ("Variable",   True,  AVV_NO,   PT_WORDS, None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (1,           "    Clear {1}"),
            (2,           "    Clear {1}: {2}"),
            ) )

        self.doc= ["If parameter 1 is:",
                   f"     '{RC_GLOBALS}'                All the global variables are cleared",
                   f"     '{RC_LOCALS}'                 All the local variables are cleared",
                   f"     '{RC_VARS}'                   All variables are cleared",
                   f"     '{RC_STACK}'                  The stack is cleared",
                   f"     '{RC_ALL}'                    All variables and the stack are cleared",
                   f"     '{RC_GLOBAL}' v1 [v2 [v3...]] Named global variables v1... are deleted",
                   f"     '{RC_LOCAL}' v1 [v2 [v3...]]  Named local variables v1... are deleted",
                   f"     '{RC_VAR}' v1 [v2 [v3...]]    Named variables v1... are deleted"]


    def Process(self, btn, idx, split_line):
        f = (self.Get_param(btn, 1)).upper()

        if f in RCG_GLOBAL:
            with btn.symbols[SYM_GLOBAL][0]:
                btn.symbols[SYM_GLOBAL][1].clear()    # clear all global variables
        if f in RCG_LOCAL:
            btn.symbols[SYM_LOCAL].clear()            # clear all local variables
        if f in RCG_STACK:
            btn.symbols[SYM_STACK].clear()            # clear the stack
        if f in RCG_G_VAR:
            for i in range(2, self.Param_count(btn)+1):
                with btn.symbols[SYM_GLOBAL][0]:
                    variables.undef(self.Get_param(btn, i), btn.symbols[SYM_GLOBAL][1])
        if f in RCG_L_VAR:
            for i in range(2, self.Param_count(btn)+1):
                variables.undef(self.Get_param(btn, i), btn.symbols[SYM_LOCAL])


    def Partial_validate_step_pass_1(self, ret, btn, idx, split_line):
        ret = super().Partial_validate_step_pass_1(ret, btn, idx, split_line)     # perform the original pass 1 validation

        if ret == None or ((type(ret) == bool) and ret):                          # if the original validation hasn't raised an error
            if not split_line[1] in RCG_ALL:                                      # invalid subcommand
                c_ok = ', '.join(RCG_ALL[:-1]) + ', or ' + RCG_ALL[-1]
                s_err = f"Invalid subcommand {split_line[1]} when expecting {c_ok}."
                return (s_err, btn.Line(idx))
        return ret


scripts.Add_command(Rpn_Clear())  # register the command