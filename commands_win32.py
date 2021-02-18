# This module is VERY specific to Win32
import command_base, ms, kb, scripts, variables, win32gui, win32process, win32api, win32con, win32clipboard, win32event
from constants import *

LIB = "cmds_wn32" # name of this library (for logging)

# ##################################################
# ### CLASS COMMAND_WIN32                        ###
# ##################################################

# class that defines more win32 stuff that gets used in various places
class Command_Win32(command_base.Command_Basic):

    # restores a window, returning its original state
    def restore_window(self, hwnd, fg = False):
        old_hwnd = win32gui.GetForegroundWindow()                # save the current window
        place = win32gui.GetWindowPlacement(hwnd)                # get info about the window
        
        if place[1] == win32con.SW_SHOWMAXIMIZED:                # if it is maximised
            win32gui.ShowWindow(hwnd, win32con.SW_SHOWMAXIMISED) # then keep it maximised
        elif place[1] == win32con.SW_SHOWMINIMIZED:              # if minimised
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)       # then restore it
        else:
            win32gui.ShowWindow(hwnd, win32con.SW_NORMAL)        # otherwise a normal show is fin
        
        if fg and (hwnd != old_hwnd):
            win32gui.SetForegroundWindow(hwnd)
        
        return place[1], old_hwnd, hwnd                          # useful if you want to minimise it again

    # resets windows to what they were before the restore
    def reset_window(self, old_state):
        state, old_hwnd, hwnd = old_state

        if state == win32con.SW_SHOWMINIMIZED:                   # re-minimise if it was minimised
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            
        if hwnd != old_hwnd:                                     # set fg window if it was different
            win32gui.SetForegroundWindow(old_hwnd)


# ##################################################
# ### CLASS WIN32_GET_CURSOR                     ###
# ##################################################

# class that defines the W_GET_CARET command -- gets the location of the cursor on the current form
class Win32_Get_Caret(Command_Win32):
    def __init__(
        self,
        ):

        super().__init__("W_GET_CARET",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val 
            ("X value",    False, AVV_REQD, PT_INT,  None,                       None),
            ("Y value",    False, AVV_REQD, PT_INT,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2,           "    Store screen absolute caret position in variables ({1}, {2})"), 
            ) )


    def get_caret(self):
        # get current caret position within window

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


scripts.Add_command(Win32_Get_Caret())  # register the command


# ##################################################
# ### CLASS W_GET_FG_HWND                        ###
# ##################################################

# class that defines the W_GET_FG_HWND command - gets the handle of the current foreground window
class Win32_Get_Fg_Hwnd(Command_Win32):
    def __init__(
        self,
        ):

        super().__init__("W_GET_FG_HWND",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val 
            ("HWND",       False, AVV_REQD, PT_INT,  None,                       None),
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
class Win32_Set_Fg_Hwnd(Command_Win32):
    def __init__(
        self,
        ):

        super().__init__("W_SET_FG_HWND",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val 
            ("HWND",       False, AVV_YES,  PT_INT,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (1,           "    Make window {1} the current window"), 
            ) )


    def Process(self, btn, idx, split_line):
        hwnd = self.Get_param(btn, 1)                   # get the window handle from the passed variable (or constant)
        
        old_x, old_y = ms.get_pos()                     # save the position of the mouse
        self.restore_window(hwnd)                       # show the window
        
        # positioning the mouse on the form while we make it the foreground seems to help
        x, y = win32gui.ClientToScreen(hwnd, (10, 10))  # get a position just inside the window
        ms.set_pos(x, y)                                # put the mouse on the form
        win32gui.SetForegroundWindow(hwnd)              # Make the window current
        ms.set_pos(old_x, old_y)                        # restore the mouse position

        
scripts.Add_command(Win32_Set_Fg_Hwnd())  # register the command


# ##################################################
# ### CLASS W_CLIENT_TO_SCREEN                   ###
# ##################################################

# class that defines the W_CLIENT_TO_SCREEN command - converts a form relative coordinate to a screen (absolute) coord
class Win32_Client_To_Screen(Command_Win32):
    def __init__(
        self,
        ):

        super().__init__("W_CLIENT_TO_SCREEN",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val 
            ("X value",    False, AVV_REQD, PT_INT,  None,                       None),
            ("Y value",    False, AVV_REQD, PT_INT,  None,                       None),
            ("HWND",       True,  AVV_YES,  PT_INT,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2,           "    Convert form relative coord in ({1}, {2}) in curent window to screen (abs)"), 
            (3,           "    Convert form relative coord in ({1}, {2}) in window {3} to screen (abs)"), 
            ) )

            
    def Process(self, btn, idx, split_line):
        x = self.Get_param(btn, 1)                                     # get x,y value
        y = self.Get_param(btn, 2)
        
        hwnd = self.Get_param(btn, 3, win32gui.GetForegroundWindow())  # get the window
        state = self.restore_window(hwnd)
        try:
            x, y = win32gui.ClientToScreen(hwnd, (x, y))                   # convert client coords to screen coords
               
            self.Set_param(btn, 1, x)                                      # set new x, y values
            self.Set_param(btn, 2, y)
        finally:
            self.reset_window(state)


