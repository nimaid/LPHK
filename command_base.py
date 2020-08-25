# ##################################################
# ### CLASS Command_Basic                        ###
# ##################################################

# Command_Basic is a class that describes a command
class Command_Basic:
    def __init__(
        self, 
        Name: str          # The name of the command (what you put in the script)
        ):

        self.name = Name


    def Validate(
        self,
        idx: int,
        line,
        lines,
        split_line,
        symbols,
        pass_no            # pass_no 1 is a symbol gathering pass, pass_no 2 is a pass that requires
                           # symbols.  Any processing that does not set up labels should be done on
                           # pass 2. For example, goto can be checked on pass 2 to ensure the label
                           # exists
        ):

        return ("", "")           # error value!


    def Parse(
        self,
        idx: int,
        line,
        lines,
        split_line,
        symbols,
        pass_no            # pass_no 1 is a symbol gathering pass, pass_no 2 is a pass that requires
                           # symbols.  Any processing that does not set up labels should be done on
                           # pass 2.  Fatal errors can be generated on pass 1 or 2 for invalid syntax.
                           # Since errors will cause the process to abort, it is permissable for
                           # the same error to be reported on both passes 1 and 2 (since you won't get
                           # past pass 1).
        ):

        ret = self.Validate(idx, line, lines, split_line, symbols, pass_no)
        if ret == True:
            return True 

        if len(ret) != 2:
            ret = ("SYSTEM ERROR PARSING LINE " + str(idx) + ". '" + line + "' on pass " + str(pass_no), line)

        if ret[0]:
            print(ret[0])

        return ret


    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        return idx+1  # just move to next line


# ##################################################
# ### CLASS Command_Header                       ###
# ##################################################

# Command_Header is a class specifically defining a header command
class Command_Header(Command_Basic):
 
    def __init__(
        self, 
        Name: str,          # The name of the command (what you put in the script)
        Is_async: bool      # is this async?
        ):

        super().__init__(Name)
        self.is_async = Is_async

    def Validate(
        self,
        idx: int,
        line,
        lines,
        split_line,
        symbols,
        pass_no
        ):

        if idx != 0:
           return ("ERROR on line " + line + ". " + self.name + " must only appear on line 1.", -1)

        return (None, 0)


