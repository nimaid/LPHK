# This module contains commands that work on the filesystem
import os, command_base, ms, kb, scripts, traceback, pathlib, files
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

        self.doc = ["Returns the filly qualified path of the user's home directory."]


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

        super().__init__("F_DELETE, Deletes a file",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("OK",         False, AVV_REQD, PT_INT,  None,                       None),
            ("File",       False, AVV_YES,  PT_STR,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2,           "    Deletes {1}"),
            ) )

        self.doc = ["Attempts to delete the file specified in parameter 2 (File) and returns 1 "
                    "in parameter 1 (OK) if the delete suceeds, otherwise returns 0.  Note that "
                    "0 will be returned if the file did not exist prior to attempted deletion"]


    def Process(self, btn, idx, split_line):
        file = self.Get_param(btn, 2)
        try:
            os.remove(file)           # delete the file
            self.Set_param(btn, 1, 1)
        except:
            traceback.print_exc()
            self.Set_param(btn, 1, 0)

scripts.Add_command(File_Delete())  # register the command


# ##################################################
# ### CLASS FILE_FILE_EXISTS                     ###
# ##################################################

# class that defines the F_FILE_EXISTS command -- confirms the existance of a file
class File_File_Exists(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("F_FILE_EXISTS, Determines if a file exists",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("Exists",     False, AVV_REQD, PT_INT,  None,                       None),
            ("File",       False, AVV_YES,  PT_STR,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2,           "    Returns 1 in {1} if {2} exists as a file, else returns 0"),
            ) )

        self.doc = ["Returns 1 in parameter 1 (Exists) if the fully specified file (includes path) "
                    "passed in parameter 2 (File) exists AND is a file, otherwise returns 0."]


    def Process(self, btn, idx, split_line):
        file = self.Get_param(btn, 2)
        try:
            self.Set_param(btn, 1, int(os.path.exists(file) and os.path.isfile(file))) # Check existance of file
        except:
            traceback.print_exc()

scripts.Add_command(File_File_Exists())  # register the command


# ##################################################
# ### CLASS FILE_PATH_EXISTS                     ###
# ##################################################

# class that defines the F_PATH_EXISTS command -- confirms the existance of a file
class File_Path_Exists(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("F_PATH_EXISTS, Determines if a path exists",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("Exists",     False, AVV_REQD, PT_INT,  None,                       None),
            ("Path",       False, AVV_YES,  PT_STR,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2,           "    Returns 1 in {1} if {2} exists as a path, else returns 0"),
            ) )

        self.doc = ["Returns 1 in parameter 1 (Exists) if the path specified in parameter "
                    "2 (Path) exists AND is a directory, otherwise returns 0."]


    def Process(self, btn, idx, split_line):
        path = self.Get_param(btn, 2)
        try:
            self.Set_param(btn, 1, int(os.path.exists(path) and os.path.isdir(file)))    # Check existance of path
        except:
            traceback.print_exc()

scripts.Add_command(File_Path_Exists())  # register the command


# ##################################################
# ### CLASS FILE_ENSURE_PATH_EXISTS              ###
# ##################################################

# class that defines the F_ENSURE_PATH_EXISTS command -- checks for the existance of a path, creating it if necessary
class File_Ensure_Path_Exists(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("F_ENSURE_PATH_EXISTS, Ensures a path exists by creating it if it doesn't",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("OK",         False, AVV_REQD, PT_INT,  None,                       None),
            ("Path",       False, AVV_YES,  PT_STR,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2,           "    Returns 1 in {1} if {2} exists as a path (or could be created), else returns 0"),
            ) )

        self.doc = ["Ensures the path passed exists by first checking for its existance, then "
                    "attempting to create the path if it does not exist.",
                    "",
                    "Returns 1 in the first parameter (OK) if the path existed or was "
                    "sucessfully created, otherwise returns 0."]


    def Process(self, btn, idx, split_line):
        path = self.Get_param(btn, 2)
        ok = 0
        try:
            if not os.path.exists(path):          # if it doesn't exist
                os.makedirs(path)                 # make it exist
            ok = 1                                # success!
        except:
            traceback.print_exc()

        self.Set_param(btn, 1, ok)


scripts.Add_command(File_Ensure_Path_Exists())    # register the command


# ##################################################
# ### CLASS File_Load_Layout                     ###
# ##################################################

# constants for LOAD_LAYOUT
LL_NORMAL    = "NORMAL"
LL_FAST      = "FAST"
LL_UNCHECKED = "UNCHECKED"

LLG_ALL = [LL_NORMAL, LL_FAST, LL_UNCHECKED]

# Loads a new layout.  Command rather than header format (doesn't have the F_ prefix for historical reasons)
class File_Load_Layout(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("LOAD_LAYOUT, Loads a new layout",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("Layout",     False, AVV_YES,  PT_STR,  None,                       None),
            ("Method",     True,  AVV_NO,   PT_WORD, None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (1,           "    loads layout {1}"),
            (2,           "    loads layout {1} with option {2}"),
            ) )

        self.doc = ["Replaces the current layout with a new one loaded from a layout file."]


    def Process(self, btn, idx, split_line):
        layout_name = self.Get_param(btn, 1)
        method = self.Get_param(btn, 2, LL_NORMAL)

        layout_path = os.path.join(files.LAYOUT_PATH, layout_name)
        if not os.path.isfile(layout_path):
            print("[cmds_head] " + coords + "  Line:" + str(idx+1) + "        ERROR: Layout file does not exist.")
            return -1

        try:
            layout = files.load_layout(layout_path, popups=False, save_converted=False)
        except files.json.decoder.JSONDecodeError:
            print("[cmds_head] " + coords + "  Line:" + str(idx+1) + "        ERROR: Layout is malformated.")
            return -1

        if files.layout_changed_since_load:
            files.save_lp_to_layout(files.curr_layout)

        if method == LL_NORMAL:
            files.load_layout_to_lp(layout_path, popups=False, save_converted=False, preload=layout)
        elif method == LL_FAST:
            files.load_layout_to_lp(layout_path, popups=False, save_converted=False, preload=layout, load_subroutines=False)
        elif method == LL_UNCHECKED:
            files.load_layout_to_lp(layout_path, popups=False, save_converted=False, preload=layout, load_subroutines=False, check_subroutines=False)

        return idx+1


    def Partial_validate_step_pass_1(self, ret, btn, idx, split_line):
        ret = super().Partial_validate_step_pass_1(ret, btn, idx, split_line)     # perform the original pass 1 validation

        if ret == None or ((type(ret) == bool) and ret):                          # if the original validation hasn't raised an error
            if (len(split_line) > 2) and (not split_line[2] in LLG_ALL):          # invalid subcommand
                c_ok = ', '.join(LLG_ALL[:-1]) + ', or ' + LLG_ALL[-1]
                s_err = f"Invalid subcommand {split_line[1]} when expecting {c_ok}."
                return (s_err, btn.Line(idx))
        return ret


scripts.Add_command(File_Load_Layout())  # register the header


