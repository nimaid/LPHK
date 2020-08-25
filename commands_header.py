import command_base, kb, lp_events, scripts


# ##################################################
# ### CLASS Header_Async                         ###
# ##################################################

class Header_Async(command_base.Command_Header):
    def __init__(
        self, 
        ):

        super().__init__("@ASYNC", True)


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
            if idx > 0:
                return ("@ASYNC must appear on the first line.", lines[0])

            if len(split_line) > 1:
                return ("@ASYNC takes no arguments.", lines[0])

        return True


    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
        ):

        return idx+1


scripts.add_command(Header_Async())


# ##################################################
# ### CLASS Header_Simple                        ###
# ##################################################

class Header_Simple(command_base.Command_Header):
    def __init__(
        self, 
        ):

        super().__init__("@SIMPLE", False)


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
            if idx > 0:
                return ("@ASYNC must appear on the first line.", lines[0])

            if len(split_line) < 2:
                return ("@SIMPLE requires a key to bind.", line)

            if len(split_line) > 2:
                return ("@SIMPLE only take one argument", line)

            if kb.sp(split_line[1]) == None:
                return ("No key named '" + split_line[1] + "'.", line)

            for lin in lines[1:]:
                if lin != "" and lin[0] != "-":
                    return ("When @SIMPLE is used, scripts can only contain comments.", lin)

        return True


    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
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


scripts.add_command(Header_Simple())


# ##################################################
# ### CLASS Header_Load_Layout                   ###
# ##################################################

class Header_Load_Layout(command_base.Command_Header):
    def __init__(
        self, 
        ):

        super().__init__("@LOAD_LAYOUT", False)


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
                return ("@LOAD_LAYOPUT requires a filename as a parameter.", line)

        return True


    def Run(
        self,
        idx: int,
        split_line,
        symbols,
        coords,
        is_async
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


scripts.add_command(Header_Load_Layout())


