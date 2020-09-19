import command_base, kb, lp_events, scripts, variables
from constants import *

LIB = "cmds_keys" # name of this library (for logging)

# ##################################################
# ### CLASS Keys_Wait_Pressed                    ###
# ##################################################

# class that defines the WAIT_PRESSED command (wait while a button is pressed?)
class Keys_Wait_Pressed(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__(
            "WAIT_PRESSED",  # the name of the command as you have to enter it in the code
            LIB,
            (),
            () )


    def Partial_run_step_info(self, ret, idx, split_line, symbols, coords, is_async):
        print(AM_PREFIX.format(self.lib, coords[BC_TEXT], str(idx+1)) + "    Wait for script key to be unpressed")


    def Process(self, idx, split_line, symbols, coords, is_async):
        while lp_events.pressed[coords[BC_X]][coords[BC_Y]]:
            sleep(DELAY_EXIT_CHECK)
            if check_kill(x, y, is_async):
                return idx + 1             

        return idx + 1             


scripts.add_command(Keys_Wait_Pressed())  # register the command


# ##################################################
# ### CLASS Keys_Tap                             ###
# ##################################################

# class that defines the TAP command (tap button a button)
class Keys_Tap(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__(
            "TAP",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var    type       p1_val                        p2_val 
            ("Key",        False, False, PT_KEY,    None,                         None), 
            ("Times",      True,  True,  PT_INT,    variables.Validate_gt_zero,   None), 
            ("Duration",   True,  True,  PT_FLOAT,  variables.Validate_ge_zero,   None), 
            ),
            (
            # num params, format string                           (trailing comma is important)
            (1,           "    Tap key {1}"), 
            (2,           "    Tap key {1}, {2} times"), 
            (3,           "    Tap key {1}, {2} times for {3} seconds each"), 
            ) )


    def Process(self, idx, split_line, symbols, coords, is_async):
        cnt = symbols[SYM_PARAM_CNT]
        key = kb.sp(symbols[SYM_PARAMS][1])
        releasefunc = lambda: None

        times = 1
        if cnt >= 2:
            times = int(symbols[SYM_PARAMS][2])

        delay = 0
        if cnt == 3:
            delay = float(symbols[SYM_PARAMS][3])
            releasefunc = lambda: kb.release(key)
        
        precheck = delay == 0 and times > 1

        for tap in range(taps):
            if check_kill(coords[BC_X], coords[BC_Y], is_async, releasefunc):
                return idx+1
                
            if delay == 0:
                kb.tap(key)
            else:
                kb.press(key)
                
            if precheck and check_kill(coords[BC_X], coords[BC_Y], is_async, releasefunc):
                return -1

            if delay > 0:
                if not safe_sleep(delay, coords[BC_X], coords[BC_Y], is_async, releasefunc):
                    return -1
                    
            releasefunc()
    

scripts.add_command(Keys_Tap())  # register the command


# ##################################################
# ### CLASS Keys_Press                           ###
# ##################################################

# class that defines the PRESS command (press a button)
class Keys_Press(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__(
            "PRESS",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var    type       p1_val              p2_val 
            ("Key",        False, False, PT_KEY,    None,               None), 
            ),
            (
            # num params, format string                           (trailing comma is important)
            (1,           "    Press key {1}"), 
            ) )


    def Process(self, idx, split_line, symbols, coords, is_async):
        key = kb.sp(symbols[SYM_PARAMS][1])
        kb.press(key)


scripts.add_command(Keys_Press())  # register the command


# ##################################################
# ### CLASS Keys_Release                         ###
# ##################################################

# class that defines the RELEASE command (un-press a button)
class Keys_Release(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__(
            "RELEASE",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var    type       p1_val              p2_val 
            ("Key",        False, False, PT_KEY,    None,               None), 
            ),
            (
            # num params, format string                           (trailing comma is important)
            (1,           "    Release key {1}"), 
            ) )


    def Process(self, idx, split_line, symbols, coords, is_async):
        key = kb.sp(symbols[SYM_PARAMS][1])
        kb.release(key)


scripts.add_command(Keys_Release())  # register the command


# ##################################################
# ### CLASS Keys_Release_All                     ###
# ##################################################

# class that defines the RELEASE_ALL command (un-press all keys)
class Keys_Release_All(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__(
            "RELEASE_ALL",  # the name of the command as you have to enter it in the code
            LIB,
            (),
            (
            # num params, format string                           (trailing comma is important)
            (0,           "    Release all keys"), 
            ) )


    def Process(self, idx, split_line, symbols, coords, is_async):
        kb.release_all()


scripts.add_command(Keys_Release_All())  # register the command


# ##################################################
# ### CLASS Keys_String                          ###
# ##################################################

# class that defines the STRING command (type a string)
class Keys_String(command_base.Command_Text_Basic):
    def __init__(
        self ):
 
        super().__init__("STRING",      # the name of the command as you have to enter it in the code
            LIB,
            "Type out string" )

        self.valid_num_params = [1, None]  # There is a minimum


    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        type_string = " ".join(split_line[1:])
        kb.write(type_string)

        return idx+1


scripts.add_command(Keys_String())  # register the command
