import command_base, kb, lp_events, scripts, lp_colors


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

        self.deprecated = True
        self.deprecated_use = "This header should not be used in new scripts.  The LOAD_LAYOUT command" + \
                              "serves the same function."

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
        
        self.doc = ["The @NAME header defines a name for a script.  This name is also "
                    "displayed on the LPHK form as annotation for the button the script "
                    "is assigned to.",
                    "",
                    "A simple example is as follows:",
                    "",
                    "      @NAME Boo!",
                    "",
                    "This will cause the script to be named `Boo!`, and for this text to "
                    "appear on the assigned button and in internally generated documentation.",
                    "",
                    "The space on buttons is limited.  For the larger square buttons, "
                    "three lines of five characters can be displayed.  For the smaller "
                    "round buttons, only two lines of three characters will fit.",
                    "",
                    "LPHK attempts to display the name as best it can.  Firstly, it breaks "
                    "long words into shorter fragments, then it tries to pack those fragments "
                    "together.  The previous example `Boo!` is less than 5 characters, so "
                    "it fits completely on one line.  The name `Pieces of text to display` "
                    "would first be broken up into `Piece` `s` `of` `text` `to` `displ` ay`, "
                    "then joined back up as `Piece` `s of` `text`,  The remainder can't be "
                    "fitted, and is dropped off.  The button would contain the text:",
                    "",
                    "      Piece",
                    "      s of",
                    "      text",
                    "",
                    "Shorter text strings are are displayed using larger fonts for greater "
                    "readability.",
                    "",
                    "Only a single name header is permitted in a script.",
                    "",
                    "This is not permitted in a subroutine because the subroutine is named "
                    "using the `@SUB` header."]


    # Dummy validate routine.  Simply says all is OK (unless you try to do it in a subroutine!)
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

        self.doc = ["The @DESC header defines a short description for a script or subroutine.",
                    "",
                    "A simple example is as follows:",
                    "",
                    "      @DESC Do really amazing things",
                    "",
                    "This will cause the script or subroutine to be described as `Do really "
                    "amazing things`, in internally generated documentation.",
                    "",
                    "Only a single description header is permitted in a script or subroutine."]


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

        self.doc = ["The `@DOC` header allows multiple line documentation to be written for a script "
                    "or subroutine.  Each `@DOC` line is appended to the documentation.",
                    "",
                    "A simple example is as follows:",
                    "",
                    "      @DOC This is the first line of the documentation...",
                    "      @DOC ...and this is the second.",
                    "",
                    "When the internal documentation is produced for the script or subroutine, this "
                    "text will appear."]


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


# ##################################################
# ### CLASS Header_Doc_Add                       ###
# ##################################################

# This is a dummy header.  It is interpreted for real when a subroutine is loaded,
# but is ignored in the normal running of commands
class Header_Doc_Add(command_base.Command_Header):
    def __init__(
        self,
        ):

        super().__init__("@DOC+, Extends a line of the documentation text without adding a line break")

        self.doc = ["The `@DOC+` header allows a documentation line to be extended so that "
                    "word wrapping works correctly",
                    "",
                    "A simple example is as follows:",
                    "",
                    "      @DOC This is the first line of the documentation...",
                    "      @DOC+ ...and this is more of the 1st line.",
                    "",
                    "When the internal documentation is produced for the script or subroutine, this "
                    "text will appear with the line wrapped as required."]


    # Dummy validate routine.  Simply says all is OK (without a validation routine, an error is reported (but not printed)
    def Validate(
        self,
        btn,
        idx: int,              # The current line number
        split_line,            # The current line, split
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:
            add_part = split_line[1:]
            last_part = btn.doc[-1:]
            last_part += add_part
            btn.doc[-1] = ' '.join(last_part)

        return True


scripts.Add_command(Header_Doc_Add())  # register the header


# ##################################################
# ### CLASS Header_Deprecated                    ###
# ##################################################

# The Deprecated header marks a routine as deprecated with any additional text
# placed in the "use" description.
class Header_Deprecated(command_base.Command_Header):
    def __init__(
        self,
        ):

        super().__init__("@DEPRECATED, Marks the routine as deprecated")

        self.doc = ["The `@DEPRECSTED` header allows a routine to be marked as Deprecated.",
                    "",
                    "Some simple examples follows",
                    "",
                    "      @DEPRECATED",
                    "      @DEPRECATED Please use the XYZ command instead",
                    "",
                    "When the internal documentation is produced for the script or subroutine, it "
                    "will be flagged as deprecated.  The optional message will be printed.",
                    "",
                    "A parameter may be available to either flag or prevent the use of deprecated "
                    "commands..."]


    # Validate routine.  Adds the deprecated information if the command is not already deprecated!
    def Validate(
        self,
        btn,
        idx: int,              # The current line number
        split_line,            # The current line, split
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:
            if self.deprecated: # don't want to deprecate twice!
                return ("Line:" + str(idx+1) + " - The header '" + split_line[0] + "' is only permitted once.", btn.Line(idx))
            else:
                self.deprecated = True
                self.deprecated_use = ' '.join(split_line[1:])

        return True


scripts.Add_command(Header_Doc())  # register the header

# ##################################################
# ### CLASS Header_Colour                        ###
# ##################################################

# The Deprecated header marks a routine as deprecated with any additional text
# placed in the "use" description.
class Header_Colour(command_base.Command_Header):
    def __init__(
        self,
        ):

        super().__init__("@COLOUR, Sets (overrides) the default buton colour")

        self.doc = ["The `@COLOUR` header allows a routine to be assigned a default button colour.",
                    "",
                    "Some simple examples follows",
                    "",
                    "      @COLOUR f00",
                    "      @COLOUR fff",
                    "",
                    "When the routine is parsed, the default button colour is set to the RGB value specified by a 3 character hex constant.",
                    "",
                    "If repeated, this the colour will be set to the last specified colour"]


    # Validate routine.  Adds the deprecated information if the command is not already deprecated!
    def Validate(
        self,
        btn,
        idx: int,              # The current line number
        split_line,            # The current line, split
        pass_no                # interpreter pass (1=gather symbols & check syntax, 2=check symbol references)
        ):

        if pass_no == 1:
            if len(split_line) <= 1:
                return ("Line:" + str(idx+1) + " - The header '" + split_line[0] + "' must have a colour specified.", btn.Line(idx))
            elif len(split_line) > 2:
                return ("Line:" + str(idx+1) + " - The header '" + split_line[0] + "' must have only 1 colour specified.", btn.Line(idx))
            else:
                if len(split_line[1]) != 3:
                    return (f"Line:{idx+1} - The header '{split_line[0]}' has a colour {split_line[1]} that is not a 3 character hex value for RGB.", btn.Line(idx))
                try:
                    cv = int('0x' + split_line[1], 16)
                except:
                    return (f"Line:{idx+1} - The header '{split_line[0]}' has a colour {split_line[1]} that is not a 3 character hex value for RGB.", btn.Line(idx))
                c = split_line[1].lower()
                btn.colour = lp_colors.Hex_to_RGB(c)
                    
        return True


scripts.Add_command(Header_Colour())  # register the header