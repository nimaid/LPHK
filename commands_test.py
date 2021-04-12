import command_base, commands_header, scripts, variables
from constants import *

LIB = "cmds_test" # name of this library (for logging)

class Test_XX(command_base.Command_Basic):

    def clean(self, s): # remove stuff that changes (memory addresses)
        p = s.find(" at 0x")
        if p >=0:
            s = self.clean(s[:p] + s[p+22:])
        return s


    def Process(self, btn, idx, split_line):
        print("============================START")
        print("=", self.name, split_line)
        print("=", self.clean(f"{self.auto_validate}"))
        before = self.clean(f"{btn.symbols}")
        print("=", f"Symbols before = {before}")
        a = self.Get_param(btn, 1)
        print("=", f"Param = '{a}', {type(a)}")
        for i in range(2,self.Param_count(btn)+1):
            _a = self.Get_param(btn, i)
            print("=", f"Param = '{_a}', {type(_a)}")
        if a != None:
            print("=", f"adding = '{self.one}', {type(self.one)}")
            a += self.one
        self.Set_param(btn, 1, a)
        print("=", f"Modified param = '{a}', {type(a)}")
        after = self.clean(f"{btn.symbols}")
        print("=", f"Symbols after  = {after}")
        if before == after:
            print("= No change to stack")
        else:
            print("= STACK CHANGED")
        print("============================END")


class Test_01(Test_XX):
    def __init__(
        self,
        ):

        super().__init__("TEST_01, Test for single optional integer constant parameter",
            LIB,
            (
            # Desc            Opt    Var      type     p1_val p2_val
            ("Param_1",       True,  AVV_NO,  PT_INT,  None,  None),
            ),
            (                          # How to log runtime execution
            # num params, format string                           (trailing comma is important)
            (1,           "    Param {1}"),
            ) )

        self.one = 1
        self.deprecated = True
        self.deprecated_use = "This command exists for testing purposes and will not exist in the production version of LPHK."

scripts.Add_command(Test_01())  # register the command


class Test_02(Test_XX):
    def __init__(
        self,
        ):

        super().__init__("TEST_02, Test for single optional float constant parameter",
            LIB,
            (
            # Desc            Opt    Var      type      p1_val p2_val
            ("Param_1",       True,  AVV_NO,  PT_FLOAT, None,  None),
            ),
            (                          # How to log runtime execution
            # num params, format string                           (trailing comma is important)
            (1,           "    Param {1}"),
            ) )

        self.one = 1
        self.deprecated = True
        self.deprecated_use = "This command exists for testing purposes and will not exist in the production version of LPHK."


scripts.Add_command(Test_02())  # register the command


class Test_03(Test_XX):
    def __init__(
        self,
        ):

        super().__init__("TEST_03, Test for single optional string constant parameter",
            LIB,
            (
            # Desc            Opt    Var      type      p1_val p2_val
            ("Param_1",       True,  AVV_NO,  PT_STR,   None,  None),
            ),
            (                          # How to log runtime execution
            # num params, format string                           (trailing comma is important)
            (1,           "    Param {1}"),
            ) )

        self.one = "1"
        self.deprecated = True
        self.deprecated_use = "This command exists for testing purposes and will not exist in the production version of LPHK."


scripts.Add_command(Test_03())  # register the command


class Test_04(Test_XX):
    def __init__(
        self,
        ):

        super().__init__("TEST_04, Test for single optional multi-string constant parameter",
            LIB,
            (
            # Desc            Opt    Var      type      p1_val p2_val
            ("Param_1",       True,  AVV_NO,  PT_STRS,  None,  None),
            ),
            (                          # How to log runtime execution
            # num params, format string                           (trailing comma is important)
            (1,           "    Param {1}"),
            ) )

        self.one = "1"
        self.deprecated = True
        self.deprecated_use = "This command exists for testing purposes and will not exist in the production version of LPHK."


scripts.Add_command(Test_04())  # register the command


