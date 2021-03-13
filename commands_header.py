import command_base, kb, lp_events, scripts


# ##################################################
# ### CLASS Header_Async                         ###
# ##################################################

class Header_Async(command_base.Command_Header):
    def __init__(
        self,
        ):

        super().__init__("@ASYNC",      # the name of the header as you have to enter it in the code
            True)                       # This must be specified for async headers

    def Validate(
        self,
        btn,
        idx: int,              # The current line number
        split_line,            # The current line, split
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:
            if idx > 0:        # headers normally have to check the line number
                return ("Line:" + str(idx+1) + " - " + self.name + " must appear on the first line.", btn.Line(0))

            if len(split_line) > 1:
                return ("Line:" + str(idx+1) + " - " + self.name + " takes no arguments.", btn.Line(idx))

        return True


scripts.Add_command(Header_Async())  # register the header


# ##################################################
# ### CLASS Header_Simple                        ###
# ##################################################

class Header_Simple(command_base.Command_Header_Run):
    def __init__(
        self,
        ):

        super().__init__("@SIMPLE")      # the name of the header as you have to enter it in the code

    def Validate(
        self,
        btn,
        idx: int,              # The current line number
        split_line,            # The current line, split
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:
            if idx > 0:        # headers normally have to check the line number
                return ("Line:" + str(idx+1) + " - " + self.name + " must appear on the first line.", btn.Line(0))

            if len(split_line) < 2:
                return ("Line:" + str(idx+1) + " - " + self.name + " requires a key to bind.", btn.Line(idx))

            if len(split_line) > 2:
                return ("Line:" + str(idx+1) + " - " + self.name + " only take one argument", btn.Line(idx))

            if kb.sp(split_line[1]) == None:
                return ("Line:" + str(idx+1) + " - No key named '" + split_line[1] + "'.", btn.Line(idx))

            for lin in lines[1:]:
                if lin != "" and lin[0] != "-":
                    return ("Line:" + str(idx+1) + " - When " + self.name + " is used, scripts can only contain comments.", lin)

        return True


    def Run(
        self,
        btn,
        idx: int,              # The current line number
        split_line             # The current line, split
        ):

        print("[cmds_head] " + coords + "  Line:" + str(idx+1) + "    Simple keybind: " + split_line[1])

        #PRESS
        key = kb.sp(split_line[1])
        releasefunc = lambda: kb.release(key)
        kb.press(key)

        #WAIT_UNPRESSED
        while lp_events.pressed[x][y]:
            sleep(DELAY_EXIT_CHECK)
            if btn.Check_kill(releasefunc):
                return idx + 1

        #RELEASE
        kb.release(key)

        return idx+1


scripts.Add_command(Header_Simple())  # register the header


# ##################################################
# ### CLASS Header_Load_Layout                   ###
# ##################################################

# Loads a new layout.  @@@ This should probably be rewritten in the newest style
class Header_Load_Layout(command_base.Command_Header_Run):
    def __init__(
        self,
        ):

        super().__init__("@LOAD_LAYOUT")      # the name of the header as you have to enter it in the code


    def Validate(
        self,
        btn,
        idx: int,              # The current line number
        split_line,            # The current line, split
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:
            if idx > 0:        # headers normally have to check the line number
                return ("Line:" + str(idx+1) + " - " + self.name + " must appear on the first line.", lines[0])

            if len(split_line) < 2:
                return ("Line:" + str(idx+1) + " - " + self.name + " requires a filename as a parameter.", btn.Line(idx))

        return True


    def Run(
        self,
        btn,
        idx: int,              # The current line number
        split_line             # The current line, split
        ):

        layout_name = " ".join(split_line[1:])

        print("[cmds_head] " + coords + "  Line:" + str(idx+1) + "    Load layout " + layout_name)

        layout_path = os.path.join(files.LAYOUT_PATH, layout_name)
        if not os.path.isfile(layout_path):
            print("[cmds_head] " + coords + "  Line:" + str(idx+1) + "        ERROR: Layout file does not exist.")
            return -1

        try:
            layout = files.load_layout(layout_path, popups=False, save_converted=False)
        except files.json.decoder.JSONDecodeError:
            print("[cmds_head] " + coords + "  Line:" + str(idx+1) + "        ERROR: Layout is malformated.")
            return -1

        if files.layout_changed_since_load:
            files.save_lp_to_layout(files.curr_layout)

        files.load_layout_to_lp(layout_path, popups=False, save_converted=False, preload=layout)

        return idx+1


scripts.Add_command(Header_Load_Layout())  # register the header


# ##################################################
# ### CLASS Header_Name                          ###
# ##################################################

# This is a dummy header.  It is interpreted for real when a subroutine is loaded,
# but is ignored in the normal running of commands
class Header_Name(command_base.Command_Header):
    def __init__(
        self,
        ):

        super().__init__("@NAME, Names a button")


    # Dummy validate routine.  Simply says all is OK (unless you try to do it in a real button!)
    def Validate(
        self,
        btn,
        idx: int,              # The current line number
        split_line,            # The current line, split
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:
            if btn.is_button:
                btn.Set_name(' '.join(split_line[1:]))
            else:
                return ("Line:" + str(idx+1) + " - The header '" + split_line[0] + "' is only permitted in a button.", btn.Line(idx))

        return True


scripts.Add_command(Header_Name())  # register the header


# ##################################################
# ### CLASS Header_Desc                          ###
# ##################################################

# This is a dummy header.  It is interpreted for real when a subroutine is loaded,
# but is ignored in the normal running of commands
class Header_Desc(command_base.Command_Header):
    def __init__(
        self,
        ):

        super().__init__("@DESC, Defines a description line")


    # Dummy validate routine.  Simply says all is OK (without a validation routine, an error is reported (but not printed)
    def Validate(
        self,
        btn,
        idx: int,              # The current line number
        split_line,            # The current line, split
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:
            btn.desc = ' '.join(split_line[1:])

        return True


scripts.Add_command(Header_Desc())  # register the header


# ##################################################
# ### CLASS Header_Doc                           ###
# ##################################################

# This is a dummy header.  It is interpreted for real when a subroutine is loaded,
# but is ignored in the normal running of commands
class Header_Doc(command_base.Command_Header):
    def __init__(
        self,
        ):

        super().__init__("@DOC, Adds a line to the documentation text")


    # Dummy validate routine.  Simply says all is OK (without a validation routine, an error is reported (but not printed)
    def Validate(
        self,
        btn,
        idx: int,              # The current line number
        split_line,            # The current line, split
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:
            btn.doc += [' '.join(split_line[1:])]

        return True


scripts.Add_command(Header_Doc())  # register the header