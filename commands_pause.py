import command_base, scripts


# ##################################################
# ### CLASS Pause_Delay                          ###
# ##################################################

# class that defines the Delay command (a target of GOTO's etc)
class Pause_Delay(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("DELAY")

    def Validate(
        self,
        idx: int,
        line,
        lines,
        split_line,
        symbols,
        pass_no
        ):

        if pass_no == 1:
            # check number of split_line
            if len(split_line) < 2:
                return ("Too few arguments for command '" + split_line[0] + "'.", line)

            if len(split_line) > 2:
                return ("Too many arguments for command '" + split_line[0] + "'.", line)

            try:
                temp = float(split_line[1])
            except:
                return ("Delay time '" + split_line[1] + "' not valid.", line)

        return True


    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        print("[cmds_paus] " + coords[0] + "    Delay for " + split_line[1] + " seconds")

        delay = float(split_line[1])

        if not safe_sleep(delay, coords[1], coords[2], is_async):
            return -1

        return idx+1


scripts.add_command(Pause_Delay())


