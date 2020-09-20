import command_base, ms, scripts, variables
from constants import *

LIB = "cmds_mous" # name of this library (for logging)

# ##################################################
# ### CLASS Mouse_Move                           ###
# ##################################################

# class that defines the M_MOVE command (relative mouse movement)
class Mouse_Move(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("M_MOVE",     # the name of the command as you have to enter it in the code
            LIB,                       # the name of this module
            (                          # description of parameters
            # Desc      Opt    Var   type      p1_val p2_val  (trailing comma is important)
            ("X value", False, True, PT_INT,   None,  None), 
            ("Y value", False, True, PT_INT,   None,  None),
            ),
            (                          # How to log runtime execution 
            # num params, format string                           (trailing comma is important)
            (2,           "    Relative mouse movement ({1}, {2})"), 
            ) )


    def Process(self, btn, idx, split_line):
        ms.move_to_pos(float(btn.symbols[SYM_PARAMS][1]), float(btn.symbols[SYM_PARAMS][2]))
    

scripts.Add_command(Mouse_Move())  # register the command


# ##################################################
# ### CLASS Mouse_Set                            ###
# ##################################################

# class that defines the M_SET command (put the mouse somewhere)
class Mouse_Set(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("M_SET",   # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc      Opt    Var   type     p1_val                      p2_val 
            ("X value", False, True, PT_INT,  variables.Validate_ge_zero, None),
            ("Y value", False, True, PT_INT,  variables.Validate_ge_zero, None),
            ),
            (                          # How to log runtime execution 
            # num params, format string                           (trailing comma is important)
            (2,           "    Set mouse position to ({1}, {2})"), 
            ) )


    def Process(self, btn, idx, split_line):
        ms.set_pos(float(btn.symbols[SYM_PARAMS][1]), float(btn.symbols[SYM_PARAMS][2]))


scripts.Add_command(Mouse_Set())  # register the command


# ##################################################
# ### CLASS Mouse_Scroll                         ###
# ##################################################

# class that defines the M_SCROLL command (???)
class Mouse_Scroll(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("M_SCROLL",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc            Opt    Var   type     p1_val p2_val 
            ("Scroll amount", False, True, PT_INT,  None,  None),
            ("X value",       True,  True, PT_INT,  None,  None),
            ),
            (                          # How to log runtime execution 
            # num params, format string                           (trailing comma is important)
            (1,           "    Scroll {1}"), 
            (2,           "    Scroll ({1}, {2})"), 
            ) )


    def Process(self, btn, idx, split_line):
        if btn.symbols[SYM_PARAMS][2]:
            ms.scroll(float(btn.symbols[SYM_PARAMS][2]), float(btn.symbols[SYM_PARAMS][1]))
        else:
            ms.scroll(0, float(btn.symbols[SYM_PARAMS][1]))


scripts.Add_command(Mouse_Scroll())  # register the command


# ##################################################
# ### CLASS Mouse_Line                           ###
# ##################################################

# class that defines the M_LINE command (draw a line?)
class Mouse_Line(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("M_LINE",   # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var   type     p1_val                      p2_val 
            ("X1 value",   False, True, PT_INT,  variables.Validate_ge_zero, None), 
            ("Y1 value",   False, True, PT_INT,  variables.Validate_ge_zero, None), 
            ("X2 value",   False, True, PT_INT,  variables.Validate_ge_zero, None), 
            ("Y2 value",   False, True, PT_INT,  variables.Validate_ge_zero, None), 
            ("Wait value", True,  True, PT_INT,  variables.Validate_ge_zero, None), 
            ("Skip value", True,  True, PT_INT,  variables.Validate_gt_zero, None),
            ),
            (                          # How to log runtime execution 
            # num params, format string                           (trailing comma is important)
            (4,           "    Mouse line from ({1}, {2}) to ({3}, {4})"), 
            (5,           "    Mouse line from ({1}, {2}) to ({3}, {4}) and wait {5}ms between steps"), 
            (6,           "    Mouse line from ({1}, {2}) to ({3}, {4}) by {6} pixels per step and wait {5}ms between steps"), 
            ) )


    def Process(self, btn, idx, split_line):
        delay = None
        if btn.symbols[SYM_PARAMS][5]:
            delay = float(btn.symbols[SYM_PARAMS][5]) / 1000.0

        skip = 1
        if btn.symbols[SYM_PARAMS][6]:
            skip = int(btn.symbols[SYM_PARAMS][6])

        points = ms.line_coords(btn.symbols[SYM_PARAMS][1], btn.symbols[SYM_PARAMS][2], btn.symbols[SYM_PARAMS][3], btn.symbols[SYM_PARAMS][4])

        for x_M, y_M in points[::skip]:
            if btn.Check_kill():
                return -1

            ms.set_pos(x_M, y_M)

            if (delay != None) and (delay > 0):
                if not btn.Safe_sleep(delay):
                    return -1


scripts.Add_command(Mouse_Line())  # register the command


# ##################################################
# ### CLASS Mouse_Line_Move                      ###
# ##################################################

# class that defines the M_LINE_MOVE command
class Mouse_Line_Move(command_base.Command_Basic):
    def __init__(
        self,
         ):

        super().__init__("M_LINE_MOVE",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var   type     p1_val                      p2_val 
            ("X value",    False, True, PT_INT,  None, None), 
            ("Y value",    False, True, PT_INT,  None, None), 
            ("Wait value", True,  True, PT_INT,  variables.Validate_gt_zero, None), 
            ("Skip value", True,  True, PT_INT,  variables.Validate_ge_zero, None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2,           "    Mouse line move relative ({1}, {2})"), 
            (3,           "    Mouse line move relative ({1}, {2}) and wait {3}ms between steps"), 
            (4,           "    Mouse line move relative ({1}, {2}) by {4} pixels per step and wait {3}ms between steps"), 
            ) )


    def Process(self, btn, idx, split_line):
        delay = None
        if btn.symbols[SYM_PARAMS][3]:
            delay = float(btn.symbols[SYM_PARAMS][3]) / 1000.0

        skip = 1
        if btn.symbols[SYM_PARAMS][4]:
            skip = int(btn.symbols[SYM_PARAMS][4])
            
        x_C, y_C = ms.get_pos()
        x_N, y_N = x_C + btn.symbols[SYM_PARAMS][1], y_C + btn.symbols[SYM_PARAMS][2]
        points = ms.line_coords(x_C, y_C, x_N, y_N)

        for x_M, y_M in points[::skip]:
            if btn.Check_kill():
                return -1

            ms.set_pos(x_M, y_M)

            if (delay != None) and (delay > 0):
                if not btn.Safe_sleep(delay):
                    return -1



