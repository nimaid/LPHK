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

            ret = variables.check_int_param(split_line, 1, "X value", idx, self.name, line, variables.validate_int_ge_zero)
            if ret != True:
                return (ret, line)

            ret = variables.check_int_param(split_line, 2, "Y value", idx, self.name, line, variables.validate_int_ge_zero)
            if ret != True:
                return (ret, line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        ok = True    
        p = len(split_line) - 1

        v1 = variables.get_value(split_line[1], symbols)
        if v1:
            v1 = int(v1)

        v2 = variables.get_value(split_line[2], symbols)
        if v2:
            v2 = int(v2)
                        
        print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Relative mouse movement (" + str(v1) + ", " + \
            str(v2) + ")")
         
        ret = variables.validate_int_ge_zero(v1, idx, self.name, "X value", 1, split_line[1])
        if ret != True:
            print("[" + lib + "] " + coords[0] + "  " + ret)
            ok = False

        ret = variables.validate_int_ge_zero(v2, idx, self.name, "Y value", 2, split_line[2])
        if ret != True:
            print("[" + lib + "] " + coords[0] + "  " + ret)
            ok = False

        if not ok:
            return -1
            
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

        if pass_no == 1:       # in Pass 1 we can do general syntax check and gather symbol definitions
            ret = variables.check_num(split_line, [2], idx, line, self.name)
            if ret != True:
                return ret

            ret = variables.check_int_param(split_line, 1, "X value", idx, self.name, line, variables.validate_int_ge_zero)
            if ret != True:
                return (ret, line)

            ret = variables.check_int_param(split_line, 2, "Y value", idx, self.name, line, variables.validate_int_ge_zero)
            if ret != True:
                return (ret, line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        ok = True    
        p = len(split_line) - 1

        v1 = variables.get_value(split_line[1], symbols)
        if v1:
            v1 = int(v1)

        v2 = variables.get_value(split_line[2], symbols)
        if v2:
            v2 = int(v2)
             
        print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Set mouse position to (" + str(v1) + ", " + \
            str(v2) + ")")

        ret = variables.validate_int_ge_zero(v1, idx, self.name, "X value", 1, split_line[1])
        if ret != True:
            print("[" + lib + "] " + coords[0] + "  " + ret)
            ok = False

        ret = variables.validate_int_ge_zero(v2, idx, self.name, "Y value", 2, split_line[2])
        if ret != True:
            print("[" + lib + "] " + coords[0] + "  " + ret)
            ok = False

        if not ok:
            return -1
            
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
            ret = variables.check_num(split_line, [1, 2], idx, line, self.name)
            if ret != True:
                return ret

            ret = variables.check_int_param(split_line, 1, "X value", idx, self.name, line, variables.validate_int_ge_zero)
            if ret != True:
                return (ret, line)

            ret = variables.check_int_param(split_line, 2, "Scroll amount", idx, self.name, line, variables.validate_int_ge_zero, True)
            if ret != True:
                return (ret, line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        ok = True    
        p = len(split_line) - 1

        v1 = variables.get_value(split_line[1], symbols)
        if v1:
            v1 = int(v1)
            
        if p > 1:
            v2 = variables.get_value(split_line[2], symbols)
            if v2:
                v2 = int(v2)
        else:
            v2 = None
            
        if v2:
            print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Scroll (" + str(v1) + ", " + str(v2) + ")")
        else:
            print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Scroll " + str(v1))

        ret = variables.validate_int_ge_zero(v1, idx, self.name, "X amount", 1, split_line[1])
        if ret != True:
            print("[" + lib + "] " + coords[0] + "  " + ret)
            ok = False

        if v2:
            ret = variables.validate_int_ge_zero(v2, idx, self.name, "Scroll amount", 2, split_line[2])
            if ret != True:
                print("[" + lib + "] " + coords[0] + "  " + ret)
                ok = False

        if not ok:
            return -1
            
        if v2:
            ms.scroll(float(v2), float(v1))
        else:
            ms.scroll(0, float(v1))

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
            ret = variables.check_num(split_line, [4, 5, 6], idx, line, self.name)
            if ret != True:
                return ret

            ret = variables.check_int_param(split_line, 1, "X1 value", idx, self.name, line, variables.validate_int_ge_zero)
            if ret != True:
                return (ret, line)

            ret = variables.check_int_param(split_line, 2, "Y1 value", idx, self.name, line, variables.validate_int_ge_zero)
            if ret != True:
                return (ret, line)

            ret = variables.check_int_param(split_line, 3, "X2 value", idx, self.name, line, variables.validate_int_ge_zero)
            if ret != True:
                return (ret, line)

            ret = variables.check_int_param(split_line, 4, "Y2 value", idx, self.name, line, variables.validate_int_ge_zero)
            if ret != True:
                return (ret, line)

            ret = variables.check_int_param(split_line, 5, "Wait value", idx, self.name, line, variables.validate_int_ge_zero, True)
            if ret != True:
                return (ret, line)

            ret = variables.check_int_param(split_line, 6, "Skip value", idx, self.name, line, variables.validate_int_gt_zero, True)
            if ret != True:
                return (ret, line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        ok = True 
        p = len(split_line) - 1

        v1 = variables.get_value(split_line[1], symbols)
        if v1:
            v1 = int(v1)
            
        v2 = variables.get_value(split_line[2], symbols)
        if v2:
            v2 = int(v2)

        v3 = variables.get_value(split_line[3], symbols)
        if v3:
            v3 = int(v3)

        v4 = variables.get_value(split_line[4], symbols)
        if v4:
            v4 = int(v4)

        if p > 4:
            v5 = variables.get_value(split_line[5], symbols)
            if v5:
                v5 = int(v5)
        else:
            v5 = None

        if p > 5:
            v6 = variables.get_value(split_line[6], symbols)
            if v6:
                v6 = int(v6)
        else:
            v6 = None

        delay = None
        if v5:
            delay = float(v5) / 1000.0

        skip = 1
        if v6:
            skip = int(v6)

        if (delay == None) or (delay <= 0):
            print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Mouse line from (" + \
                str(v1) + ", " + str(v2) + ") to (" + \
                str(v3) + ", " + str(v4) + ") by " + str(skip) + " pixels per step")
        else:
            print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Mouse line from (" + \
                str(v1) + ", " + str(v2) + ") to (" + \
                str(v3) + ", " + str(v4) + ") by " + \
                str(skip) + " pixels per step and wait " + str(v6) + " milliseconds between each step")

        ret = variables.validate_int_ge_zero(v1, idx, self.name, "X1 value", 1, split_line[1])
        if ret != True:
            print("[" + lib + "] " + coords[0] + "  " + ret)
            ok = False

        ret = variables.validate_int_ge_zero(v2, idx, self.name, "Y1 value", 2, split_line[2])
        if ret != True:
            print("[" + lib + "] " + coords[0] + "  " + ret)
            ok = False

        ret = variables.validate_int_ge_zero(v3, idx, self.name, "X2 value", 3, split_line[3])
        if ret != True:
            print("[" + lib + "] " + coords[0] + "  " + ret)
            ok = False

        ret = variables.validate_int_ge_zero(v4, idx, self.name, "Y2 value", 4, split_line[4])
        if ret != True:
            print("[" + lib + "] " + coords[0] + "  " + ret)
            ok = False

        if p > 4:
            ret = variables.validate_int_ge_zero(v5, idx, self.name, "Wait value", 5, split_line[5])
            if ret != True:
                print("[" + lib + "] " + coords[0] + "  " + ret)
                ok = False

        if p > 5:
            ret = variables.validate_int_ge_zero(v6, idx, self.name, "Skip value", 6, split_line[6])
            if ret != True:
                print("[" + lib + "] " + coords[0] + "  " + ret)
                ok = False

        if not ok:
            return -1

        points = ms.line_coords(v1, v2, v3, v4)

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
            ret = variables.check_num(split_line, [2, 3, 4], idx, line, self.name)
            if ret != True:
                return ret

            ret = variables.check_int_param(split_line, 1, "X value", idx, self.name, line, variables.validate_int_ge_zero)
            if ret != True:
                return (ret, line)

            ret = variables.check_int_param(split_line, 2, "Y value", idx, self.name, line, variables.validate_int_ge_zero)
            if ret != True:
                return (ret, line)

            ret = variables.check_int_param(split_line, 3, "Wait value", idx, self.name, line, variables.validate_int_ge_zero, True)
            if ret != True:
                return (ret, line)

            ret = variables.check_int_param(split_line, 4, "Skip value", idx, self.name, line, variables.validate_int_gt_zero, True)
            if ret != True:
                return (ret, line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        ok = True 
        p = len(split_line) - 1

        v1 = variables.get_value(split_line[1], symbols)
        if v1:
            v1 = int(v1)

        v2 = variables.get_value(split_line[2], symbols)
        if v2:
            v2 = int(v2)

        if p > 2:
            v3 = variables.get_value(split_line[3], symbols)
            if v3:
                v3 = int(v3)
        else:
            v3 = None

        if p > 3:
            v4 = variables.get_value(split_line[4], symbols)
            if v4:
                v4 = int(v3)
        else:
            v4 = None

        delay = None
        if v3:
            delay = float(v4) / 1000.0

        skip = 1
        if v4:
            skip = int(v3)

        if (delay == None) or (delay <= 0):
            print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Mouse line move relative (" + \
                str(v1) + ", " + str(v2) + ") and wait " + str(v3) + " milliseconds between each step")
        else:
            print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Mouse line move relative (" + \
                str(v1) + ", " + str(v2) + ") by " + str(v4) + \
                " pixels per step and wait " + str(v3) + " milliseconds between each step")
                
        ret = variables.validate_int_ge_zero(v1, idx, self.name, "X value", 1, split_line[1])
        if ret != True:
            print("[" + lib + "] " + coords[0] + "  " + ret)
            ok = False

        ret = variables.validate_int_ge_zero(v2, idx, self.name, "Y value", 2, split_line[2])
        if ret != True:
            print("[" + lib + "] " + coords[0] + "  " + ret)
            ok = False

        if p > 2:
            ret = variables.validate_int_ge_zero(v3, idx, self.name, "Wait value", 3, split_line[3])
            if ret != True:
                print("[" + lib + "] " + coords[0] + "  " + ret)
                ok = False

        if p > 3:
            ret = variables.validate_int_gt_zero(v4, idx, self.name, "Skip value", 4, split_line[4])
            if ret != True:
                print("[" + lib + "] " + coords[0] + "  " + ret)
                ok = False

        if not ok:
            return -1

        x_C, y_C = ms.get_pos()
        x_N, y_N = x_C + v1, y_C + v2
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
            ret = variables.check_num(split_line, [2, 3, 4], idx, line, self.name)
            if ret != True:
                return ret

            ret = variables.check_int_param(split_line, 1, "X value", idx, self.name, line, variables.validate_int_ge_zero)
            if ret != True:
                return (ret, line)

            ret = variables.check_int_param(split_line, 2, "Y value", idx, self.name, line, variables.validate_int_ge_zero)
            if ret != True:
                return (ret, line)

            ret = variables.check_int_param(split_line, 3, "Wait value", idx, self.name, line, variables.validate_int_ge_zero, True)
            if ret != True:
                return (ret, line)

            ret = variables.check_int_param(split_line, 4, "Skip value", idx, self.name, line, variables.validate_int_gt_zero, True)
            if ret != True:
                return (ret, line)
            
        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        ok = True 
        p = len(split_line) - 1

        v1 = variables.get_value(split_line[1], symbols)
        if v1:
            v1 = int(v1)

        v2 = variables.get_value(split_line[2], symbols)
        if v1:
            v1 = int(v1)

        if p > 2:
            v3 = variables.get_value(split_line[3], symbols)
            if v3:
                v3 = int(v3)
        else:
            v3 = None

        if p > 3:
            v4 = variables.get_value(split_line[4], symbols)
            if v4:
                v4 = int(v4)
        else:
            v4 = None

        delay = None
        if v3:
            delay = float(v3) / 1000.0

        skip = 1
        if v4:
            skip = int(v4)

        if (delay == None) or (delay <= 0):
            print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Mouse line set (" + \
                split_line[1] + ", " + split_line[2] + ") by " + str(skip) + \
                " pixels per step")
        else:
            print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Mouse line set (" + \
            split_line[1] + ", " + split_line[2] + ") by " + str(skip) + \
            " pixels per step and wait " + split_line[3] + " milliseconds between each step")

        ret = variables.validate_int_ge_zero(v1, idx, self.name, "X value", 1, split_line[1])
        if ret != True:
            print("[" + lib + "] " + coords[0] + "  " + ret)
            ok = False

        ret = variables.validate_int_ge_zero(v2, idx, self.name, "Y value", 2, split_line[2])
        if ret != True:
            print("[" + lib + "] " + coords[0] + "  " + ret)
            ok = False

        if p > 2:
            ret = variables.validate_int_gt_zero(v3, idx, self.name, "Wait value", 3, split_line[3])
            if ret != True:
                print("[" + lib + "] " + coords[0] + "  " + ret)
                ok = False

        if p > 3:
            ret = variables.validate_int_ge_zero(v4, idx, self.name, "Skip value", 4, split_line[4])
            if ret != True:
                print("[" + lib + "] " + coords[0] + "  " + ret)
                ok = False

        if not ok:
            return -1

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
            ret = variables.check_num(split_line, [1, 2], idx, line, self.name)
            if ret != True:
                return ret

            ret = variables.check_int_param(split_line, 1, "Wait value", idx, self.name, line, variables.validate_int_ge_zero)
            if ret != True:
                return (ret, line)

            ret = variables.check_int_param(split_line, 2, "Skip value", idx, self.name, line, variables.validate_int_gt_zero, True)
            if ret != True:
                return (ret, line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        ok = True 
        p = len(split_line) - 1

        if p > 0:
            v1 = variables.get_value(split_line[1], symbols)
            if v1:
                v1 = int(v1)
        else:
            v1 = None

        if p > 1:
            v2 = variables.get_value(split_line[2], symbols)
            if v2:
                v2 = int(v2)
        else:
            v2 = None

        x1, y1 = symbols['m_pos']

        delay = None
        if v3:
            delay = float(v3) / 1000.0

        skip = 1
        if v4:
            skip = int(v4)

        if (delay == None) or (delay <= 0):
            print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Recall mouse position " + str(symbols["m_pos"]) + \
                " in a line by " + str(skip) + " pixels per step")
        else:
            print("[" + lib + "] " + coords + "  Line:" + str(idx+1) + "    Recall mouse position " + str(symbols["m_pos"]) + \
                " in a line by " + str(skip) + " pixels per step and wait " + \
                str(delay) + " milliseconds between each step")

        if p > 0:
            ret = variables.validate_int_ge_zero(v1, idx, self.name, "Skip value", 1, split_line[1])
            if ret != True:
                print("[" + lib + "] " + coords[0] + "  " + ret)
                ok = False

        if p > 3:
            ret = variables.validate_int_ge_zero(v2, idx, self.name, "Wait value", 2, split_line[2])
            if ret != True:
                print("[" + lib + "] " + coords[0] + "  " + ret)
                ok = False

        if not ok:
            return -1

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

        super().__init__("M_STORE" )  # the name of the command as you have to enter it in the code
            
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
            ret = variables.check_num(split_line, [0], idx, line, self.name)
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

        super().__init__("M_RECALL" ) # the name of the command as you have to enter it in the code
   

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
            ret = variables.check_num(split_line, [0], idx, line, self.name)
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

        if symbols['m_pos'] == tuple():
            print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    No 'M_STORE' command has been run, cannot do 'M_RECALL'")
        else:
            print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Recall mouse position " + str(symbols['m_pos']))
            ms.set_pos(symbols['m_pos'][0], symbols['m_pos'][1])

        return idx+1


scripts.add_command(Mouse_Recall())  # register the command


