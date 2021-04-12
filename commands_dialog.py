import command_base, commands_header, scripts, dialog
from constants import *

LIB = "cmds_dlgs" # name of this library (for logging)


# ##################################################
# ### CLASS DIALOG_OK_CANCEL                     ###
# ##################################################

# class that defines the OK Cancel dialog command
class Dialog_Ok_Cancel(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("DIALOG_OK_CANCEL, A simple OK/Cancel dialog",
            LIB,
            (
            # Desc            Opt    Var      type     p1_val p2_val
            ("Title",         False, AVV_YES, PT_STR,  None,  None),
            ("Message",       False, AVV_YES, PT_STR,  None,  None),
            ("Return",        True,  AVV_REQD,PT_INT,  None,  None),
            ),
            (                          # How to log runtime execution
            # num params, format string                           (trailing comma is important)
            (2,           "    Dialog OK/Cancel '{1}' - abort on cancel"),
            (3,           "    Dialog OK/Cancel '{1}'"),
            ) )

        self.doc = ["A simple dialog with a title, message and OK/Cancel buttons.  Closing the "
                    "window is treated the same as cancel.  If a return variable is specified, "
                    "contain 1 for OK, and 0 for cancel.  If no variable is passed for the "
                    "return value, a cancel will result in a button abort."]


    def Process(self, btn, idx, split_line):
        ret = dialog.QueuedDialog(btn, DLG_OK_CANCEL, (self.Get_param(btn, 1), self.Get_param(btn, 2))) # Call the dialog and get the return value
        try:
            rval = ret[1][1]                                                 # this will get the return value if everything worked

        except:
            rval = dialog.DR_ABORT                                           # otherwise we'll substitute an abort code

        if rval == dialog.DR_OK:                                             # if we got OK
            self.Set_param(btn, 3, dialog.DR_OK)                             # set the return value to OK (if we can)
        elif self.Param_count(btn) == 3:                                     # otherwise, if there were 3 parameters
            self.Set_param(btn, 3, dialog.DR_CANCEL)                         # return cancel
        else:                                                                # if only 1 parameter and no return parameter
            btn.root.thread.kill.set()                                       # then kill the thread
            return -1


scripts.Add_command(Dialog_Ok_Cancel())  # register the command


# ##################################################
# ### CLASS DIALOG_INFO                          ###
# ##################################################

# class that defines an info dialog command
class Dialog_Info(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("DIALOG_INFO, A simple informational dialog",
            LIB,
            (
            # Desc            Opt    Var      type     p1_val p2_val
            ("Title",         False, AVV_YES, PT_STR,  None,  None),
            ("Message",       False, AVV_YES, PT_STR,  None,  None),
            ),
            (                          # How to log runtime execution
            # num params, format string                           (trailing comma is important)
            (2,           "    Info dialog '{1}'"),
            ) )

        self.doc = ["A simple dialog with a title, message and OK button.  No return value "
                    "is required since the message only requires acknowledgement.  This "
                    "will never cause an abort"]


    def Process(self, btn, idx, split_line):
        ret = dialog.QueuedDialog(btn, DLG_INFO, (self.Get_param(btn, 1), self.Get_param(btn, 2))) # Call the dialog


scripts.Add_command(Dialog_Info())  # register the command

# ##################################################
# ### CLASS DIALOG_ERROR                         ###
# ##################################################

# class that defines an error dialog command
class Dialog_Error(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("DIALOG_ERROR, A simple error dialog",
            LIB,
            (
            # Desc            Opt    Var      type     p1_val p2_val
            ("Title",         False, AVV_YES, PT_STR,  None,  None),
            ("Message",       False, AVV_YES, PT_STR,  None,  None),
            ("Return",        True,  AVV_REQD,PT_INT,  None,  None),
            ),
            (                          # How to log runtime execution
            # num params, format string                           (trailing comma is important)
            (2,           "    Error dialog '{1}'"),
            (3,           "    Error dialog '{1}' returning {3}"),
            ) )

        self.doc = ["A simple dialog with a title, message and Cancel button.  Typically "
                    "this should be called without a return variable to allow the script "
                    "to abort.  If a return value is specified, the script will continue "
                    "after the dialog is dismissed."]


    def Process(self, btn, idx, split_line):
        ret = dialog.QueuedDialog(btn, DLG_ERROR, (self.Get_param(btn, 1), self.Get_param(btn, 2))) # Call the dialog
        if self.Param_count(btn) == 2:
            btn.root.thread.kill.set()                                       # then kill the thread
            return -1



scripts.Add_command(Dialog_Error())  # register the command
