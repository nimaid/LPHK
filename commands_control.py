import command_base, lp_events, scripts

lib = "cmds_ctrl" # name of this library (for logging)

# ##################################################
# ### CLASS Control_Comment                      ###
# ##################################################

# class that defines the comment command (single quote at beginning of line)
# this is special because it has some different handling in the main code
# to allow it to work without a space following it
class Control_Comment(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("-")  # the name of the command as you have to enter it in the code

    def Validate(
        self,
        idx: int,              # The current line number
        line,                  # The current line
        lines,                 # The current script
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        return True            # return True if there is no error (a comment can't ever be an error)  

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + lib + "] " + coords[0] + "    comment: " + split_line[1:]) # coords[0] is the text "(x, y)"

        return idx+1           # Return the number of the next line to execute, -1 to exit 


scripts.add_command(Control_Comment())  # register the command


# ##################################################
# ### CLASS Control_Label                        ###
# ##################################################

# class that defines the LABEL command (a target of GOTO's etc)
class Control_Label(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("LABEL")  # the name of the command as you have to enter it in the code

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
            if len(split_line) != 2:
                return ("Wrong number of parameters in " + self.name, line)

            # check for duplicate label
            if split_line[1] in symbols["labels"]:        # Does the label already exist (that's bad)?
                return ("duplicate LABEL", line)

            # add label to symbol table                   # Add the new label to the labels in the symbol table
            symbols["labels"][split_line[1]] = idx        # key is label, data is line number

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + lib + "] " + coords[0] + "    Label: " + split_line[1])

        return idx+1           # Nothing to do when executing a label


scripts.add_command(Control_Label())  # register the command


# ##################################################
# ### CLASS Control_Goto_Label                   ###
# ##################################################

# class that defines the GOTO_LABEL command
class Control_Goto_Label(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("GOTO_LABEL")  # the name of the command as you have to enter it in the code

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
            if len(split_line) != 2:
                return ("Wrong number of parameters in " + self.ame, line)

        if pass_no == 2:       # in Pass 2 we can check to make sure referenced symbols exist
            if split_line[1] not in symbols["labels"]:
                return ("Target not found for " + self.name, line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + lib + "] " + coords[0] + "    Goto LABEL " + split_line[1])

        # check for label
        if not split_line[1] in symbols["labels"]:          # The label should always exist
            print("missing LABEL '" + split_line[1] + "'")  # otherwise an error
            return -1
        else:
            return symbols["labels"][split_line[1]]         # normally we return the line number the label is on

        return idx+1           # We'll never get here


scripts.add_command(Control_Goto_Label())  # register the command


# ##################################################
# ### CLASS Control_If_Pressed_Goto_Label        ###
# ##################################################

# class that defines the IF_PRESSED_GOTO_LABEL command
class Control_If_Pressed_Goto_Label(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("IF_PRESSED_GOTO_LABEL")  # the name of the command as you have to enter it in the code

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
            if len(split_line) != 2:
                return ("'" + split_line[0] + "' takes exactly 1 argument.", line)

        if pass_no == 2:       # in Pass 2 we can check to make sure referenced symbols exist
            if split_line[1] not in symbols["labels"]:
                return ("Target not found for " + self.name, line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + lib + "] " + coords[0] + "    If key is pressed goto LABEL " + split_line[1])
        if not split_line[1] in symbols["labels"]:            # The label should always exist
            print("missing LABEL '" + split_line[1] + "'")    # otherwise an error
            return -1
        else:
            if lp_events.pressed[coords[1]][coords[2]]:       # coords[1] is x, and coords[2] is y
                if split_line[1] in symbols["labels"]:        # The label should always exist
                    return symbols["labels"][split_line[1]]   # and we return the line number the label is on
                else:
                    print("missing LABEL '" + split_line[1] + "'")  # otherwise an error
                    return -1

        return idx+1


scripts.add_command(Control_If_Pressed_Goto_Label())  # register the command


# ##################################################
# ### CLASS Control_If_Unpressed_Goto_Label      ###
# ##################################################

# class that defines the IF_UNPRESSED_GOTO_LABEL command
class Control_If_Unpressed_Goto_Label(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("IF_UNPRESSED_GOTO_LABEL")  # the name of the command as you have to enter it in the code

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
            if len(split_line) != 2:
               return ("'" + split_line[0] + "' takes exactly 1 argument.", line)

        if pass_no == 2:       # in Pass 2 we can check to make sure referenced symbols exist
            if split_line[1] not in symbols["labels"]:
                return ("Target not found for " + self.name, line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + lib + "] " + coords[0] + "    If key is not pressed goto LABEL " + split_line[1])

        if not split_line[1] in symbols["labels"]:            # The label should always exist
            print("missing LABEL '" + split_line[1] + "'")    # otherwise an error
            return -1
        else:
            if not lp_events.pressed[coords[1]][coords[2]]:   # if the key is pressed
                return symbols["labels"][split_line[1]]       # jump to the label

        return idx+1


scripts.add_command(Control_If_Unpressed_Goto_Label())  # register the command


# ##################################################
# ### CLASS Control_Repeat_Label                 ###
# ##################################################

# class that defines the REPEAT_LABEL command
class Control_Repeat_Label(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("REPEAT_LABEL")  # the name of the command as you have to enter it in the code

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
            if len(split_line) != 3:
                return ("'" + split_line[0] + "' needs both a label name and how many times to repeat.", line)

            try:
                temp = int(split_line[2])
                if temp < 1:
                    return (split_line[0] + " requires a minimum of 1 repeat.", line)
                else:
                    symbols["repeats"][idx] = int(split_line[2])
                    symbols["original"][idx] = int(split_line[2])
            except:
                return (split_line[0] + " number of repeats '" + split_line[2] + "' not valid.", line)

        if pass_no == 2:       # in Pass 2 we can check to make sure referenced symbols exist
            if split_line[1] not in symbols["labels"]:
                return ("Target not found for " + self.name, line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + lib + "] " + coords[0] + "    Repeat LABEL " + split_line[1] + " " + \
            split_line[2] + " times max")

        if not split_line[1] in symbols["labels"]:          # The label should always exist
            print("missing LABEL '" + split_line[1] + "'")  # otherwise an error
            return -1
        else:
            if symbols["repeats"][idx] > 0:
                print("[" + lib + "] " + coords[0] + "        " + str(symbols["repeats"][idx]) + " repeats left.")
                symbols["repeats"][idx] -= 1
                return symbols["labels"][split_line[1]]
            else:
                print("[" + lib + "] " + coords[0] + "        No repeats left, not repeating.")

        return idx+1


scripts.add_command(Control_Repeat_Label())  # register the command


# ##################################################
# ### CLASS Control_Repeat                       ###
# ##################################################

# class that defines the REPEAT command.  This operates more like a 
# traditional repeat/until by causing the code to repeat n times (rather than
# n+1, and it resets the counter at the end
class Control_Repeat(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("REPEAT")  # the name of the command as you have to enter it in the code

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
            if len(split_line) != 3:
                return ("'" + split_line[0] + "' needs both a label name and how many times to repeat.", line)

            try:
                temp = int(split_line[2])
                if temp < 1:
                    return (split_line[0] + " requires a minimum of 1 repeat.", line)
                else:
                    symbols["repeats"][idx] = int(split_line[2])-1
                    symbols["original"][idx] = int(split_line[2])-1
            except:
               return (split_line[0] + " number of repeats '" + split_line[2] + "' not valid.", line)

        if pass_no == 2:       # in Pass 2 we can check to make sure referenced symbols exist
            if split_line[1] not in symbols["labels"]:
                return ("Target not found for " + self.name, line)

            if symbols["labels"][split_line[1]] > idx:
                return ("Target for " + self.name + " must preceed the command.", line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + lib + "] " + coords[0] + "    Repeat LABEL " + split_line[1] + " " + \
            split_line[2] + " times max")

        if symbols["repeats"][idx] > 0:
            print("[" + lib + "] " + coords[0] + "        " + str(symbols["repeats"][idx]) + " repeats left.")
            symbols["repeats"][idx] -= 1
            return symbols["labels"][split_line[1]]
        else:
            print("[" + lib + "] " + coords[0] + "        No repeats left, not repeating.")
            symbols["repeats"][idx] = symbols["original"][idx] # makes this behave like a normal loop
        return idx+1


scripts.add_command(Control_Repeat())  # register the command


# ##################################################
# ### CLASS Control_If_Pressed_Repeat_Label      ###
# ##################################################

# class that defines the IF_PRESSED_REPEAT_LABEL command
class Control_If_Pressed_Repeat_Label(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("IF_PRESSED_REPEAT_LABEL")  # the name of the command as you have to enter it in the code

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
            if len(split_line) != 3:
                return ("'" + split_line[0] + "' needs both a label name and how many times to repeat.", line)

            try:
                temp = int(split_line[2])
                if temp < 1:
                    return (split_line[0] + " requires a minimum of 1 repeat.", line)
                else:
                    symbols["repeats"][idx] = int(split_line[2])
                    symbols["original"][idx] = int(split_line[2])
            except:
                return (split_line[0] + " number of repeats '" + split_line[2] + "' not valid.", line)

        if pass_no == 2:       # in Pass 2 we can check to make sure referenced symbols exist
            if split_line[1] not in symbols["labels"]:
                return ("Target not found for " + self.name, line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + lib + "] " + coords[0] + "    If key is pressed repeat label " + split_line[1] + " " + split_line[2] + " times max")

        if not split_line[1] in symbols["labels"]:          # The label should always exist
            print("missing LABEL '" + split_line[1] + "'")  # otherwise an error
            return -1
        else:
            if lp_events.pressed[coords[1]][coords[2]]:
                if symbols["repeats"][idx] > 0:
                    print("[" + lib + "] " + coords[0] + "        " + str(symbols["repeats"][idx]) + " repeats left.")
                    symbols["repeats"][idx] -= 1
                    return symbols["labels"][split_line[1]]
                else:
                    print("[" + lib + "] " + coords[0] + "        No repeats left, not repeating.")

        return idx+1


scripts.add_command(Control_If_Pressed_Repeat_Label())  # register the command


# ##################################################
# ### CLASS Control_If_Pressed_Repeat            ###
# ##################################################

# class that defines the IF_PRESSED command.  This operates more like a 
# traditional repeat/until by causing the code to repeat n times (rather than
# n+1, and it resets the counter at the end
class Control_If_Pressed_Repeat(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("IF_PRESSED_REPEAT")  # the name of the command as you have to enter it in the code

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
            if len(split_line) != 3:
                return ("'" + split_line[0] + "' needs both a label name and how many times to repeat.", line)

            try:
                temp = int(split_line[2])
                if temp < 1:
                    return (split_line[0] + " requires a minimum of 1 repeat.", line)
                else:
                    symbols["repeats"][idx] = int(split_line[2])-1
                    symbols["original"][idx] = int(split_line[2])-1
            except:
                return (split_line[0] + " number of repeats '" + split_line[2] + "' not valid.", line)

        if pass_no == 2:       # in Pass 2 we can check to make sure referenced symbols exist
            if split_line[1] not in symbols["labels"]:
                return ("Target not found for " + self.name, line)

            if symbols["labels"][split_line[1]] > idx:
                return ("Target for " + self.name + " must preceed the command.", line)


        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + lib + "] " + coords[0] + "    If key is pressed repeat " + split_line[1] + " " + split_line[2] + " times max")

        if not split_line[1] in symbols["labels"]:          # The label should always exist
            print("missing LABEL '" + split_line[1] + "'")  # otherwise an error
            return -1
        else:
            if lp_events.pressed[coords[1]][coords[2]]:
                if symbols["repeats"][idx] > 0:
                    print("[" + lib + "] " + coords[0] + "        " + str(symbols["repeats"][idx]) + " repeats left.")
                    symbols["repeats"][idx] -= 1
                    return symbols["labels"][split_line[1]]
                else:
                    print("[" + lib + "] " + coords[0] + "        No repeats left, not repeating.")
                    symbols["repeats"][idx] = symbols["original"][idx] # for a normal repeat statement

        return idx+1


scripts.add_command(Control_If_Pressed_Repeat())  # register the command


# ##################################################
# ### CLASS Control_If_Unpressed_Repeat_Label    ###
# ##################################################

# class that defines the IF_UNPRESSED_REPEAT_LABEL command.
class Control_If_Unpressed_Repeat_Label(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("IF_UNPRESSED_REPEAT_LABEL")  # the name of the command as you have to enter it in the code

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
            if len(split_line) != 3:
                return ("'" + split_line[0] + "' needs both a label name and how many times to repeat.", line)

            try:
                temp = int(split_line[2])
                if temp < 1:
                    return (split_line[0] + " requires a minimum of 1 repeat.", line)
                    symbols["repeats"][idx] = int(split_line[2])
                    symbols["original"][idx] = int(split_line[2])
            except:
               return (split_line[0] + " number of repeats '" + split_line[2] + "' not valid.", line)

        if pass_no == 2:       # in Pass 2 we can check to make sure referenced symbols exist
            if split_line[1] not in symbols["labels"]:
                return ("Target not found for " + self.name, line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + lib + "] " + coords[0] + "    If key is not pressed repeat label " + split_line[1] + " " + split_line[2] + " times max")

        if not split_line[1] in symbols["labels"]:          # The label should always exist
            print("missing LABEL '" + split_line[1] + "'")  # otherwise an error
            return -1
        else:
            if not lp_events.pressed[coords[1]][coords[2]]:
                if symbols["repeats"][idx] > 0:
                    print("[" + lib + "] " + coords[0] + "        " + str(symbols["repeats"][idx]) + " repeats left.")
                    symbols["repeats"][idx] -= 1
                    return symbols["labels"][split_line[1]]
                else:
                    print("[" + lib + "] " + coords[0] + "        No repeats left, not repeating.")

        return idx+1


scripts.add_command(Control_If_Unpressed_Repeat_Label())  # register the command


# ##################################################
# ### CLASS Control_If_Unpressed_Repeat          ###
# ##################################################

# class that defines the IF_UNPRESSED_REPEAT command.  This operates more like a 
# traditional repeat/until by causing the code to repeat n times (rather than
# n+1, and it resets the counter at the end
class Control_If_Unpressed_Repeat(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("IF_UNPRESSED_REPEAT")  # the name of the command as you have to enter it in the code

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
            if len(split_line) != 3:
                return ("'" + split_line[0] + "' needs both a label name and how many times to repeat.", line)

            try:
                temp = int(split_line[2])
                if temp < 1:
                    return (split_line[0] + " requires a minimum of 1 repeat.", line)
                    symbols["repeats"][idx] = int(split_line[2])-1
                    symbols["original"][idx] = int(split_line[2])-1
            except:
               return (split_line[0] + " number of repeats '" + split_line[2] + "' not valid.", line)

        if pass_no == 2:       # in Pass 2 we can check to make sure referenced symbols exist
            if split_line[1] not in symbols["labels"]:
                return ("Target not found for " + self.name, line)

            if symbols["labels"][split_line[1]] > idx:
                return ("Target for " + self.name + " must preceed the command.", line)


        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + lib + "] " + coords[0] + "    If key is not pressed repeat " + split_line[1] + " " + split_line[2] + " times max")

        if not split_line[1] in symbols["labels"]:          # The label should always exist
            print("missing LABEL '" + split_line[1] + "'")  # otherwise an error
            return -1
        else:
            if not lp_events.pressed[coords[1]][coords[2]]:
                if symbols["repeats"][idx] > 0:
                    print("[" + lib + "] " + coords[0] + "        " + str(symbols["repeats"][idx]) + " repeats left.")
                    symbols["repeats"][idx] -= 1
                    return symbols["labels"][split_line[1]]
                else:
                    print("[" + lib + "] " + coords[0] + "        No repeats left, not repeating.")
                    symbols["repeats"][idx] = symbols["original"][idx] # to behave more normal

        return idx+1


scripts.add_command(Control_If_Unpressed_Repeat())  # register the command


# ##################################################
# ### CLASS Control_Reset_Repeats                ###
# ##################################################

# class that defines the RESET_REPEATS command
class Control_Reset_Repeats(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("RESET_REPEATS")  # the name of the command as you have to enter it in the code

    def Validate(
        self,
        idx: int,              # The current line number
        line,                  # The current line
        lines,                 # The current script
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if len(split_line) > 1:
            return ("Too many arguments for command '" + split_line[0] + "'.", line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + lib + "] " + coords[0] + "    Reset all repeats")

        for i in symbols["repeats"]:
             symbols["repeats"][i] = symbols["original"][i]

        return idx+1


scripts.add_command(Control_Reset_Repeats())  # register the command


