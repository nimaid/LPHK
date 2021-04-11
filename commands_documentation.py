import command_base, commands_header, scripts, variables
from constants import *

LIB = "cmds_docs" # name of this library (for logging)

# ##################################################
# ### CLASS DOC_DOCUMENT                         ###
# ##################################################

# constants for DOC_DOCUMENT
DD_HEADERS       = "HEADERS"
DD_COMMANDS      = "COMMANDS"
DD_SUBROUTINES   = "SUBROUTINES"
DD_BUTTONS       = "BUTTONS"
DD_COMMAND_BASE  = "COMMAND_BASE"
DD_DEBUG         = "DEBUG"
DD_SOURCE        = "SOURCE"

DDG_ALL = [DD_HEADERS, DD_COMMANDS, DD_SUBROUTINES, DD_BUTTONS, DD_COMMAND_BASE, DD_DEBUG, DD_SOURCE]
DDG_DEFAULT = [DD_HEADERS, DD_COMMANDS, DD_SUBROUTINES, DD_BUTTONS]

# class that defines more the DOCUMENT command that outputs documentation
class DOC_Document(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("DOCUMENT, Produce documentation on LPHK",
            LIB,
            (
            # Desc            Opt    Var      type      p1_val p2_val
            ("Method",        True,  AVV_NO,  PT_WORDS, None,  None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (0,           "    Dump headers and commands"),
            ) )


        self.doc = ["Prints documentation about LPHK to standard output."
                    ""
                    "Any number of valid parameters can be passed.  These can be a",
                    "combination of 'category' parameters (that define the subset(s)",
                    "of documentation to be printed, and 'modifier' parameters that",
                    "alter how the documentation is produced.",
                    "",
                    "If no parameters are passed, a standard output is produced.  If",
                    "the only parameters passed are 'modifier' parameters, they modify",
                    "the standard output.",
                    "",
                    "The `category` parameters cause documentation to be created for:",
                    "      HEADERS      - commands starting with '@' used in scripts.",
                    "      COMMANDS     - regular macro commands",
                    "      SUBROUTINES  - user-defined subroutines",
                    "      BUTTONS      - button scripts",
                    "      COMMAND_BASE - (not yet implemented) routines used when writing commands",
                    "",
                    "The `modifier` parameters change the way documentation is produced:",
                    "      DEBUG        - includes type ancestory for commands.",
                    "      SOURCE       - includes source for buttons and subroutines",
                    "",
                    "The default categories are HEADERS COMMANDS SUBROUTINES BUTTONS"]


    def Process(self, btn, idx, split_line):
        doc_set = []

        for i in range(self.Param_count(btn)):
            p = self.Get_param(btn, i+1)             # For each parameter

            doc_set = []                             # start with nothing to request documentation on

            if p == DD_HEADERS:                      # add requestsa as per the parameters
                doc_set += [D_HEADERS]
            elif p == DD_COMMANDS:
                doc_set += [D_COMMANDS]
            elif p == DD_SUBROUTINES:
                doc_set += [D_SUBROUTINES]
            elif p == DD_BUTTONS:
                doc_set += [D_BUTTONS]
            elif p == DD_COMMAND_BASE:
                doc_set += [D_COMMAND_BASE]
            elif p == DD_DEBUG:
                doc_set += [D_DEBUG]
            elif p == DD_SOURCE:
                doc_set += [D_SOURCE]

        if (set(doc_set) - {D_DEBUG, D_SOURCE}) == set({}): # if only modifiers have been specified
            doc_set = DS_NORMAL + doc_set            # add them to teh "normal" documentation

        scripts.Dump_commands(doc_set)               # print documentation


    def Partial_validate_step_pass_1(self, ret, btn, idx, split_line):
        ret = super().Partial_validate_step_pass_1(ret, btn, idx, split_line)     # perform the original pass 1 validation

        if ret == None or ((type(ret) == bool) and ret):                          # if the original validation hasn't raised an error
            for i in range(len(split_line)-1):
                if not split_line[i+1] in DDG_ALL:                                # invalid subcommand
                    c_ok = ', '.join(DDG_ALL[:-1]) + ', or ' + DDG_ALL[-1]
                    s_err = f"Invalid subcommand {split_line[i+1]} when expecting {c_ok}."
                    return (s_err, btn.Line(idx))
        return ret


scripts.Add_command(DOC_Document())  # register the command
