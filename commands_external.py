import command_base, webbrowser, sound, subprocess, os, scripts


# ##################################################
# ### CLASS External_Web                         ###
# ##################################################

# class that defines the WEB command 
class External_Web(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("WEB")

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
            if len(split_line) < 2:
                return ("Too few arguments for command '" + split_line[0] + "'.", line)

            if len(split_line) > 2:
                return ("Too many arguments for command '" + split_line[0] + "'.", line)

        return True

    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        link = split_line[1]
        if "http" not in link:
            link = "http://" + link

        print("[cmds_extn] " + coords[0] + "    Open website " + link + " in default browser")

        webbrowser.open(link)

        return idx+1


scripts.add_command(External_Web())


# ##################################################
# ### CLASS External_Web_New                     ###
# ##################################################

# class that defines the WEB_NEW command 
class External_Web_New(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("WEB_NEW")

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
            if len(split_line) < 2:
                return ("Too few arguments for command '" + split_line[0] + "'.", line)

            if len(split_line) > 2:
                return ("Too many arguments for command '" + split_line[0] + "'.", line)

        return True

    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        link = split_line[1]
        if "http" not in link:
            link = "http://" + link

        print("[cmds_extn] " + coords[0] + "    Open website " + link + " in default browser, try to make a new window")

        webbrowser.open_new(link)

        return idx+1


scripts.add_command(External_Web_New())


# ##################################################
# ### CLASS External_Open                        ###
# ##################################################

# class that defines the OPEN command 
class External_Open(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("OPEN")

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
            if len(split_line) < 2:
                return ("Too few arguments for command '" + split_line[0] + "'.", line)

            path_name = " ".join(split_line[1:])

            if (not os.path.isfile(path_name)) and (not os.path.isdir(path_name)):
                return (split_line[0] + " folder or file location '" + path_name + \
                    "' does not exist.", line)

        return True

    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        path_name = " ".join(split_line[1:])

        print("[cmds_extn] " + coords[0] + "    Open file or folder " + path_name)

        files.open_file_folder(path_name)

        return idx+1


scripts.add_command(External_Open())


# ##################################################
# ### CLASS External_Sound                       ###
# ##################################################

# class that defines the SOUND command (plays a sound file) 
class External_Sound(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("SOUND")

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
            if len(split_line) < 2:
                return ("Too few arguments for command '" + split_line[0] + "'.", line)

            if len(split_line) > 3:
                return ("Too many arguments for command '" + split_line[0] + "'.", line)

        return True

    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        if len(split_line) > 2:
            print("[cmds_extn] " + coords[0] + "    Play sound file " + split_line[1] + \
                " at volume " + str(split_line[2]))
            sound.play(split_line[1], float(split_line[2]))
        else:
            print("[cmds_extn] " + coords[0] + "    Play sound file " + split_line[1])
            sound.play(split_line[1])

        return idx+1


scripts.add_command(External_Sound())


# ##################################################
# ### CLASS External_Sound_STOP                  ###
# ##################################################

# class that defines the SOUND_STOP command (stops sound) 
class External_Sound_Stop(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("SOUND_STOP")

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
            if len(split_line) > 2:
                return ("Too many arguments for command '" + split_line[0] + "'.", line)

        return True

    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        if len(split_line) > 1:
            delay = split_line[1]
            print("[scripts] " + coords +
                  "    Stopping sounds with " + delay + " milliseconds fadeout time")
            sound.fadeout(int(delay))
        else:
            print("[scripts] " + coords + "    Stopping sounds")
            sound.stop()

        return idx+1


scripts.add_command(External_Sound())


# ##################################################
# ### CLASS External_Code                        ###
# ##################################################

# class that defines the CODE command (runs something) 
class External_Code(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("CODE")

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
            if len(split_line) < 2:
                return ("Too few arguments for command '" + split_line[0] + "'.", line)

        return True

    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        args = " ".join(split_line[1:])
        print("[cmds_extn] " + coords[0] + "    Running code: " + args)

        try:
            subprocess.run(args)
        except Exception as e:
            print("[cmds_extn] " + coords[0] + "    Error with running code: " + str(e))

        return idx+1


scripts.add_command(External_Code())


