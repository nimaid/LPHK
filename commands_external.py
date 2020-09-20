import command_base, webbrowser, sound, subprocess, os, scripts
from constants import *

LIB = "cmds_extn" # name of this library (for logging)

# ##################################################
# ### CLASS External_Web                         ###
# ##################################################

# class that defines the WEB command 
class External_Web(command_base.Command_Text_Basic):
    def __init__(
        self, 
        ):

        super().__init__(
            "WEB",  # the name of the command as you have to enter it in the code
            LIB,
            "    Open website '{1}' in default browser"
            )

        self.valid_num_params = [1]  # one or more is OK


    def Partial_run_step_get(self, ret, btn, idx, split_line):
        # This gets the values as normal, then modifies them as required
        ret = super().Partial_run_step_get(ret, btn, idx, split_line)
        
        link = split_line[1]
        if "http" not in link:
            split_line[1] = "http://" + link        
        
        return ret


    def Process(self, btn, idx, split_line):
        webbrowser.open(btn.symbols[SYM_PARAMS][1])


scripts.Add_command(External_Web())  # register the command


# ##################################################
# ### CLASS External_Web_New                     ###
# ##################################################

# class that defines the WEB_NEW command 
class External_Web_New(External_Web):
    def __init__(
        self, 
        ):

        super().__init__()

        self.name = "WEB_NEW"  # the name of the command as you have to enter it in the code
        self.info_msg = "    Open website '{1}' in a new browser"


    def Process(self, btn, idx, split_line):
        webbrowser.open_new(btn.symbols[SYM_PARAMS][1])


scripts.Add_command(External_Web_New())  # register the command


# ##################################################
# ### CLASS External_Open                        ###
# ##################################################

# class that defines the OPEN command 
class External_Open(command_base.Command_Text_Basic):
    def __init__(
        self, 
        ):

        super().__init__(
            "OPEN",  # the name of the command as you have to enter it in the code
            LIB,
            "    Open file or location '{1}'"
            )

        self.valid_num_params = [1]  # one or more is OK


    def Process(self, btn, idx, split_line):
        files.open_file_folder(btn.symbols[SYM_PARAMS][1])


scripts.Add_command(External_Open())  # register the command


# ##################################################
# ### CLASS External_Sound                       ###
# ##################################################

# class that defines the SOUND command (plays a sound file) 
class External_Sound(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("SOUND")  # the name of the command as you have to enter it in the code

    def Validate(
        self,
        btn,
        idx: int,              # The current line number
        split_line,            # The current line, split
        ):

        if pass_no == 1:       # in Pass 1 we can do general syntax check and gather symbol definitions
            if len(split_line) < 2:
                return ("Line:" + str(idx+1) + " - Too few arguments for command '" + split_line[0] + "'.", btn.line[idx])

            if len(split_line) > 3:
                return ("Line:" + str(idx+1) + " - Too many arguments for command '" + split_line[0] + "'.", btn.line[idx])

        return True

    def Run(
        self,
        btn,
        idx: int,              # The current line number
        split_line             # The current line, split
        ):

        if len(split_line) > 2:
            print("[" + lib + "] " + btn.coords + "  Line:" + str(idx+1) + "    Play sound file " + split_line[1] + \
                " at volume " + str(split_line[2]))
            sound.play(split_line[1], float(split_line[2]))
        else:
            print("[" + lib + "] " + btn.coords + "  Line:" + str(idx+1) + "    Play sound file " + split_line[1])
            sound.play(split_line[1])

        return idx+1


scripts.Add_command(External_Sound())  # register the command


# ##################################################
# ### CLASS External_Sound_STOP                  ###
# ##################################################

# class that defines the SOUND_STOP command (stops sound) 
class External_Sound_Stop(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__(
            "SOUND_STOP",   # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var   type     p1_val                      p2_val 
            ("Fade value", True , True, PT_INT,  variables.Validate_gt_zero, None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (0,           "    Stopping sounds immediately"), 
            (1,           "    Stopping sounds with {1} milliseconds fadeout time"), 
            ) )


    def Process(self, btn, idx, split_line):
        delay = btn.symbols[SYM_PARAMS][1]
        
        if delay == None or delay <= 0:
            sound.stop()
        else:
            sound.fadeout(int(delay))


scripts.Add_command(External_Sound())  # register the command


# ##################################################
# ### CLASS External_Code                        ###
# ##################################################

# class that defines the CODE command (runs something) 
class External_Code(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("CODE")  # the name of the command as you have to enter it in the code


    def Validate(
        self,
        btn,
        idx: int,              # The current line number
        split_line,            # The current line, split
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:       # in Pass 1 we can do general syntax check and gather symbol definitions
            if len(split_line) < 2:
                return ("Line:" + str(idx+1) + " - Too few arguments for command '" + split_line[0] + "'.", btn.line[idx])

        return True


    def Run(
        self,
        btn,
        idx: int,              # The current line number
        split_line             # The current line, split
        ):

        args = " ".join(split_line[1:])
        print("[" + lib + "] " + btn.coords + "  Line:" + str(idx+1) + "    Running code: " + args)

        try:
            subprocess.run(args)
        except Exception as e:
            print("[" + lib + "] " + btn.coords + "  Line:" + str(idx+1) + "    Error with running code: " + str(e))

        return idx+1


scripts.Add_command(External_Code())  # register the command