class Test_11(Test_XX):
    def __init__(
        self,
        ):

        super().__init__("TEST_11, Test for single optional integer constant/variable parameter",
            LIB,
            (
            # Desc            Opt    Var      type     p1_val p2_val
            ("Param_1",       True,  AVV_YES, PT_INT,  None,  None),
            ),
            (                          # How to log runtime execution
            # num params, format string                           (trailing comma is important)
            (1,           "    Param {1}"),
            ) )

        self.one = 1
        self.deprecated = True
        self.deprecated_use = "This command exists for testing purposes and will not exist in the production version of LPHK."


scripts.Add_command(Test_11())  # register the command


class Test_12(Test_XX):
    def __init__(
        self,
        ):

        super().__init__("TEST_12, Test for single optional float constant/variable parameter",
            LIB,
            (
            # Desc            Opt    Var      type      p1_val p2_val
            ("Param_1",       True,  AVV_YES, PT_FLOAT, None,  None),
            ),
            (                          # How to log runtime execution
            # num params, format string                           (trailing comma is important)
            (1,           "    Param {1}"),
            ) )

        self.one = 1
        self.deprecated = True
        self.deprecated_use = "This command exists for testing purposes and will not exist in the production version of LPHK."


scripts.Add_command(Test_12())  # register the command


class Test_13(Test_XX):
    def __init__(
        self,
        ):

        super().__init__("TEST_13, Test for single optional string constant/variable parameter",
            LIB,
            (
            # Desc            Opt    Var      type      p1_val p2_val
            ("Param_1",       True,  AVV_YES, PT_STR,   None,  None),
            ),
            (                          # How to log runtime execution
            # num params, format string                           (trailing comma is important)
            (1,           "    Param {1}"),
            ) )

        self.one = "1"
        self.deprecated = True
        self.deprecated_use = "This command exists for testing purposes and will not exist in the production version of LPHK."


scripts.Add_command(Test_13())  # register the command


class Test_14(Test_XX):
    def __init__(
        self,
        ):

        super().__init__("TEST_14, Test for single optional multi-string constant/variable parameter",
            LIB,
            (
            # Desc            Opt    Var      type      p1_val p2_val
            ("Param_1",       True,  AVV_YES, PT_STRS,  None,  None),
            ),
            (                          # How to log runtime execution
            # num params, format string                           (trailing comma is important)
            (1,           "    Param {1}"),
            ) )

        self.one = "1"
        self.deprecated = True
        self.deprecated_use = "This command exists for testing purposes and will not exist in the production version of LPHK."


scripts.Add_command(Test_14())  # register the command


class Test_21(Test_XX):
    def __init__(
        self,
        ):

        super().__init__("TEST_21, Test for single optional integer by-ref parameter",
            LIB,
            (
            # Desc            Opt    Var      type     p1_val p2_val
            ("Param_1",       True,  AVV_REQD,PT_INT,  None,  None),
            ),
            (                          # How to log runtime execution
            # num params, format string                           (trailing comma is important)
            (1,           "    Param {1}"),
            ) )

        self.one = 1
        self.deprecated = True
        self.deprecated_use = "This command exists for testing purposes and will not exist in the production version of LPHK."


scripts.Add_command(Test_21())  # register the command


class Test_22(Test_XX):
    def __init__(
        self,
        ):

        super().__init__("TEST_22, Test for single optional float by-ref parameter",
            LIB,
            (
            # Desc            Opt    Var      type      p1_val p2_val
            ("Param_1",       True,  AVV_REQD,PT_FLOAT, None,  None),
            ),
            (                          # How to log runtime execution
            # num params, format string                           (trailing comma is important)
            (1,           "    Param {1}"),
            ) )

        self.one = 1
        self.deprecated = True
        self.deprecated_use = "This command exists for testing purposes and will not exist in the production version of LPHK."


scripts.Add_command(Test_22())  # register the command