scripts.Add_command(Win32_Client_To_Screen())  # register the command


# ##################################################
# ### CLASS W_SCREEN_TO_CLIENT                   ###
# ##################################################

# class that defines the W_SCREEN_TO_CLIENT command - converts a screen (absolute) coord to a form relative coordinate
class Win32_Screen_To_Client(Command_Win32):
    def __init__(
        self,
        ):

        super().__init__("W_SCREEN_TO_CLIENT",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val 
            ("X value",    False, AVV_REQD, PT_INT,  None,                       None),
            ("Y value",    False, AVV_REQD, PT_INT,  None,                       None),
            ("HWND",       True,  AVV_YES,  PT_INT,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2,           "    Convert form absolute coord in ({1}, {2}) to relative to current window"), 
            (3,           "    Convert form absolute coord in ({1}, {2}) to relative to window {3}"), 
            ) )

            
    def Process(self, btn, idx, split_line):
        x = self.Get_param(btn, 1)                                     # get x,y value
        y = self.Get_param(btn, 2)
        
        hwnd = self.Get_param(btn, 3, win32gui.GetForegroundWindow())  # get the window
        state = self.restore_window(hwnd)
        try:        
            x, y = win32gui.ScreenToClient(hwnd, (x, y))                   # convert client coords to screen coords
               
            self.Set_param(btn, 1, x)                                      # set new x, y values
            self.Set_param(btn, 2, y)        
        finally:
            self.reset_window(state)


scripts.Add_command(Win32_Screen_To_Client())  # register the command


# ##################################################
# ### CLASS W_FIND_HWND                          ###
# ##################################################

