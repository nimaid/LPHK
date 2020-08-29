import command_base, kb, lp_events, scripts


# ##################################################
# ### CLASS Header_Async                         ###
# ##################################################

class Header_Async(command_base.Command_Header):
    def __init__(
        self, 
        ):

        super().__init__("@ASYNC",      # the name of the header as you have to enter it in the code
            True)                       # You also define if the header causes the script to be asynchronous

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
            if idx > 0:        # headers normally have to check the line number
                return (self.name + " must appear on the first line.", lines[0])

            if len(split_line) > 1:
                return (self.name + " takes no arguments.", line)

        return True


    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        return idx+1


scripts.add_command(Header_Async())  # register the header


# ##################################################
# ### CLASS Header_Simple                        ###
# ##################################################

class Header_Simple(command_base.Command_Header):
    def __init__(
        self, 
        ):

        super().__init__("@SIMPLE",      # the name of the header as you have to enter it in the code
            False)                       # You also define if the header causes the script to be asynchronous

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
            if idx > 0:        # headers normally have to check the line number
                return (self.name + " must appear on the first line.", lines[0])

            if len(split_line) < 2:
                return (self.name + " requires a key to bind.", line)

            if len(split_line) > 2:
                return (self.name + " only take one argument", line)

            if kb.sp(split_line[1]) == None:
                return ("No key named '" + split_line[1] + "'.", line)

            for lin in lines[1:]:
                if lin != "" and lin[0] != "-":
                    return ("When " + self.name + " is used, scripts can only contain comments.", lin)

        return True


    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        print("[cmds_head] " + coords + "    Simple keybind: " + split_line[1])

        #PRESS
        key = kb.sp(split_line[1])
        releasefunc = lambda: kb.release(key)
        kb.press(key)

        #WAIT_UNPRESSED
        while lp_events.pressed[x][y]:
            sleep(DELAY_EXIT_CHECK)
            if check_kill(x, y, is_async, releasefunc):
                return idx + 1

        #RELEASE
        kb.release(key)

        return idx+1


scripts.add_command(Header_Simple())  # register the header


# ##################################################
# ### CLASS Header_Load_Layout                   ###
# ##################################################

class Header_Load_Layout(command_base.Command_Header):
    def __init__(
        self, 
        ):

        super().__init__("@LOAD_LAYOUT",      # the name of the header as you have to enter it in the code
            False)                            # You also define if the header causes the script to be asynchronous


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
            if idx > 0:        # headers normally have to check the line number
                return (self.name + " must appear on the first line.", lines[0])

            if len(split_line) < 2:
                return (self.name + " requires a filename as a parameter.", line)

        return True


    def Run(
        self,
        idx: int,              # The current line number
        split_line,            # The current line, split
        symbols,               # The symbol table (a dictionary containing labels, loop counters etc.)
        coords,                # Tuple of printable coords as well as the individual x and y values
        is_async               # True if the script is running asynchronously
        ):

        layout_name = " ".join(split_line[1:])

        print("[cmds_head] " + coords + "    Load layout " + layout_name)

        layout_path = os.path.join(files.LAYOUT_PATH, layout_name)
        if not os.path.isfile(layout_path):
            print("[cmds_head] " + coords + "        ERROR: Layout file does not exist.")
            return -1

        try:
            layout = files.load_layout(layout_path, popups=False, save_converted=False)
        except files.json.decoder.JSONDecodeError:
            print("[cmds_head] " + coords + "        ERROR: Layout is malformated.")
            return -1

        if files.layout_changed_since_load:
            files.save_lp_to_layout(files.curr_layout)

        files.load_layout_to_lp(layout_path, popups=False, save_converted=False, preload=layout)

        return idx+1


scripts.add_command(Header_Load_Layout())  # register the header