class Test_23(Test_XX):
    def __init__(
        self,
        ):

        super().__init__("TEST_23, Test for single optional string by-ref parameter",
            LIB,
            (
            # Desc            Opt    Var      type      p1_val p2_val
            ("Param_1",       True,  AVV_REQD,PT_STR,   None,  None),
            ),
            (                          # How to log runtime execution
            # num params, format string                           (trailing comma is important)
            (1,           "    Param {1}"),
            ) )

        self.one = "1"
        self.deprecated = True
        self.deprecated_use = "This command exists for testing purposes and will not exist in the production version of LPHK."


scripts.Add_command(Test_23())  # register the command


class Test_24(Test_XX):
    def __init__(
        self,
        ):

        super().__init__("TEST_24, Test for single optional multi-string by-ref parameter",
            LIB,
            (
            # Desc            Opt    Var      type      p1_val p2_val
            ("Param_1",       True,  AVV_REQD,PT_STRS,  None,  None),
            ),
            (                          # How to log runtime execution
            # num params, format string                           (trailing comma is important)
            (1,           "    Param {1}"),
            ) )

        self.one = "1"
        self.deprecated = True
        self.deprecated_use = "This command exists for testing purposes and will not exist in the production version of LPHK."


scripts.Add_command(Test_24())  # register the command


class Test_101(Test_XX):
    def __init__(
        self,
        ):

        super().__init__("TEST_101, Test for single required string followed by an optional integer",
            LIB,
            (
            # Desc            Opt    Var      type      p1_val p2_val
            ("Param_1",       False, AVV_YES, PT_STR,   None,  None),
            ("Param_2",       True,  AVV_REQD,PT_INT,   None,  None),
            ),
            (                          # How to log runtime execution
            # num params, format string                           (trailing comma is important)
            (1,           "    Param {1}"),
            ) )

        self.one = "1"
        self.deprecated = True
        self.deprecated_use = "This command exists for testing purposes and will not exist in the production version of LPHK."


scripts.Add_command(Test_101())  # register the command


# class that defines the Delay command (a target of GOTO's etc)
class Test_Dialog(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("TEST_DIALOG, Test to display a simple dialog",
            LIB,
            (
            # Desc            Opt    Var      type     p1_val p2_val
            ),
            (                          # How to log runtime execution
            # num params, format string                           (trailing comma is important)
            (0,           "    Dialog Test"),
            ) )

        self.deprecated = True
        self.deprecated_use = "This command will not exist in the production version of LPHK.  Please use one of the `DIALOG_` commands."


    def Process(self, btn, idx, split_line):
        import dialog
        ret = dialog.CommentBox(btn, "this is a test")


scripts.Add_command(Test_Dialog())  # register the command


# class that dumps all known commands
class Test_Dump(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("TEST_DUMP, Dump all headers and commands",
            LIB,
            (
            # Desc            Opt    Var      type     p1_val p2_val
            ),
            (                          # How to log runtime execution
            # num params, format string                           (trailing comma is important)
            (0,           "    Dump headers and commands"),
            ) )

        self.deprecated = True
        self.deprecated_use = "This command will not exist in the production version of LPHK.  Please use the `DOCUMENT` command."


    def Process(self, btn, idx, split_line):
        scripts.Dump_commands()


scripts.Add_command(Test_Dump())  # register the command


# class that dumps all known commands
class Test_Dump_Debug(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("TEST_DUMP_DEBUG, Dump all headers and commands with ancestory",
            LIB,
            (
            # Desc            Opt    Var      type     p1_val p2_val
            ),
            (                          # How to log runtime execution
            # num params, format string                           (trailing comma is important)
            (0,           "    Dump headers and commands"),
            ) )

        self.deprecated = True
        self.deprecated_use = "This command will not exist in the production version of LPHK.  Please use the `DOCUMENT` command."


    def Process(self, btn, idx, split_line):
        scripts.Dump_commands(DS_NORMAL + [D_DEBUG])


scripts.Add_command(Test_Dump_Debug())  # register the command
