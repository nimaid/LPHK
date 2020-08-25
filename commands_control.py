import command_base, lp_events, scripts


# ##################################################
# ### CLASS Control_Comment                      ###
# ##################################################

# class that defines the comment command (single quote at beginning of line)
# this is special because it has some different handling in the main sode
# to allow it to work without a space following it
class Control_Comment(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("-")

    def Validate(
        self,
        idx: int,
        line,
        lines,
        split_line,
        symbols,
        pass_no
        ):

        return True  # never return an error

    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        print("[cmds_ctrl] " + coords[0] + "    comment: " + split_line[1])

        return idx+1


scripts.add_command(Control_Comment())


# ##################################################
# ### CLASS Control_Label                        ###
# ##################################################

# class that defines the LABEL command (a target of GOTO's etc)
class Control_Label(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("LABEL")

    def Validate(
        self,
        idx: int,
        line,
        lines,
        split_line,
        symbols,
        pass_no
        ):

        if pass_no == 1:
            # check number of split_line
            if len(split_line) != 2:
                return ("Wrong number of parameters in " + self.Name, line)

            # check for duplicate label
            if split_line[1] in symbols["labels"]:
                return ("duplicate LABEL", line)

            # add label to symbol table
            symbols["labels"][split_line[1]] = idx

        return True

    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        print("[cmds_ctrl] " + coords[0] + "    Label: " + split_line[1])

        return idx+1


scripts.add_command(Control_Label())


# ##################################################
# ### CLASS Control_Goto_Label                   ###
# ##################################################

# class that defines the GOTO_LABEL command
class Control_Goto_Label(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("GOTO_LABEL")

    def Validate(
        self,
        idx: int,
        line,
        lines,
        split_line,
        symbols,
        pass_no
        ):

        if pass_no == 1:
            # check number of split_line
            if len(split_line) != 2:
                return ("Wrong number of parameters in " + self.Name, line)

        if pass_no == 2:
            if split_line[1] not in symbols["labels"]:
                return ("Target not found for " + self.Name, line)

        return True

    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        # check for label
        if split_line[1] in symbols["labels"]:
            return symbols["labels"][split_line[1]]
        else:
            print("missing LABEL '" + split_line[1] + "'")
            return -1

        return idx+1


scripts.add_command(Control_Goto_Label())


# ##################################################
# ### CLASS Control_If_Pressed_Goto_Label        ###
# ##################################################

# class that defines the IF_PRESSED_GOTO_LABEL command
class Control_If_Pressed_Goto_Label(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("IF_PRESSED_GOTO_LABEL")

    def Validate(
        self,
        idx: int,
        line,
        lines,
        split_line,
        symbols,
        pass_no
        ):

        if pass_no == 1:
            if len(split_line) != 2:
                return ("'" + split_line[0] + "' takes exactly 1 argument.", line)

        if pass_no == 2:
            if split_line[1] not in symbols["labels"]:
                return ("Target not found for " + self.Name, line)

        return True

    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        print("[cmds_ctrl] " + coords[0] + "    If key is pressed goto LABEL " + split_line[1])
        if lp_events.pressed[coords[1]][coords[2]]:
            return symbols["labels"][split_line[1]]

        return idx+1


scripts.add_command(Control_If_Pressed_Goto_Label())


# ##################################################
# ### CLASS Control_If_Unpressed_Goto_Label      ###
# ##################################################

# class that defines the IF_UNPRESSED_GOTO_LABEL command
class Control_If_Unpressed_Goto_Label(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("IF_UNPRESSED_GOTO_LABEL")

    def Validate(
        self,
        idx: int,
        line,
        lines,
        split_line,
        symbols,
        pass_no
        ):

        if pass_no == 1:
            if len(split_line) != 2:
               return ("'" + split_line[0] + "' takes exactly 1 argument.", line)

        if pass_no == 2:
            if split_line[1] not in symbols["labels"]:
                return ("Target not found for " + self.Name, line)

        return True

    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        print("[cmds_ctrl] " + coords[0] + "    If key is not pressed goto LABEL " + split_line[1])
        if not lp_events.pressed[coords[1]][coords[2]]:
            return symbols["labels"][split_line[1]]

        return idx+1


scripts.add_command(Control_If_Unpressed_Goto_Label())


# ##################################################
# ### CLASS Control_Repeat_Label                 ###
# ##################################################

# class that defines the REPEAT_LABEL command
class Control_Repeat_Label(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("REPEAT_LABEL")

    def Validate(
        self,
        idx: int,
        line,
        lines,
        split_line,
        symbols,
        pass_no
        ):

        if pass_no == 1:
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

        if pass_no == 2:
            if split_line[1] not in symbols["labels"]:
                return ("Target not found for " + self.Name, line)

        return True

    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        print("[cmds_ctrl] " + coords[0] + "    Repeat LABEL " + split_line[1] + " " + \
            split_line[2] + " times max")

        if symbols["repeats"][idx] > 0:
            print("[cmds_ctrl] " + coords[0] + "        " + str(symbols["repeats"][idx]) + " repeats left.")
            symbols["repeats"][idx] -= 1
            return symbols["labels"][split_line[1]]
        else:
            print("[cmds_ctrl] " + coords[0] + "        No repeats left, not repeating.")

        return idx+1


scripts.add_command(Control_Repeat_Label())


# ##################################################
# ### CLASS Control_If_Pressed_Repeat_Label      ###
# ##################################################

# class that defines the IF_PRESSED_REPEAT_LABEL command
class Control_If_Pressed_Repeat_Label(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("IF_PRESSED_REPEAT_LABEL")

    def Validate(
        self,
        idx: int,
        line,
        lines,
        split_line,
        symbols,
        pass_no
        ):

        if pass_no == 1:
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

        if pass_no == 2:
            if split_line[1] not in symbols["labels"]:
                return ("Target not found for " + self.Name, line)

        return True

    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        print("[cmds_ctrl] " + coords[0] + "    If key is pressed repeat label " + split_line[1] + " " + split_line[2] + " times max")

        if lp_events.pressed[coords[1]][coords[2]]:
            if symbols["repeats"][idx] > 0:
                print("[cmds_ctrl] " + coords[0] + "        " + str(symbols["repeats"][idx]) + " repeats left.")
                symbols["repeats"][idx] -= 1
                return symbols["labels"][split_line[1]]
            else:
                print("[cmds_ctrl] " + coords[0] + "        No repeats left, not repeating.")

        return idx+1


scripts.add_command(Control_If_Pressed_Repeat_Label())


# ##################################################
# ### CLASS Control_If_Unpressed_Repeat_Label    ###
# ##################################################

# class that defines the IF_UNPRESSED_REPEAT_LABEL command.
class Control_If_Unpressed_Repeat_Label(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("IF_UNPRESSED_REPEAT_LABEL")

    def Validate(
        self,
        idx: int,
        line,
        lines,
        split_line,
        symbols,
        pass_no
        ):

        if pass_no == 1:
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

        if pass_no == 2:
            if split_line[1] not in symbols["labels"]:
                return ("Target not found for " + self.Name, line)

        return True

    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        print("[cmds_ctrl] " + coords[0] + "    If key is not pressed repeat label " + split_line[1] + " " + split_line[2] + " times max")

        if not lp_events.pressed[coords[1]][coords[2]]:
            if symbols["repeats"][idx] > 0:
                print("[cmds_ctrl] " + coords[0] + "        " + str(symbols["repeats"][idx]) + " repeats left.")
                symbols["repeats"][idx] -= 1
                return symbols["labels"][split_line[1]]
            else:
                print("[cmds_ctrl] " + coords[0] + "        No repeats left, not repeating.")

        return idx+1


scripts.add_command(Control_If_Unpressed_Repeat_Label())


# ##################################################
# ### CLASS Control_Reset_Repeats                ###
# ##################################################

# class that defines the RESET_REPEATS command
class Control_Reset_Repeats(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("RESET_REPEATS")

    def Validate(
        self,
        idx: int,
        line,
        lines,
        split_line,
        symbols,
        pass_no
        ):

        if len(split_line) > 1:
            return ("Too many arguments for command '" + split_line[0] + "'.", line)

        return True

    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        print("[cmds_ctrl] " + coords[0] + "    Reset all repeats")

        for i in symbols["repeats"]:
             symbols["repeats"][i] = symbols["original"][i]

        return idx+1


scripts.add_command(Control_Reset_Repeats())


