import command_base, ms, scripts, variables

lib = "cmds_mous" # name of this library (for logging)

# ##################################################
# ### CLASS Mouse_Move                           ###
# ##################################################

# class that defines the M_MOVE command (wait while a button is pressed?)
class Mouse_Move(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("M_MOVE")  # the name of the command as you have to enter it in the code

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
            ret = variables.check_num(split_line, [2], idx, line, self.name)
            if ret != True:
                return ret

            ret = variables.check_param(split_line, 1, "X value", idx, self.name, line, True)
            if ret != True:
                return ret

            ret = variables.check_param(split_line, 2, "Y value", idx, self.name, line, True)
            if ret != True:
                return ret

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        v1 = variables.get_value(1, symbols)
        v2 = variables.get_value(2, symbols)
                        
        print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Relative mouse movement (" + str(v1) + ", " + \
            str(v2) + ")")

        ms.move_to_pos(float(v1), float(v2))

        return idx+1


scripts.add_command(Mouse_Move())  # register the command


# ##################################################
# ### CLASS Mouse_Set                            ###
# ##################################################

# class that defines the M_SET command (put the mouse somewhere)
class Mouse_Set(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("M_SET")  # the name of the command as you have to enter it in the code

    def Validate(
        self,
        idx: int,              # The current line number
        line,                  # The current line
        lines,                 # The current script
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        # no longer allow just 2 tokens

        if pass_no == 1:       # in Pass 1 we can do general syntax check and gather symbol definitions
            if len(split_line) < 3:
                return ("Line:" + str(idx+1) + " - Too few arguments for command '" + split_line[0] + "'.", line)

            if len(split_line) > 3:
                return ("Line:" + str(idx+1) + " - Too many arguments for command '" + split_line[0] + "'.", line)

            try:
                temp = int(split_line[1])
            except:
                if not variables.valid_var_name(split_line[1]):   # a variable is OK here
                    return ("Line:" + str(idx+1) + " - '" + self.name + "' X value '" + split_line[1] + "' not valid.", line)

            try:
                temp = int(split_line[2])
            except:
                if not variables.valid_var_name(split_line[2]):   # a variable is OK here
                    return ("Line:" + str(idx+1) + " - '" + self.name + "' Y value '" + split_line[2] + "' not valid.", line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        v1 = split_line[1]
        if variables.valid_var_name(v1):
            with symbols['g_vars'][0]:                                # lock the globals while we do this
                v1 = variables.get(v1, symbols['l_vars'], symbols['g_vars'][1])
            
        v2 = split_line[2]
        if variables.valid_var_name(v2):
            with symbols['g_vars'][0]:                                # lock the globals while we do this
                v1 = variables.get(v2, symbols['l_vars'], symbols['g_vars'][1])
             
        print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Set mouse position to (" + str(v1) + ", " + \
            str(v2) + ")")

        ms.set_pos(float(v1), float(v2))

        return idx+1


scripts.add_command(Mouse_Set())  # register the command


# ##################################################
# ### CLASS Mouse_Scroll                         ###
# ##################################################

# class that defines the M_SCROLL command (???)
class Mouse_Scroll(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("M_SCROLL")  # the name of the command as you have to enter it in the code

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
            if len(split_line) < 2:
                return ("Line:" + str(idx+1) + " - Too few arguments for command '" + split_line[0] + "'.", line)

            if len(split_line) > 3:
                return ("Line:" + str(idx+1) + " - Too many arguments for command '" + split_line[0] + "'.", line)

            try:
                temp = int(split_line[1])
            except:
                if not variables.valid_var_name(split_line[1]):   # a variable is OK here
                    return ("Line:" + str(idx+1) + " - '" + self.name + "' X value '" + split_line[1] + "' not valid.", line)

            if len(split_line) > 2:
                try:
                    temp = float(split_line[2])
                except:
                    if not variables.valid_var_name(split_line[2]):   # a variable is OK here
                        return ("Line:" + str(idx+1) + " - Invalid scroll amount '" + split_line[2] + "'.", line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        if len(split_line) > 2:
            print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Scroll (" + split_line[1] + ", " + split_line[2] + ")")
            ms.scroll(float(split_line[2]), float(split_line[1]))
        else:
            print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Scroll " + split_line[1])
            ms.scroll(0, float(split_line[1]))

        return idx+1


scripts.add_command(Mouse_Scroll())  # register the command


# ##################################################
# ### CLASS Mouse_Line                           ###
# ##################################################

# class that defines the M_LINE command (draw a line?)
class Mouse_Line(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("M_LINE")  # the name of the command as you have to enter it in the code

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
            if len(split_line) < 5:
                return ("Line:" + str(idx+1) + " - Too few arguments for command '" + split_line[0] + "'.", line)

            if len(split_line) > 7:
                return ("Line:" + str(idx+1) + " - Too many arguments for command '" + split_line[0] + "'.", line)

            try:
                temp = int(split_line[1])
            except:
                if not variables.valid_var_name(split_line[1]):   # a variable is OK here
                    return ("Line:" + str(idx+1) + " - '" + self.name + "' X1 value '" + split_line[1] + "' not valid.", line)

            try:
                temp = int(split_line[2])
            except:
                if not variables.valid_var_name(split_line[2]):   # a variable is OK here
                    return ("Line:" + str(idx+1) + " - '" + self.name + "' Y1 value '" + split_line[2] + "' not valid.", line)

            try:
                temp = int(split_line[3])
            except:
                if not variables.valid_var_name(split_line[3]):   # a variable is OK here
                    return ("Line:" + str(idx+1) + " - '" + self.name + "' X2 value '" + split_line[3] + "' not valid.", line)

            try:
                temp = int(split_line[4])
            except:
                if not variables.valid_var_name(split_line[4]):   # a variable is OK here
                    return ("Line:" + str(idx+1) + " - '" + self.name + "' Y2 value '" + split_line[4] + "' not valid.", line)

            if len(split_line) >= 6:
                try:
                    temp = float(split_line[5])
                except:
                    if not variables.valid_var_name(split_line[5]):   # a variable is OK here
                        return ("Line:" + str(idx+1) + " - '" + self.name + "' wait value '" + split_line[5] + "' not valid.", line)

            if len(split_line) >= 7:
                try:
                    temp = int(split_line[6])
                    if temp == 0:
                        return ("Line:" + str(idx+1) + " - '" + self.name + "' skip value cannot be zero.", line)
                except:
                    if not variables.valid_var_name(split_line[6]):   # a variable is OK here
                        return ("Line:" + str(idx+1) + " - '" + self.name + "' skip value '" + split_line[6] + "' not valid.", line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        x1 = int(split_line[1])
        y1 = int(split_line[2])
        x2 = int(split_line[3])
        y2 = int(split_line[4])

        delay = None
        if len(split_line) > 5:
            delay = float(split_line[5]) / 1000.0

        skip = 1
        if len(split_line) > 6:
            skip = int(split_line[6])

        if (delay == None) or (delay <= 0):
            print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Mouse line from (" + \
                split_line[1] + ", " + split_line[2] + ") to (" + \
                split_line[3] + ", " + split_line[4] + ") by " + str(skip) + " pixels per step")
        else:
            print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Mouse line from (" + \
                split_line[1] + ", " + split_line[2] + ") to (" + \
                split_line[3] + ", " + split_line[4] + ") by " + \
                str(skip) + " pixels per step and wait " + split_line[5] + " milliseconds between each step")

        points = ms.line_coords(x1, y1, x2, y2)

        for x_M, y_M in points[::skip]:
            if check_kill(x, y, is_async):
                return -1

            ms.set_pos(x_M, y_M)

            if (delay != None) and (delay > 0):
                if not safe_sleep(delay, x, y, is_async):
                    return -1

        return idx+1


scripts.add_command(Mouse_Line())  # register the command


# ##################################################
# ### CLASS Mouse_Line_Move                      ###
# ##################################################

# class that defines the M_LINE_MOVE command 
class Mouse_Line_Move(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("M_LINE_MOVE")  # the name of the command as you have to enter it in the code

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
            if len(split_line) < 3:
                return ("Line:" + str(idx+1) + " - '" + split_line[0] + "' requires at least X and Y arguments.", line)

            try:
                temp = int(split_line[1])
            except:
                if not variables.valid_var_name(split_line[1]):   # a variable is OK here
                    return ("Line:" + str(idx+1) + " - '" + split_line[0] + "' X value '" + split_line[1] + "' not valid.", line)

            try:
                temp = int(split_line[2])
            except:
                if not variables.valid_var_name(split_line[2]):   # a variable is OK here
                    return ("Line:" + str(idx+1) + " - '" + split_line[0] + "' Y value '" + split_line[2] + "' not valid.", line)

            if len(split_line) >= 4:
                try:
                    temp = float(split_line[3])
                except:
                    if not variables.valid_var_name(split_line[3]):   # a variable is OK here
                        return ("Line:" + str(idx+1) + " - '" + split_line[0] + "' wait value '" + split_line[3] + "' not valid.", line)

            if len(split_line) >= 5:
                try:
                    temp = int(split_line[4])
                    if temp == 0:
                        return ("Line:" + str(idx+1) + " - '" + split_line[0] + "' skip value cannot be zero.", line)
                except:
                    if not variables.valid_var_name(split_line[4]):   # a variable is OK here
                        return ("Line:" + str(idx+1) + " - '" + split_line[0] + "' skip value '" + split_line[4] + "' not valid.", line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        x1 = int(split_line[1])
        y1 = int(split_line[2])

        delay = None
        if len(split_line) > 3:
            delay = float(split_line[3]) / 1000.0

        skip = 1
        if len(split_line) > 4:
            skip = int(split_line[4])

        if (delay == None) or (delay <= 0):
            print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Mouse line move relative (" + \
                split_line[1] + ", " + split_line[2] + ") by " + str(skip) + \
                " pixels per step")
        else:
            print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Mouse line move relative (" + \
                split_line[1] + ", " + split_line[2] + ") by " + str(skip) + \
                " pixels per step and wait " + split_line[3] + " milliseconds between each step")

        x_C, y_C = ms.get_pos()
        x_N, y_N = x_C + x1, y_C + y1
        points = ms.line_coords(x_C, y_C, x_N, y_N)

        for x_M, y_M in points[::skip]:
            if check_kill(coords[1], coords[2], is_async):
                return -1

            ms.set_pos(x_M, y_M)

            if (delay != None) and (delay > 0):
                if not safe_sleep(delay, coords[1], coords[2], is_async):
                    return -1

        return idx+1


scripts.add_command(Mouse_Line_Move())  # register the command


# ##################################################
# ### CLASS Mouse_Line_Set                       ###
# ##################################################

# class that defines the M_LINE_SET command 
class Mouse_Line_Set(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("M_LINE_SET")  # the name of the command as you have to enter it in the code

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
            if len(split_line) < 3:
                return ("Line:" + str(idx+1) + " - '" + split_line[0] + "' requires at least X and Y arguments.", line)

            try:
                temp = int(split_line[1])
            except:
                if not variables.valid_var_name(split_line[1]):   # a variable is OK here
                    return ("Line:" + str(idx+1) + " - '" + split_line[0] + "' X value '" + split_line[1] + "' not valid.", line)

            try:
                temp = int(split_line[2])
            except:
                if not variables.valid_var_name(split_line[2]):   # a variable is OK here
                    return ("Line:" + str(idx+1) + " - '" + split_line[0] + "' Y value '" + split_line[2] + "' not valid.", line)

            if len(split_line) >= 4:
                try:
                     temp = float(split_line[3])
                except:
                    if not variables.valid_var_name(split_line[3]):   # a variable is OK here
                        return ("Line:" + str(idx+1) + " - '" + split_line[0] + "' wait value '" + split_line[3] + "' not valid.", line)

            if len(split_line) >= 5:
                try:
                    temp = int(split_line[4])
                    if temp == 0:
                        return ("Line:" + str(idx+1) + " - '" + split_line[0] + "' skip value cannot be zero.", line)
                except:
                    if not variables.valid_var_name(split_line[4]):   # a variable is OK here
                        return ("Line:" + str(idx+1) + " - '" + split_line[0] + "' skip value '" + split_line[4] + "' not valid.", line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        x1 = int(split_line[1])
        y1 = int(split_line[2])

        delay = None
        if len(split_line) > 3:
            delay = float(split_line[3]) / 1000.0

        skip = 1
        if len(split_line) > 4:
            skip = int(split_line[4])

        if (delay == None) or (delay <= 0):
            print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Mouse line set (" + \
                split_line[1] + ", " + split_line[2] + ") by " + str(skip) + \
                " pixels per step")
        else:
            print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Mouse line set (" + \
            split_line[1] + ", " + split_line[2] + ") by " + str(skip) + \
            " pixels per step and wait " + split_line[3] + " milliseconds between each step")

        x_C, y_C = ms.get_pos()
        points = ms.line_coords(x_C, y_C, x1, y1)

        for x_M, y_M in points[::skip]:
            if check_kill(coords[1], coords[2], is_async):
                return -1
            ms.set_pos(x_M, y_M)
            if (delay != None) and (delay > 0):
                if not safe_sleep(delay, coords[1], coords[2], is_async):
                    return -1

        return idx+1


scripts.add_command(Mouse_Line_Set())  # register the command


# ##################################################
# ### CLASS Mouse_Recall_Line                    ###
# ##################################################

# class that defines the M_RECALL_LINE command 
class Mouse_Recall_Line(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("M_RECALL_LINE")  # the name of the command as you have to enter it in the code

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
            if len(split_line) > 1:
                try:
                    temp = float(split_line[1])
                except:
                    if not variables.valid_var_name(split_line[1]):   # a variable is OK here
                        return ("Line:" + str(idx+1) + " - '" + split_line[0] + "' wait value '" + split_line[1] + "' not valid.", line)

            if len(split_line) > 2:
                try:
                    temp = int(split_line[2])
                    if temp == 0:
                        return ("Line:" + str(idx+1) + " - '" + split_line[0] + "' skip value cannot be zero.", line)
                except:
                    if not variables.valid_var_name(split_line[2]):   # a variable is OK here
                        return ("Line:" + str(idx+1) + " - '" + split_line[0] + "' skip value '" + split_line[2] + "' not valid.", line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        x1, y1 = symbols['m_pos']

        delay = None
        if len(split_line) > 1:
            delay = float(split_line[1]) / 1000.0

        skip = 1
        if len(split_line) > 2:
            skip = int(split_line[2])

        if (delay == None) or (delay <= 0):
            print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Recall mouse position " + str(symbols["m_pos"]) + \
                " in a line by " + str(skip) + " pixels per step")
        else:
            print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Recall mouse position " + str(symbols["m_pos"]) + \
                " in a line by " + str(skip) + " pixels per step and wait " + \
                split_line[1] + " milliseconds between each step")

        x_C, y_C = ms.get_pos()
        points = ms.line_coords(x_C, y_C, x1, y1)

        for x_M, y_M in points[::skip]:
            if check_kill(coords[1], coords[2], is_async):
                return -1

            ms.set_pos(x_M, y_M)

            if (delay != None) and (delay > 0):
                if not safe_sleep(delay, coords[1], coords[2], is_async):
                    return -1

        return idx+1


scripts.add_command(Mouse_Recall_Line())  # register the command


# ##################################################
# ### CLASS Mouse_Store                          ###
# ##################################################

# class that defines the M_STORE command 
class Mouse_Store(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("M_STORE")  # the name of the command as you have to enter it in the code

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
            if len(split_line) > 1:
                return ("Line:" + str(idx+1) + " - '" + split_line[0] + "' takes no arguments.", line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Store mouse position")

        symbols["m_pos"] = ms.get_pos()  # Another example of modifying the symbol table during execution.

        return idx+1


scripts.add_command(Mouse_Store())  # register the command


# ##################################################
# ### CLASS Mouse_Recall                         ###
# ##################################################

# class that defines the M_RECALL command 
class Mouse_Recall(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("M_RECALL")  # the name of the command as you have to enter it in the code

    def Validate(
        self,
        idx: int,
        line,
        lines,
        split_line,
        symbols,
        pass_no
        ):

        if pass_no == 1:       # in Pass 1 we can do general syntax check and gather symbol definitions
            if len(split_line) > 1:
                return ("Line:" + str(idx+1) + " - '" + split_line[0] + "' takes no arguments.", line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        if symbols['m_pos'] == tuple():
            print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    No 'M_STORE' command has been run, cannot do 'M_RECALL'")
        else:
            print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Recall mouse position " + str(symbols['m_pos']))
            ms.set_pos(symbols['m_pos'][0], symbols['m_pos'][1])

        return idx+1


scripts.add_command(Mouse_Recall())  # register the command


