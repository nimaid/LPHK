# This module is VERY specific to Win32
import command_base, ms, scripts, variables, win32gui, win32process, win32api
from constants import *

LIB = "cmds_wn32" # name of this library (for logging)

# ##################################################
# ### CLASS WIN32_GET_CURSOR                     ###
# ##################################################

# class that defines the W_GET_CURSOR command -- gets the location of the cursor on the current form
class Win32_Get_Cursor(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("W_GET_CURSOR",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var   type     p1_val                      p2_val 
            ("X value",    False, True, PT_VAR,  None,                       None),
            ("Y value",    False, True, PT_VAR,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2,           "    Store screen absolute cursor position in variables ({1}, {2})"), 
            ) )


    def get_cursor(self):
        # get current cursor position within window

        res = (-1, -1) # failure value
        
        fg_win = win32gui.GetForegroundWindow()                                # find the current foreground window
        fg_thread, fg_process = win32process.GetWindowThreadProcessId(fg_win)  # get thread and process information
        current_thread = win32api.GetCurrentThreadId()                         # find the current thread
        win32process.AttachThreadInput(current_thread, fg_thread, True)        # attach to the current thread
        try:
            res = win32gui.GetCaretPos()                                       # find the caret
        finally:
            win32process.AttachThreadInput(current_thread, fg_thread, False)   # and always detatch from the other thread

        return res # and this is where the text cursor is

    def Process(self, btn, idx, split_line):
        x, y = self.get_cursor()                                               # get x,y position of text cursor on fg window

        self.Set_param(btn, 1, x)                                              # store the result
        self.Set_param(btn, 2, y)


scripts.Add_command(Win32_Get_Cursor())  # register the command


# ##################################################
# ### CLASS W_GET_FG_HWND                        ###
# ##################################################

# class that defines the W_GET_FG_HWND command - gets the handle of the current foreground window
class Win32_Get_Fg_Hwnd(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("W_GET_FG_HWND",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var   type     p1_val                      p2_val 
            ("HWND",       False, True, PT_VAR,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (1,           "    Return the handle of the current foreground window into {1}"), 
            ) )


    def Process(self, btn, idx, split_line):
        hwnd = win32gui.GetForegroundWindow()  # get the current window
        
        #variables.Auto_store(btn.symbols[SYM_PARAMS][1], hwnd, btn.symbols)  # Return the current window
        self.Set_param(btn, 1, hwnd)


scripts.Add_command(Win32_Get_Fg_Hwnd())  # register the command


# ##################################################
# ### CLASS W_SET_FG_HWND                        ###
# ##################################################

# class that defines the W_SET_FG_HWND command - makes the window pointed to by hwnd the current window
class Win32_Set_Fg_Hwnd(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("W_SET_FG_HWND",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var   type     p1_val                      p2_val 
            ("HWND",       False, True, PT_INT,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (1,           "    Make window {1} the current window"), 
            ) )


    def Process(self, btn, idx, split_line):
        hwnd = self.Get_param(btn, 1)           # get the window handle from the passed variable (or constant)
        win32gui.SetForegroundWindow(hwnd)      # make it the foreground window


scripts.Add_command(Win32_Set_Fg_Hwnd())  # register the command


# ##################################################
# ### CLASS W_CLIENT_TO_SCREEN                   ###
# ##################################################

# class that defines the W_CLIENT_TO_SCREEN command - converts a form relative coordinate to a screen (absolute) coord
class Win32_Client_To_Screen(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("W_CLIENT_TO_SCREEN",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var   type     p1_val                      p2_val 
            ("HWND",       False, True, PT_INT,  None,                       None),
            ("X value",    False, True, PT_VAR,  None,                       None),
            ("Y value",    False, True, PT_VAR,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (3,           "    Convert form relative coord in ({1}, {2}) to screen (abs)"), 
            ) )


    def Process(self, btn, idx, split_line):
        x = self.Get_param(btn, 2)      # get x,y value
        y = self.Get_param(btn, 3)
            
        x, y = win32gui.ClientToScreen(btn.symbols[SYM_PARAMS][1], (x, y))  # convert client coords to screen coords
        
        self.Set_param(btn, 2, x)       # set new x, y values
        self.Set_param(btn, 3, y)


scripts.Add_command(Win32_Client_To_Screen())  # register the command


# ##################################################
# ### CLASS W_FIND_HWND                          ###
# ##################################################

# class that defines the W_FIND_HWND command - returns the nth matching window handle
class Win32_Find_Hwnd(command_base.Command_Basic):
    def __init__(
        self,
        ): 
        
        super().__init__("W_FIND_HWND",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var    type     p1_val                      p2_val 
            ("Title",      False, False, PT_TEXT, None,                       None),   # name to search for (use ~ for space
            ("HWND",       False, True,  PT_VAR,  None,                       None),   # variable to contain HWND
            ("M",          False, True,  PT_VAR,  None,                       None),   # number of matches found (if M<N then error)
            ("N",          False, True,  PT_INT,  variables.Validate_gt_zero, None),   # number of match desired
            ),
            (
            # num params, format string                           (trailing comma is important)
            (4,           "    Find {4}th window titled '{1}', returning handle in {2}.  Report {3} total matches"), 
            ) )
            
    def Process(self, btn, idx, split_line):
    
        def CheckWindow(hwnd, data):
            # callback function to receive enumerated window handles
            if win32gui.GetWindowText(hwnd) == data['title']:  # does it match?
                data['hwnds'] += [hwnd]                        # add to list
        
        hwnds = []                                             # reset the list of window handles
        title = self.Get_param(btn, 1).replace('~', ' ')       # get the title we're searching for

        data = {'title':title, 'hwnds':hwnds}                  # data structure to be used by the callback routine
        win32gui.EnumWindows(CheckWindow, data)                # enumerate windows
        
        hwnds = data['hwnds']                                  # this is now probably in front to back order
        hwnds.sort()                                           # helps to ensure we get the windows in the same order.  (creation?)
        
        m = len(hwnds)                                         # how many did we get?
        self.Set_param(btn, 3, m)                              # pass this back
        
        n = self.Get_param(btn, 4)                             # which one did we want?
        if n <= m:                                             # do we have it
            hwnd = hwnds[n-1]                                  # get it
        else:
            hwnd = -1                                          # otherwise return -1
            
        self.Set_param(btn, 2, hwnd)                           # return the window handle in parameter 2


scripts.Add_command(Win32_Find_Hwnd())  # register the command
