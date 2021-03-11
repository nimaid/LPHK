import command_base, scripts

lib = "cmds_paus" # name of this library (for logging)

# ##################################################
# ### CLASS Pause_Delay                          ###
# ##################################################

# class that defines the Delay command (a target of GOTO's etc)
class Pause_Delay(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("DELAY")  # the name of the command as you have to enter it in the code

    def Validate(
        self,
        btn,
        idx: int,              # The current line number
        split_line,            # The current line, split
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:
            # check number of split_line
            if len(split_line) < 2:
                return ("Line:" + str(idx+1) + " - Too few arguments for command '" + split_line[0] + "'.", btn.Line(idx))

            if len(split_line) > 2:
                return ("Line:" + str(idx+1) + " - Too many arguments for command '" + split_line[0] + "'.", btn.Line(idx))

            try:
                temp = float(split_line[1])
            except:
                return ("Line:" + str(idx+1) + " - Delay time '" + split_line[1] + "' not valid.", btn.Line(idx))

        return True


    def Run(
        self,
        btn,
        idx: int,              # The current line number
        split_line             # The current line, split
        ):

        print("[" + lib + "] " + btn.coords + "  Line:" + str(idx+1) + "    Delay for " + split_line[1] + " seconds")

        delay = float(split_line[1])

        if not btn.Safe_sleep(delay):
            return -1

        return idx+1


scripts.Add_command(Pause_Delay())  # register the command



