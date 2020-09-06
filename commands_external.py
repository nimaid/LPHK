import command_base, webbrowser, sound, subprocess, os, scripts

lib = "cmds_extn" # name of this library (for logging)

# ##################################################
# ### CLASS External_Web                         ###
# ##################################################

# class that defines the WEB command 
class External_Web(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("WEB")  # the name of the command as you have to enter it in the code

    def Validate(
        self,
        idx: int,              # The current line number
        line,                  # The current line
        lines,                 # The current script
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:       # in Pass 1 we can do general syntax check and gather symbol definitions
            if len(split_line) < 2:
                return ("Line:" + str(idx+1) + " - Too few arguments for command '" + split_line[0] + "'.", line)

            if len(split_line) > 2:
                return ("Line:" + str(idx+1) + " - Too many arguments for command '" + split_line[0] + "'.", line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        link = split_line[1]
        if "http" not in link:
            link = "http://" + link

        print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Open website " + link + " in default browser")

        webbrowser.open(link)

        return idx+1


scripts.add_command(External_Web())  # register the command


# ##################################################
# ### CLASS External_Web_New                     ###
# ##################################################

# class that defines the WEB_NEW command 
class External_Web_New(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("WEB_NEW")  # the name of the command as you have to enter it in the code

    def Validate(
        self,
        idx: int,              # The current line number
        line,                  # The current line
        lines,                 # The current script
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:       # in Pass 1 we can do general syntax check and gather symbol definitions
            if len(split_line) < 2:
                return ("Line:" + str(idx+1) + " - Too few arguments for command '" + split_line[0] + "'.", line)

            if len(split_line) > 2:
                return ("Line:" + str(idx+1) + " - Too many arguments for command '" + split_line[0] + "'.", line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        link = split_line[1]
        if "http" not in link:
            link = "http://" + link

        print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Open website " + link + " in default browser, try to make a new window")

        webbrowser.open_new(link)

        return idx+1


scripts.add_command(External_Web_New())  # register the command


# ##################################################
# ### CLASS External_Open                        ###
# ##################################################

# class that defines the OPEN command 
class External_Open(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("OPEN")  # the name of the command as you have to enter it in the code

    def Validate(
        self,
        idx: int,              # The current line number
        line,                  # The current line
        lines,                 # The current script
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:       # in Pass 1 we can do general syntax check and gather symbol definitions
            if len(split_line) < 2:
                return ("Line:" + str(idx+1) + " - Too few arguments for command '" + split_line[0] + "'.", line)

            path_name = " ".join(split_line[1:])

            if (not os.path.isfile(path_name)) and (not os.path.isdir(path_name)):
                return ("Line:" + str(idx+1) + " - " + split_line[0] + " folder or file location '" + path_name + \
                    "' does not exist.", line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        path_name = " ".join(split_line[1:])

        print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Open file or folder " + path_name)

        files.open_file_folder(path_name)

        return idx+1


scripts.add_command(External_Open())  # register the command


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
        idx: int,              # The current line number
        line,                  # The current line
        lines,                 # The current script
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:       # in Pass 1 we can do general syntax check and gather symbol definitions
            if len(split_line) < 2:
                return ("Line:" + str(idx+1) + " - Too few arguments for command '" + split_line[0] + "'.", line)

            if len(split_line) > 3:
                return ("Line:" + str(idx+1) + " - Too many arguments for command '" + split_line[0] + "'.", line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        if len(split_line) > 2:
            print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Play sound file " + split_line[1] + \
                " at volume " + str(split_line[2]))
            sound.play(split_line[1], float(split_line[2]))
        else:
            print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Play sound file " + split_line[1])
            sound.play(split_line[1])

        return idx+1


scripts.add_command(External_Sound())  # register the command


# ##################################################
# ### CLASS External_Sound_STOP                  ###
# ##################################################

# class that defines the SOUND_STOP command (stops sound) 
class External_Sound_Stop(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("SOUND_STOP")  # the name of the command as you have to enter it in the code

    def Validate(
        self,
        idx: int,              # The current line number
        line,                  # The current line
        lines,                 # The current script
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:       # in Pass 1 we can do general syntax check and gather symbol definitions
            if len(split_line) > 2:
                return ("Line:" + str(idx+1) + " - Too many arguments for command '" + split_line[0] + "'.", line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        if len(split_line) > 1:
            delay = split_line[1]
            print("[scripts] " + coords +
                  "  Line:" + str(idx+1) + "    Stopping sounds with " + delay + " milliseconds fadeout time")
            sound.fadeout(int(delay))
        else:
            print("[scripts] " + coords + "  Line:" + str(idx+1) + "    Stopping sounds")
            sound.stop()

        return idx+1


scripts.add_command(External_Sound())  # register the command


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
        idx: int,              # The current line number
        line,                  # The current line
        lines,                 # The current script
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:       # in Pass 1 we can do general syntax check and gather symbol definitions
            if len(split_line) < 2:
                return ("Line:" + str(idx+1) + " - Too few arguments for command '" + split_line[0] + "'.", line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        args = " ".join(split_line[1:])
        print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Running code: " + args)

        try:
            subprocess.run(args)
        except Exception as e:
            print("[" + lib + "] " + coords[0] + "  Line:" + str(idx+1) + "    Error with running code: " + str(e))

        return idx+1


scripts.add_command(External_Code())  # register the command


