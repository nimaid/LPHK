import command_base, kb, lp_events, scripts

lib = "cmds_ctrl" # name of this library (for logging)

# ##################################################
# ### CLASS Keys_Wait_Pressed                    ###
# ##################################################

# class that defines the WAIT_PRESSED command (wait while a button is pressed?)
class Keys_Wait_Pressed(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("WAIT_PRESSED")  # the name of the command as you have to enter it in the code

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
            if len(split_line) > 1:
                return ("Too many arguments for command '" + split_line[0] + "'.", line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + lib + "] " + coords + "    Wait for script key to be unpressed")

        while lp_events.pressed[coords[1]][coords[2]]:
            sleep(DELAY_EXIT_CHECK)
            if check_kill(x, y, is_async):
                return idx + 1             

        return idx+1


scripts.add_command(Keys_Wait_Pressed())  # register the command


# ##################################################
# ### CLASS Keys_Tap                             ###
# ##################################################

# class that defines the TAP command (tap button a button)
class Keys_Tap(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("TAP")  # the name of the command as you have to enter it in the code

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
                return ("Too few arguments for command '" + split_line[0] + "'.", line)

            if len(split_line) > 4:
                return ("Too many arguments for command '" + split_line[0] + "'.", line)

            if kb.sp(split_line[1]) == None:
                return ("No key named '" + split_line[1] + "'.", line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        key = kb.sp(split_line[1])

        releasefunc = lambda: kb.release(key)

        if len(split_line) <= 2:
            print("[" + lib + "] " + coords[0] + "    Tap key " + split_line[1])
            kb.tap(key)
        elif len(split_line) <= 3:
            print("[" + lib + "] " + coords[0] + "    Tap key " + split_line[1] + " " + split_line[2] + " times")
            taps = int(split_line[2])

            for tap in range(taps):
                if check_kill(coords[1], coords[2], is_async, releasefunc):
                    return idx + 1
                kb.tap(key)
        else:
            print("[" + lib + "] " + coords[0] + "    Tap key " + split_line[1] + " " + split_line[2] + \
                " times for " + str(split_line[3]) + " seconds each")

            taps = int(split_line[2])
            delay = float(split_line[3])

            for tap in range(taps):
                if check_kill(coords[1], coords[2], is_async, releasefunc):
                    return -1

                kb.press(key)
                if not safe_sleep(delay, coords[1], coords[2], is_async, releasefunc):
                    return -1

        return idx+1


scripts.add_command(Keys_Tap())  # register the command


# ##################################################
# ### CLASS Keys_Press                           ###
# ##################################################

# class that defines the PRESS command (press a button)
class Keys_Press(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("PRESS")  # the name of the command as you have to enter it in the code

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
                return ("Too few arguments for command '" + split_line[0] + "'.", line)

            if len(split_line) > 2:
                return ("Too many arguments for command '" + split_line[0] + "'.", line)

            if kb.sp(split_line[1]) == None:
                return ("No key named '" + split_line[1] + "'.", line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + lib + "] " + coords[0] + "    Press key " + split_line[1])

        key = kb.sp(split_line[1])
        kb.press(key)

        return idx+1


scripts.add_command(Keys_Press())  # register the command


# ##################################################
# ### CLASS Keys_Release                         ###
# ##################################################

# class that defines the RELEASE command (un-press a button)
class Keys_Release(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("RELEASE")  # the name of the command as you have to enter it in the code

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
                return ("Too few arguments for command '" + split_line[0] + "'.", line)

            if len(split_line) > 2:
                return ("Too many arguments for command '" + split_line[0] + "'.", line)

            if kb.sp(split_line[1]) == None:
                return ("No key named '" + split_line[1] + "'.", line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + lib + "] " + coords[0] + "    Release key " + split_line[1])

        key = kb.sp(split_line[1])
        kb.release(key)

        return idx+1


scripts.add_command(Keys_Release())  # register the command


# ##################################################
# ### CLASS Keys_Release_All                     ###
# ##################################################

# class that defines the RELEASE_ALL command (un-press all keys)
class Keys_Release_All(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("RELEASE_ALL")  # the name of the command as you have to enter it in the code

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
            if len(split_line) > 1:
                return ("Too many arguments for command '" + split_line[0] + "'.", line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[" + lib + "] " + coords[0] + "    Release all keys")

        kb.release_all()

        return idx+1


scripts.add_command(Keys_Release_All())  # register the command


# ##################################################
# ### CLASS Keys_String                          ###
# ##################################################

# class that defines the STRING command (type a string)
class Keys_String(command_base.Command_Basic):
    def __init__(
        self, 
        ):

        super().__init__("STRING")  # the name of the command as you have to enter it in the code

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
                return ("Too few arguments for command '" + split_line[0] + "'.", line)

        return True

    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        type_string = " ".join(split_line[1:])

        print("[" + lib + "] " + coords[0] + "    Type out string " + type_string)

        kb.write(type_string)

        return idx+1


scripts.add_command(Keys_String())  # register the command
