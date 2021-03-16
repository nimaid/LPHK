# This module is VERY specific to Win32
import command_base, scripts, traceback
from selenium import webdriver
from constants import *

LIB = "cmds_baut" # name of this library (for logging)

# ##################################################
# ### CLASS BAUTO_START                          ###
# ##################################################

# class that defines the BA_START command that starts a browser under automated control
class Bauto_Start(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("BA_START, Starts a browser under automated control",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("Browser",    False, AVV_NO,   PT_WORD, None,                       None),
            ("Auto",       False, AVV_REQD, PT_OBJ,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2,           "    Open browser {1} for automation as {2}"),
            ) )

        self.doc = ["Starts a browser using selinium for automated control.  The return will",
                    "be an object if the call suceeds, otherwise it will return 0"]


    def Process(self, btn, idx, split_line):
        br = self.Get_param(btn, 1)
        try:
            auto = webdriver.Chrome()
        except:
            traceback.print_exc()
            auto = 0
            
        self.Set_param(btn, 2, auto)                                 # pass the object back


scripts.Add_command(Bauto_Start())  # register the command


# ##################################################
# ### CLASS BAUTO_NAVIGATE                       ###
# ##################################################

# class that defines the BA_NAVIGATE command navigates the browser to a particular page
class Bauto_Navigate(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("BA_NAVIGATE, Starts a browser under automated control",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("Auto",       False, AVV_REQD, PT_OBJ,  None,                       None),
            ("URL",        False, AVV_YES,  PT_STR,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2,           "    Navigate browser to {2}"),
            ) )


    def Process(self, btn, idx, split_line):
        auto = self.Get_param(btn, 1)
        url = self.Get_param(btn, 2)
        try:
            auto.get(url)
        except:
            traceback.print_exc()
            auto = 0


scripts.Add_command(Bauto_Navigate())  # register the command


# ##################################################
# ### CLASS BAUTO_STOP                           ###
# ##################################################

# class that defines the BA_STOP command to close the browser
class Bauto_Stop(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("BA_STOP, Stops the browser under automated control",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("Auto",       False, AVV_REQD, PT_OBJ,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (1,           "    Stop browser {1}"),
            ) )


    def Process(self, btn, idx, split_line):
        auto = self.Get_param(btn, 1)
        try:
            auto.quit()
        except:
            traceback.print_exc()
            auto = 0


scripts.Add_command(Bauto_Stop())  # register the command