scripts.Add_command(Mouse_Line_Move())  # register the command


# ##################################################
# ### CLASS Mouse_Line_Set                       ###
# ##################################################

# class that defines the M_LINE_SET command
class Mouse_Line_Set(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("M_LINE_SET",   # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var   type     p1_val                      p2_val 
            ("X value",    False, True, PT_INT,  variables.Validate_ge_zero, None),
            ("Y value",    False, True, PT_INT,  variables.Validate_ge_zero, None),
            ("Wait value", True,  True, PT_INT,  variables.Validate_ge_zero, None),
            ("Skip value", True,  True, PT_INT,  variables.Validate_gt_zero, None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2,           "    Mouse set line ({1}, {2})"), 
            (3,           "    Mouse set line ({1}, {2}) and wait {3}ms between steps"), 
            (4,           "    Mouse set line ({1}, {2}) by {4} pixels per step and wait {3}ms between steps"), 
            ) )


    def Process(self, btn, idx, split_line):
        delay = None
        if self.params[3]:
            delay = float(self.params[3]) / 1000.0

        skip = 1
        if self.params[4]:
            skip = int(self.params[4])

        x_C, y_C = ms.get_pos()
        points = ms.line_coords(x_C, y_C, params[1], params[2])

        for x_M, y_M in points[::skip]:
            if btn.Check_kill():
                return -1
            ms.set_pos(x_M, y_M)
            if (delay != None) and (delay > 0):
                if not btn.Safe_sleep(delay):
                    return -1


