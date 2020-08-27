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
        idx: int,              # The current line number
        line,                  # The current line
        lines,                 # The current script
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
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
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + lib + "] " + coords[0] + "    Delay for " + split_line[1] + " seconds")

        delay = float(split_line[1])

        if not safe_sleep(delay, coords[1], coords[2], is_async):
            return -1

        return idx+1


scripts.add_command(Pause_Delay())  # register the command



