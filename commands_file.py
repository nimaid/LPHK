# This module contains commands that work on the filesystem
import os, command_base, ms, kb, scripts, traceback, pathlib
from constants import *

LIB = "cmds_file" # name of this library (for logging)

# ##################################################
# ### CLASS FILE_HOME                            ###
# ##################################################

# class that defines the F_HOME command -- returns the user's home directory
class File_Home(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("F_HOME, Returns the user's home directory",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("Home",       False, AVV_REQD, PT_STR,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (1,           "    returns user's home dir in {1}"),
            ) )


    def Process(self, btn, idx, split_line):
        self.Set_param(btn, 1, pathlib.Path.home())                     # return the path


scripts.Add_command(File_Home())  # register the command


# ##################################################
# ### CLASS FILE_DELETE                          ###
# ##################################################

# class that defines the F_DEL command -- deletes a file
class File_Delete(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("F_DEL, Returns the user's home directory",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("File",       False, AVV_YES,  PT_STR,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (1,           "    Deletes {1}"),
            ) )


    def Process(self, btn, idx, split_line):
        file = self.Get_param(btn, 1)
        try:
            os.remove(self.Get_param(btn, 1, file))           # delete the file
        except:
            traceback.print_exc()

scripts.Add_command(File_Delete())  # register the command


