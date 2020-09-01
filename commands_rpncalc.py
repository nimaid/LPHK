import command_base, lp_events, scripts

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

    def add(self, stack):
        a = stack.pop()
        b = stack.pop()
        stack.append(b+a)

    def subtract(self, stack):
        a = stack.pop()
        b = stack.pop()
        stack.append(b-a)

    def multiply(self, stack):
        a = stack.pop()
        b = stack.pop()
        stack.append(b*a)

    def divide(self, stack):
        a = stack.pop()
        b = stack.pop()
        stack.append(b/a)

    def view(self, stack):
        print('Top of stack = ', stack[-1])

    def views(self, stack):
        print('Stack = ', stack)

    def pi(self, stack):
        stack.append(3.1415926535)

    def sqr(self, stack):
        a = stack.pop()
        stack.append(a*a)

    def dup(self, stack):
        stack.append(stack[-1])

    def clst(self, stack):
        stack.clear()

    def __init__(
        self, 
        ):

        super().__init__("RPN_EVAL")  # the name of the command as you have to enter it in the code

        self.operators = dict()
        self.operators["+"] = self.add
        self.operators["-"] = self.subtract
        self.operators["*"] = self.multiply
        self.operators["/"] = self.divide
        self.operators["VIEW"] = self.view
        self.operators["VIEWS"] = self.views
        self.operators["PI"] = self.pi
        self.operators["SQR"] = self.sqr
        self.operators["DUP"] = self.dup
        self.operators["CLST"] = self.clst

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

        stack = [] # this is local, but it could be stored globally in the symbol table!

        for i in split_line[1:]:
            try:
                n = float(i)
                ok = True
            except ValueError:
                ok = False

            if ok:
                stack.append(n)
                continue

            opr = i.upper()
            if opr in self.operators:
                self.operators[opr](stack)
            else:
               print("invalid operator '", i, "'")
               break
        
        return idx+1           # Normal default exit to the next line


scripts.add_command(RpnCalc_Rpn_Eval())  # register the command

