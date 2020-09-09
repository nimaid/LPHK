import command_base, ms, scripts, variables
from command_base import R_INIT, R_GET, R_PRE_INFO, R_VALIDATE, R_INFO, R_RUN, R_FINAL

lib = "cmds_mous" # name of this library (for logging)

# ##################################################
# ### CLASS Mouse_Move                           ###
# ##################################################

# class that defines the M_MOVE command (wait while a button is pressed?)
class Mouse_Move(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("M_MOVE", lib, (   # the name of the command as you have to enter it in the code
            # Desc      Opt    Var   type       conv  p1_val p2_val
            ("X value", False, True, "integer", int,  None,  None), \
            ("Y value", False, True, "integer", int,  None,  None) ) )


    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        params = [idx, split_line, symbols, coords, is_async]
        try:
            if self.Partial_run(*params, [R_INIT, R_GET, R_VALIDATE]) == -1:
                return -1
                
            print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Relative mouse movement (" + str(self.param[1]) + ", " + str(self.param[2]) + ")")

            ms.move_to_pos(float(self.param[1]), float(self.param[2]))

            return idx+1
            
        finally:
            self.Partial_run(*params, [R_FINAL])


scripts.add_command(Mouse_Move())  # register the command


# ##################################################
# ### CLASS Mouse_Set                            ###
# ##################################################

# class that defines the M_SET command (put the mouse somewhere)
class Mouse_Set(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("M_SET", lib, (   # the name of the command as you have to enter it in the code
            # Desc      Opt    Var   type      conv  p1_val                      p2_val 
            ("X value", False, True, "integer", int, variables.Validate_ge_zero, None), \
            ("Y value", False, True, "integer", int, variables.Validate_ge_zero, None) ) )


    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        params = [idx, split_line, symbols, coords, is_async]
        try:
            if self.Partial_run(*params, [R_INIT, R_GET, R_VALIDATE]) == -1:
                return -1

            print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Set mouse position to (" + str(self.param[1]) + ", " + \
                str(self.param[2]) + ")")

            ms.set_pos(float(self.param[1]), float(self.param[2]))

            return idx+1
            
        finally:
            self.Partial_run(*params, [R_FINAL])


scripts.add_command(Mouse_Set())  # register the command


# ##################################################
# ### CLASS Mouse_Scroll                         ###
# ##################################################

# class that defines the M_SCROLL command (???)
class Mouse_Scroll(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("M_SCROLL", lib, (   # the name of the command as you have to enter it in the code
            lib,
            # Desc            Opt    Var   type      conv  p1_val p2_val 
            ("X value",       False, True, "integer", int, None,  None), \
            ("Scroll amount", False, True, "integer", int, None,  None) ) )


    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        params = [idx, split_line, symbols, coords, is_async]
        try:
            if self.Partial_run(*params, [R_INIT, R_GET, R_VALIDATE]) == -1:
                return -1

            if self.param[2]:
                print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Scroll (" + str(self.param[1]) + ", " + str(self.param[2]) + ")")
            else:
                print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Scroll " + str(self.param[1]))

            if v2:
                ms.scroll(float(self.param[2]), float(self.param[1]))
            else:
                ms.scroll(0, float(self.param[1]))

            return idx+1
            
        finally:
            self.Partial_run(*params, [R_FINAL])


scripts.add_command(Mouse_Scroll())  # register the command


# ##################################################
# ### CLASS Mouse_Line                           ###
# ##################################################

# class that defines the M_LINE command (draw a line?)
class Mouse_Line(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("M_LINE", lib, (   # the name of the command as you have to enter it in the code
            # Desc         Opt    Var   type      conv  p1_val                      p2_val 
            ("X1 value",   False, True, "integer", int, variables.Validate_ge_zero, None), \
            ("Y1 value",   False, True, "integer", int, variables.Validate_ge_zero, None), \
            ("X2 value",   False, True, "integer", int, variables.Validate_ge_zero, None), \
            ("Y2 value",   False, True, "integer", int, variables.Validate_ge_zero, None), \
            ("Wait value", True,  True, "integer", int, variables.Validate_ge_zero, None), \
            ("Skip value", True,  True, "integer", int, variables.Validate_gt_zero, None) ) )


    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        params = [idx, split_line, symbols, coords, is_async]
        try:
            if self.Partial_run(*params, [R_INIT, R_GET, R_VALIDATE]) == -1:
                return -1

            delay = None
            if self.param[5]:
                delay = float(self.param[5]) / 1000.0

            skip = 1
            if self.param[6]:
                skip = int(self.param[6])

            if (delay == None) or (delay <= 0):
                print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Mouse line from (" + \
                    str(self.param[1]) + ", " + str(self.param[2]) + ") to (" + \
                    str(self.param[3]) + ", " + str(self.param[4]) + ") by " + str(skip) + " pixels per step")
            else:
                print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Mouse line from (" + \
                    str(self.param[1]) + ", " + str(self.param[2]) + ") to (" + \
                    str(self.param[3]) + ", " + str(self,param[4]) + ") by " + \
                    str(skip) + " pixels per step and wait " + str(self.param[5]) + " milliseconds between each step")

            points = ms.line_coords(self.param[1], self.param[2], self.param[3], self.param[4])

            for x_M, y_M in points[::skip]:
                if check_kill(x, y, is_async):
                    return -1

                ms.set_pos(x_M, y_M)

                if (delay != None) and (delay > 0):
                    if not safe_sleep(delay, x, y, is_async):
                        return -1

            return idx+1
            
        finally:
            self.Partial_run(*params, [R_FINAL])


scripts.add_command(Mouse_Line())  # register the command


# ##################################################
# ### CLASS Mouse_Line_Move                      ###
# ##################################################

# class that defines the M_LINE_MOVE command
class Mouse_Line_Move(command_base.Command_Basic):
    def __init__(
        self,
         ):

        super().__init__("M_LINE_MOVE", lib, (   # the name of the command as you have to enter it in the code
            # Desc         Opt    Var   type      conv  p1_val                      p2_val 
            ("X value",    False, True, "integer", int, variables.Validate_ge_zero, None), \
            ("Y value",    False, True, "integer", int, variables.Validate_ge_zero, None), \
            ("Wait value", True,  True, "integer", int, variables.Validate_ge_zero, None), \
            ("Skip value", True,  True, "integer", int, variables.Validate_gt_zero, None) ) )


    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        params = [idx, split_line, symbols, coords, is_async]
        try:
            if self.Partial_run(*params, [R_INIT, R_GET, R_VALIDATE]) == -1:
                return -1

            delay = None
            if self.param[3]:
                delay = float(self.param[3]) / 1000.0

            skip = 1
            if self.param[4]:
                skip = int(self.param[4])

            if (delay == None) or (delay <= 0):
                print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Mouse line move relative (" + \
                    str(self.param[1]) + ", " + str(self.param[2]) + ") and wait " + str(self.param[3]) + " milliseconds between each step")
            else:
                print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Mouse line move relative (" + \
                    str(self.param[1]) + ", " + str(self.param[2]) + ") by " + str(self.param[4]) + \
                    " pixels per step and wait " + str(self.param[3]) + " milliseconds between each step")

            x_C, y_C = ms.get_pos()
            x_N, y_N = x_C + self.param[1], y_C + self.param[2]
            points = ms.line_coords(x_C, y_C, x_N, y_N)

            for x_M, y_M in points[::skip]:
                if check_kill(coords[1], coords[2], is_async):
                    return -1

                ms.set_pos(x_M, y_M)

                if (delay != None) and (delay > 0):
                    if not safe_sleep(delay, coords[1], coords[2], is_async):
                        return -1

            return idx+1
            
        finally:
            self.Partial_run(*params, [R_FINAL])


scripts.add_command(Mouse_Line_Move())  # register the command


# ##################################################
# ### CLASS Mouse_Line_Set                       ###
# ##################################################

# class that defines the M_LINE_SET command
class Mouse_Line_Set(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("M_LINE_SET", lib, (   # the name of the command as you have to enter it in the code
            # Desc         Opt    Var   type      conv  p1_val                      p2_val 
            ("X value",    False, True, "integer", int, variables.Validate_ge_zero, None), \
            ("Y value",    False, True, "integer", int, variables.Validate_ge_zero, None), \
            ("Wait value", True,  True, "integer", int, variables.Validate_ge_zero, None), \
            ("Skip value", True,  True, "integer", int, variables.Validate_gt_zero, None) ) )


    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        params = [idx, split_line, symbols, coords, is_async]
        try:
            if self.Partial_run(*params, [R_INIT, R_GET, R_VALIDATE]) == -1:
                return -1

            delay = None
            if self.params[3]:
                delay = float(self.params[3]) / 1000.0

            skip = 1
            if self.params[4]:
                skip = int(self.params[4])

            if (delay == None) or (delay <= 0):
                print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Mouse line set (" + \
                    self.params[1] + ", " + self.params[2] + ") by " + str(skip) + \
                    " pixels per step")
            else:
                print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Mouse line set (" + \
                self.params[1] + ", " + self.params[2] + ") by " + str(skip) + \
                " pixels per step and wait " + self.params[3] + " milliseconds between each step")

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
            
        finally:
            self.Partial_run(*params, [R_FINAL])


scripts.add_command(Mouse_Line_Set())  # register the command


# ##################################################
# ### CLASS Mouse_Recall_Line                    ###
# ##################################################

# class that defines the M_RECALL_LINE command
class Mouse_Recall_Line(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("M_RECALL_LINE", lib, (   # the name of the command as you have to enter it in the code
            # Desc         Opt    Var   type      conv  p1_val                      p2_val 
            ("Wait value", True , True, "integer", int, variables.Validate_ge_zero, None), \
            ("Skip value", True,  True, "integer", int, variables.Validate_gt_zero, None) ) )


    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        params = [idx, split_line, symbols, coords, is_async]
        try:
            if self.Partial_run(*params, [R_INIT, R_GET, R_VALIDATE]) == -1:
                return -1

            x1, y1 = symbols['m_pos']

            delay = 0
            if self.params[3]:
                delay = float(self.params[3]) / 1000.0

            skip = 1
            if self.params[4]:
                skip = int(self.params[4])

            if (delay == None) or (delay <= 0):
                print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Recall mouse position " + str(symbols["m_pos"]) + \
                    " in a line by " + str(skip) + " pixels per step")
            else:
                print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Recall mouse position " + str(symbols["m_pos"]) + \
                    " in a line by " + str(skip) + " pixels per step and wait " + \
                    str(delay) + " milliseconds between each step")

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
            
        finally:
            self.Partial_run(*params, [R_FINAL])


scripts.add_command(Mouse_Recall_Line())  # register the command


# ##################################################
# ### CLASS Mouse_Store                          ###
# ##################################################

# class that defines the M_STORE command
class Mouse_Store(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("M_STORE", lib, () )  # the name of the command as you have to enter it in the code

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        params = [idx, split_line, symbols, coords, is_async]
        try:
            if self.Partial_run(*params, [R_INIT, R_GET, R_VALIDATE]) == -1:
                return -1

            print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Store mouse position")

            symbols["m_pos"] = ms.get_pos()  # Another example of modifying the symbol table during execution.

            return idx+1
            
        finally:
            self.Partial_run(*params, [R_FINAL])


scripts.add_command(Mouse_Store())  # register the command


# ##################################################
# ### CLASS Mouse_Recall                         ###
# ##################################################

# class that defines the M_RECALL command
class Mouse_Recall(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("M_RECALL", lib, () ) # the name of the command as you have to enter it in the code


    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        params = [idx, split_line, symbols, coords, is_async]
        try:
            if self.Partial_run(*params, [R_INIT, R_GET, R_VALIDATE]) == -1:
                return -1

            if symbols['m_pos'] == tuple():
                print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    No 'M_STORE' command has been run, cannot do 'M_RECALL'")
            else:
                print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Recall mouse position " + str(symbols['m_pos']))
                ms.set_pos(symbols['m_pos'][0], symbols['m_pos'][1])

            return idx+1
            
        finally:
            self.Partial_run(*params, [R_FINAL])


scripts.add_command(Mouse_Recall())  # register the command
