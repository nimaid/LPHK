import command_base, ms, scripts


# ##################################################
# ### CLASS Mouse_Move                           ###
# ##################################################

# class that defines the M_MOVE command (wait while a button is pressed?)
class Mouse_Move(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("M_MOVE")

    def Validate(
        self,
        idx: int,
        line,
        lines,
        split_line,
        symbols,
        pass_no
        ):

        # no longer allow just 2 tokens

        if pass_no == 1:
            if len(split_line) < 3:
                return ("Too few arguments for command '" + split_line[0] + "'.", line)

            if len(split_line) > 3:
                return ("Too many arguments for command '" + split_line[0] + "'.", line)

            try:
                temp = int(split_line[1])
            except:
                return ("'M_MOVE' X value '" + split_line[1] + "' not valid.", line)

            try:
                temp = int(split_line[2])
            except:
                return ("'M_MOVE' Y value '" + split_line[2] + "' not valid.", line)

        return True

    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        # removed error for != 3 tokens

        print("[cmds_mous] " + coords[0] + "    Relative mouse movement (" + split_line[1] + ", " + \
            str(split_line[2]) + ")")

        ms.move_to_pos(float(split_line[1]), float(split_line[2]))

        return idx+1


scripts.add_command(Mouse_Move())


# ##################################################
# ### CLASS Mouse_Set                            ###
# ##################################################

# class that defines the M_SET command (put the mouse somewhere)
class Mouse_Set(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("M_SET")

    def Validate(
        self,
        idx: int,
        line,
        lines,
        split_line,
        symbols,
        pass_no
        ):

        # no longer allow just 2 tokens

        if pass_no == 1:
            if len(split_line) < 3:
                return ("Too few arguments for command '" + split_line[0] + "'.", line)

            if len(split_line) > 3:
                return ("Too many arguments for command '" + split_line[0] + "'.", line)

            try:
                temp = int(split_line[1])
            except:
                return ("'M_SET' X value '" + split_line[1] + "' not valid.", line)

            try:
                temp = int(split_line[2])
            except:
                return ("'M_SET' Y value '" + split_line[2] + "' not valid.", line)

        return True

    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        # removed error for != 3 tokens

        print("[cmds_mous] " + coords[0] + "    Set mouse position to (" + split_line[1] + ", " + \
            str(split_line[2]) + ")")

        ms.set_pos(float(split_line[1]), float(split_line[2]))

        return idx+1


scripts.add_command(Mouse_Set())


# ##################################################
# ### CLASS Mouse_Scroll                         ###
# ##################################################

# class that defines the M_SCROLL command (???)
class Mouse_Scroll(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("M_SCROLL")

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
            if len(split_line) < 2:
                return ("Too few arguments for command '" + split_line[0] + "'.", line)

            if len(split_line) > 3:
                return ("Too many arguments for command '" + split_line[0] + "'.", line)

            try:
                temp = int(split_line[1])
            except:
                return ("'M_SET' X value '" + split_line[1] + "' not valid.", line)

            try:
                temp = float(split_line[1])
            except:
                return ("Invalid scroll amount '" + split_line[1] + "'.", line)

            if len(split_line) > 2:
                try:
                    temp = float(split_line[2])
                except:
                    return ("Invalid scroll amount '" + split_line[2] + "'.", line)

        return True

    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        if len(split_line) > 2:
            print("[cmds_mous] " + coords + "    Scroll (" + split_line[1] + ", " + split_line[2] + ")")
            ms.scroll(float(split_line[2]), float(split_line[1]))
        else:
            print("[cmds_mous] " + coords + "    Scroll " + split_line[1])
            ms.scroll(0, float(split_line[1]))

        return idx+1


scripts.add_command(Mouse_Scroll())


# ##################################################
# ### CLASS Mouse_Line                           ###
# ##################################################

# class that defines the M_LINE command (draw a line?)
class Mouse_Line(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("M_LINE")

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
            if len(split_line) < 5:
                return ("Too few arguments for command '" + split_line[0] + "'.", line)

            if len(split_line) > 7:
                return ("Too many arguments for command '" + split_line[0] + "'.", line)

            try:
                temp = int(split_line[1])
            except:
                return ("'M_LINE' X1 value '" + split_line[1] + "' not valid.", line)

            try:
                temp = int(split_line[2])
            except:
                return ("'M_LINE' Y1 value '" + split_line[2] + "' not valid.", line)

            try:
                temp = int(split_line[3])
            except:
                return ("'M_LINE' X2 value '" + split_line[3] + "' not valid.", line)

            try:
                temp = int(split_line[4])
            except:
                return ("'M_LINE' Y2 value '" + split_line[4] + "' not valid.", line)

            if len(split_line) >= 6:
                try:
                    temp = float(split_line[5])
                except:
                    return ("'M_LINE' wait value '" + split_line[5] + "' not valid.", line)

            if len(split_line) >= 7:
                try:
                    temp = int(split_line[6])
                    if temp == 0:
                        return ("'M_LINE' skip value cannot be zero.", line)
                except:
                    return ("'M_LINE' skip value '" + split_line[6] + "' not valid.", line)

        return True

    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
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
            print("[cmds_mous] " + coords[0] + "    Mouse line from (" + \
                split_line[1] + ", " + split_line[2] + ") to (" + \
                split_line[3] + ", " + split_line[4] + ") by " + str(skip) + " pixels per step")
        else:
            print("[cmds_mous] " + coords + "    Mouse line from (" + \
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


scripts.add_command(Mouse_Line())


# ##################################################
# ### CLASS Mouse_Line_Move                           ###
# ##################################################

# class that defines the M_LINE_MOVE command 
class Mouse_Line_Move(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("M_LINE_MOVE")

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
            if len(split_line) < 3:
                return ("'" + split_line[0] + "' requires at least X and Y arguments.", line)

            try:
                temp = int(split_line[1])
            except:
                return ("'" + split_line[0] + "' X value '" + split_line[1] + "' not valid.", line)

            try:
                temp = int(split_line[2])
            except:
                return ("'" + split_line[0] + "' Y value '" + split_line[2] + "' not valid.", line)

            if len(split_line) >= 4:
                try:
                    temp = float(split_line[3])
                except:
                    return ("'" + split_line[0] + "' wait value '" + split_line[3] + "' not valid.", line)

            if len(split_line) >= 5:
                try:
                    temp = int(split_line[4])
                    if temp == 0:
                        return ("'" + split_line[0] + "' skip value cannot be zero.", line)
                except:
                    return ("'" + split_line[0] + "' skip value '" + split_line[4] + "' not valid.", line)

        return True

    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
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
            print("[cmds_mous] " + coords + "    Mouse line move relative (" + \
                split_line[1] + ", " + split_line[2] + ") by " + str(skip) + \
                " pixels per step")
        else:
            print("[cmds_mous] " + coords + "    Mouse line move relative (" + \
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


scripts.add_command(Mouse_Line_Move())


# ##################################################
# ### CLASS Mouse_Line_Set                       ###
# ##################################################

# class that defines the M_LINE_SET command 
class Mouse_Line_Set(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("M_LINE_SET")

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
            if len(split_line) < 3:
                return ("'" + split_line[0] + "' requires at least X and Y arguments.", line)

            try:
                temp = int(split_line[1])
            except:
                return ("'" + split_line[0] + "' X value '" + split_line[1] + "' not valid.", line)

            try:
                temp = int(split_line[2])
            except:
                return ("'" + split_line[0] + "' Y value '" + split_line[2] + "' not valid.", line)

            if len(split_line) >= 4:
                try:
                     temp = float(split_line[3])
                except:
                    return ("'" + split_line[0] + "' wait value '" + split_line[3] + "' not valid.", line)

            if len(split_line) >= 5:
                try:
                    temp = int(split_line[4])
                    if temp == 0:
                        return ("'" + split_line[0] + "' skip value cannot be zero.", line)
                except:
                    return ("'" + split_line[0] + "' skip value '" + split_line[4] + "' not valid.", line)

        return True

    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
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
            print("[cmds_mous] " + coords[0] + "    Mouse line set (" + \
                split_line[1] + ", " + split_line[2] + ") by " + str(skip) + \
                " pixels per step")
        else:
            print("[cmds_mous] " + coords[0] + "    Mouse line set (" + \
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


scripts.add_command(Mouse_Line_Set())


# ##################################################
# ### CLASS Mouse_Recall_Line                    ###
# ##################################################

# class that defines the M_RECALL_LINE command 
class Mouse_Recall_Line(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("M_RECALL_LINE")

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
            if len(split_line) > 1:
                try:
                    temp = float(split_line[1])
                except:
                    return ("'" + split_line[0] + "' wait value '" + split_line[1] + "' not valid.", line)

            if len(split_line) > 2:
                try:
                    temp = int(split_line[2])
                    if temp == 0:
                        return ("'" + split_line[0] + "' skip value cannot be zero.", line)
                except:
                    return ("'" + split_line[0] + "' skip value '" + split_line[2] + "' not valid.", line)

        return True

    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        x1, y1 = symbols['m_pos']

        delay = None
        if len(split_line) > 1:
            delay = float(split_line[1]) / 1000.0

        skip = 1
        if len(split_line) > 2:
            skip = int(split_line[2])

        if (delay == None) or (delay <= 0):
            print("[cmds_mous] " + coords + "    Recall mouse position " + str(symbols["m_pos"]) + \
                " in a line by " + str(skip) + " pixels per step")
        else:
            print("[cmds_mous] " + coords + "    Recall mouse position " + str(symbols["m_pos"]) + \
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


scripts.add_command(Mouse_Recall_Line())


# ##################################################
# ### CLASS Mouse_Store                          ###
# ##################################################

# class that defines the M_STORE command 
class Mouse_Store(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("M_STORE")

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
            if len(split_line) > 1:
                return ("'" + split_line[0] + "' takes no arguments.", line)

        return True

    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        print("[cmds_mous] " + coords[0] + "    Store mouse position")

        symbols["m_pos"] = ms.get_pos()

        return idx+1


scripts.add_command(Mouse_Store())


# ##################################################
# ### CLASS Mouse_Recall                         ###
# ##################################################

# class that defines the M_RECALL command 
class Mouse_Recall(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("M_RECALL")

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
            if len(split_line) > 1:
                return ("'" + split_line[0] + "' takes no arguments.", line)

        return True

    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        if symbols['m_pos'] == tuple():
            print("[cmds_mous] " + coords[0] + "    No 'M_STORE' command has been run, cannot do 'M_RECALL'")
        else:
            print("[cmds_mous] " + coords[0] + "    Recall mouse position " + str(symbols['m_pos']))
            ms.set_pos(symbols['m_pos'][0], symbols['m_pos'][1])

        return idx+1


scripts.add_command(Mouse_Recall())