# class that defines the W_FIND_HWND command - returns the nth matching window handle
class Win32_Find_Hwnd(Command_Win32):
    def __init__(
        self,
        ): 
        
        super().__init__("W_FIND_HWND",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val 
            ("Title",      False, AVV_YES,  PT_TEXT, None,                       None),   # name to search for (use ~ for space
            ("HWND",       False, AVV_REQD, PT_INT,  None,                       None),   # variable to contain HWND
            ("M",          False, AVV_REQD, PT_INT,  None,                       None),   # number of matches found (if M<N then error)
            ("N",          False, AVV_YES,  PT_INT,  variables.Validate_gt_zero, None),   # number of match desired
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


# ##################################################
# ### CLASS W_COPY                               ###
# ##################################################

# class that defines the W_COPY command - copies and places (optionally) text into variable
class Win32_Copy(Command_Win32):
    def __init__(
        self,
        ): 
        
        super().__init__("W_COPY",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val 
            ("Clipboard",  True,  AVV_REQD, PT_TEXT, None,                       None),   # variable to contain cut item
            ),
            (
            # num params, format string                           (trailing comma is important)
            (0,           "    Copy into system clipboard"), 
            (1,           "    Copy into system clipboard and {1}"), 
            ) )
            
    def Process(self, btn, idx, split_line):
    
        hwnd = win32gui.GetForegroundWindow()                  # get the current window
        
        try:                                                   # clear the clipboard
            win32clipboard.OpenClipboard(hwnd)
            win32clipboard.EmptyClipboard()
        finally:
            win32clipboard.CloseClipboard()
        
        try:                                                   # do the keyboard stuff for copy (sending a WM_COPY message does not always work)
            kb.press(kb.sp('ctrl'))        
            kb.tap(kb.sp('c'))   
        finally:
            kb.release(kb.sp('ctrl'))        
        #win32api.SendMessage(hwnd, win32con.WM_COPYDATA, 0, 0) # do a copy
        
        if self.Param_count(btn) > 0:                          # save to variable if required
            try:
                win32clipboard.OpenClipboard(hwnd)               
                t = win32clipboard.GetClipboardData(win32con.CF_TEXT)
                self.Set_param(btn, 1, t)
            finally:
                win32clipboard.CloseClipboard()


scripts.Add_command(Win32_Copy())  # register the command


# ##################################################
# ### CLASS W_PASTE                              ###
# ##################################################

# class that defines the W_Paste command - copies and places (optionally) text into variable
class Win32_Paste(Command_Win32):
    def __init__(
        self,
        ): 
        
        super().__init__("W_PASTE",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val 
            ("Clipboard",  True,  AVV_REQD, PT_TEXT, None,                       None),   # variable to contain item to paste
            ),
            (
            # num params, format string                           (trailing comma is important)
            (0,           "    Paste from system clipboard"), 
            (1,           "    Paste from {1} via system clipboard"), 
            ) )
            
    def Process(self, btn, idx, split_line):
    
        if self.Param_count(btn) > 0:                          # place variable into clipboard if required
            hwnd = win32gui.GetForegroundWindow()              # get the current window
      
            c = self.Get_param(btn, 1)                         # get the value
            try:
                win32clipboard.OpenClipboard(hwnd)  
                win32clipboard.EmptyClipboard()                # clear the clipboard first (because that makes it work)
                win32clipboard.SetClipboardText(str(c))        # and put the string in the clipboard
            finally:
                win32clipboard.CloseClipboard()
        
        # win32api.SendMessage(hwnd, win32con.WM_PASTE, 0, 0)  # do a paste  
        try:
            kb.press(kb.sp('ctrl'))                            # do a ctrl v (because the message version isn't reliable)
            kb.tap(kb.sp('v'))   
        finally:
            kb.release(kb.sp('ctrl'))        


scripts.Add_command(Win32_Paste())  # register the command


# ##################################################
# ### CLASS W_WAIT                               ###
# ##################################################

# class that defines the W_WAIT command - waits until the process for a window handle is ready for input
class Win32_Wait(Command_Win32):
    def __init__(
        self,
        ): 
        
        super().__init__("W_WAIT",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val 
            ("HWND",       False, AVV_YES,  PT_INT,  None,                       None),   # variable to contain item to paste
            ),
            (
            # num params, format string                           (trailing comma is important)
            (0,           "    Wait until {1} is ready for input"), 
            ) )
            
    def Process(self, btn, idx, split_line):
    
        hwnd = self.Get_param(btn, 1)                          # get the window
        tid, pid = win32process.GetWindowThreadProcessId(hwnd) # find the pid
        hproc = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION , False, pid) # find the process id
        
        res = win32con.WAIT_TIMEOUT
        while res == win32con.WAIT_TIMEOUT:
            res = win32event.WaitForInputIdle(hproc, 20)
            if btn.Check_kill():
                return False


scripts.Add_command(Win32_Wait())  # register the command