scripts.Add_command(Mouse_Line_Set())  # register the command


# ##################################################
# ### CLASS Mouse_Recall_Line                    ###
# ##################################################

# class that defines the M_RECALL_LINE command
class Mouse_Recall_Line(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("M_RECALL_LINE",   # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var   type     p1_val                      p2_val 
            ("Wait value", True , True, PT_INT,  variables.Validate_ge_zero, None),
            ("Skip value", True,  True, PT_INT,  variables.Validate_gt_zero, None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (0,           "    Recall mouse position () in a line"), 
            (1,           "    Recall mouse position () in a line and wait {1} milliseconds between each step"), 
            (2,           "    Recall mouse position () in a line by {2} pixels per step and wait {1} milliseconds between each step"), 
            ) )


    def Process(self, btn, idx, split_line):
        # while this looks like validation, it is just a warning
        if btn.symbols[SYM_MOUSE] == tuple():
            print("[" + lib + "] " + btn.coords + "  Line:" + str(idx+1) + "    No 'M_STORE' command has been run, cannot do 'M_RECALL'")
        else:
            print("[" + lib + "] " + btn.coords + "  Line:" + str(idx+1) + "    Recall mouse position " + str(btn.symbols[SYM_MOUSE]))

            x1, y1 = btn.symbols[SYM_MOUSE]

            delay = 0
            if self.params[1]:
                delay = float(self.params[3]) / 1000.0

            skip = 1
            if self.params[2]:
                skip = int(self.params[4])

            x_C, y_C = ms.get_pos()
            points = ms.line_coords(x_C, y_C, x1, y1)

            for x_M, y_M in points[::skip]:
                if btn.Check_kill():
                    return -1

                ms.set_pos(x_M, y_M)

                if (delay != None) and (delay > 0):
                    if not btn.Safe_sleep(delay):
                        return -1


scripts.Add_command(Mouse_Recall_Line())  # register the command


# ##################################################
# ### CLASS Mouse_Store                          ###
# ##################################################

# class that defines the M_STORE command
class Mouse_Store(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("M_STORE",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # no variables defined, so none are allowed
            ),
            (
            # num params, format string                           (trailing comma is important)
            (0,           "    Store mouse position"), 
            ) )


    def Process(self, btn, idx, split_line):
        btn.symbols[SYM_MOUSE] = ms.get_pos()  # Another example of modifying the symbol table during execution.


scripts.Add_command(Mouse_Store())  # register the command


# ##################################################
# ### CLASS Mouse_Recall                         ###
# ##################################################

# class that defines the M_RECALL command
class Mouse_Recall(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("M_RECALL",   # the name of the command as you have to enter it in the code
            (
            # no variables defined, so none are allowed
            ),
            (
            # no message format, so default will be used
            ) )

        self.run_states = [RS_INIT, RS_GET, RS_VALIDATE, RS_RUN, RS_FINAL]  # we won't do RS_INFO


    def Process(self, btn, idx, split_line):
        # while this looks like validation, it is really just the info. Putting it here is easy
        if btn.symbols[SYM_MOUSE] == tuple():
            print("[" + lib + "] " + btn.coords + "  Line:" + str(idx+1) + "    No 'M_STORE' command has been run, cannot do 'M_RECALL'")
        else:
            print("[" + lib + "] " + btn.coords + "  Line:" + str(idx+1) + "    Recall mouse position " + str(btn.symbols[SYM_MOUSE]))
            ms.set_pos(btn.symbols[SYM_MOUSE][0], btn.symbols[SYM_MOUSE][1])


scripts.Add_command(Mouse_Recall())  # register the command
