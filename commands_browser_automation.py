# This module is VERY specific to Win32
import command_base, scripts, traceback
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from constants import *

LIB = "cmds_baut" # name of this library (for logging)

# constants for characters we replace in strings (note that these are not standard)
ESCAPE_CHARS  = ["\\n", "\\^", "\\h"]
REPLACE_CHARS = ["\n", Keys.ARROW_UP, Keys.HOME]

# constants for BA_START
BAS_CHROME     = "CHROME"
BAS_CHROMIUM   = "CHROMIUM"
BAS_EDGE       = "EDGE"
BAS_FIREFOX    = "FIREFOX"
BAS_IE         = "IE"
BAS_OPERA      = "OPERA"
BAS_SAFARI     = "SAFARI"
BAS_WEBKITGTK  = "WEBKITGTK"
BAS_REMOTE     = "REMOTE"

BASG_ALL = [BAS_CHROME, BAS_CHROMIUM, BAS_EDGE, BAS_FIREFOX, BAS_IE, BAS_OPERA, BAS_SAFARI, BAS_WEBKITGTK, BAS_REMOTE]

# ##################################################
# ### CLASS BAUTO_START                          ###
# ##################################################

# class that defines the BA_START command that starts a browser under automated control
class Bauto_Start(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("BA_START, Starts a browser under automated control",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("Browser",    False, AVV_NO,   PT_WORD, None,                       None),
            ("Auto",       False, AVV_REQD, PT_OBJ,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2,           "    Open browser {1} for automation as {2}"),
            ) )

        self.doc = ["Starts a browser using selinium for automated control.  The return will "
                    "be an object if the call suceeds, otherwise it will return -1.",
                    "",
                    "NOTE 1: The first parameter should be used to select what browser you "
                    "want to load.  This is implemented, but has only been tested with Chrome. "
                    "The values that can be used are:",
                    "",
                    "      {BAS_CHROME}",
                    "      {BAS_CHROMIUM}",
                    "      {BAS_EDGE}",
                    "      {BAS_FIREFOX}",
                    "      {BAS_IE}",
                    "      {BAS_OPERA}",
                    "      {BAS_SAFARI}",
                    "      {BAS_WEBKITGTK}",
                    "      {BAS_REMOTE}",
                    "",
                    "NOTE 2: This blocks while the browser loads, so it should use a "
                    "similar technique to the dialog boxes to pass this processing off "
                    "to another thread."]


    def Process(self, btn, idx, split_line):
        br = self.Get_param(btn, 1)
        try:
            if br == BAS_CHROME:
                auto = webdriver.Chrome()
            elif br == BAS_CHROMIUM:
                auto = webdriver.Chromium()
            elif br == BAS_EDGE:
                auto = webdriver.Edge()
            elif br == BAS_FIREFOX:
                auto = webdriver.Firefox()
            elif br == BAS_IE:
                auto = webdriver.Ie()
            elif br == BAS_OPERA:
                auto = webdriver.Opera()
            elif br == BAS_SAFARI:
                auto = webdriver.Safari()
            elif br == BAS_WEBKITGTK:
                auto = webdriver.Webkitgtk()
            elif br == BAS_REMOTE:
                auto = webdriver.Remote()
        except:
            traceback.print_exc()
            auto = -1

        self.Set_param(btn, 2, auto)                                 # pass the object back


    def Partial_validate_step_pass_1(self, ret, btn, idx, split_line):
        ret = super().Partial_validate_step_pass_1(ret, btn, idx, split_line)     # perform the original pass 1 validation

        if ret == None or ((type(ret) == bool) and ret):                          # if the original validation hasn't raised an error
            if not split_line[1] in BASG_ALL:                                     # invalid subcommand
                c_ok = ', '.join(BASG_ALL[:-1]) + ', or ' + BASG_ALL[-1]
                s_err = f"Invalid subcommand {split_line[1]} when expecting {c_ok}."
                return (s_err, btn.Line(idx))
        return ret


scripts.Add_command(Bauto_Start())  # register the command


# ##################################################
# ### CLASS BAUTO_NAVIGATE                       ###
# ##################################################

# class that defines the BA_NAVIGATE command navigates the browser to a particular page
class Bauto_Navigate(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("BA_NAVIGATE, Navigate controlled browser to a new URL",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("Auto",       False, AVV_REQD, PT_OBJ,  None,                       None),
            ("URL",        False, AVV_YES,  PT_STR,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2,           "    Navigate browser to {2}"),
            ) )

        self.doc = ["Navigates an existing browser to a new URL.",
                    "",
                    "NOTE 1: This blocks while the browser loads the page, so it should use "
                    "a similar technique to the dialog boxes to pass this processing off to "
                    "another thread."]


    def Process(self, btn, idx, split_line):
        auto = self.Get_param(btn, 1)
        url = self.Get_param(btn, 2)
        try:
            auto.get(url)
        except:
            traceback.print_exc()


scripts.Add_command(Bauto_Navigate())  # register the command


# ##################################################
# ### CLASS BAUTO_STOP                           ###
# ##################################################

# class that defines the BA_STOP command to close the browser
class Bauto_Stop(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("BA_STOP, Stops the browser under automated control",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("Auto",       False, AVV_REQD, PT_OBJ,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (1,           "    Stop browser {1}"),
            ) )

        self.doc = ["Closes an existing browser.",
                    "",
                    "NOTE 1: You should probably clear the variable that held the browser "
                    "object after you call this."]


    def Process(self, btn, idx, split_line):
        auto = self.Get_param(btn, 1)
        try:
            auto.quit()
        except:
            traceback.print_exc()


scripts.Add_command(Bauto_Stop())  # register the command


# ##################################################
# ### CLASS BAUTO_GET_URL                        ###
# ##################################################

# class that defines the BA_GET_URL command to find out what page the operator is on
class Bauto_Get_Url(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("BA_GET_URL, Returns the URL of the current page",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("Auto",       False, AVV_REQD, PT_OBJ,  None,                       None),
            ("URL",        False, AVV_REQD, PT_STR,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2,           "    Return current url on {1} into {2}"),
            ) )

        self.doc = ["Returns the URL the existing browser is displaying.",
                    "",
                    "NOTE 1: This can fail (returning a blank string) if the browser is "
                    "still loading the page."]


    def Process(self, btn, idx, split_line):
        auto = self.Get_param(btn, 1)
        url = ''
        try:
            url = auto.current_url;
        except:
            traceback.print_exc()

        self.Set_param(btn, 2, url)                                 # pass the url back


scripts.Add_command(Bauto_Get_Url())  # register the command


# constants for BA_GET_ELEMENT
BAG_XPATH        = "XPATH"
BAG_NAME         = "NAME"
BAG_TAG_NAME     = "TAG_NAME"
BAG_ID           = "ID"
BAG_LABEL        = "LABEL"
BAG_LINK_TEXT    = "LINK_TEXT"
BAG_CLASS_NAME   = "CLASS_NAME"
BAG_CSS_SELECTOR = "CSS_SELECTOR"

BAGG_ALL = [BAG_XPATH, BAG_NAME, BAG_TAG_NAME, BAG_ID, BAG_LABEL, BAG_LINK_TEXT, BAG_CLASS_NAME, BAG_CSS_SELECTOR]

# ##################################################
# ### CLASS BAUTO_GET_ELEMENT                    ###
# ##################################################

# class that defines the BA_GET_ELEMENT command to get an element from a loaded page
class Bauto_Get_Element(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("BA_GET_ELEMENT, Returns an element along a particular xpath",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("Auto",       False, AVV_REQD, PT_OBJ,  None,                       None),
            ("Method",     False, AVV_NO,   PT_WORD, None,                       None),
            ("Search",     False, AVV_YES,  PT_STR,  None,                       None),
            ("Element",    False, AVV_REQD, PT_OBJ,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (4,           "    Return element {3} from {1} into {4} using method {2}"),
            ) )

        self.doc = ["Returns an element at the location.  Often this will be used to extract "
                    "tables for further processing.",
                    "",
                    "The first parameter `Auto` is weither an browser object or an element "
                    "returned from a successful search.",
                    "",
                    "The `Method` can be:",
                    "",
                    "~19",
                    "      XPATH      - finds element by xpath",
                    "      NAME       - finds element by name",
                    "      TAG_NAME   - finds element by tag name",
                    "      ID         - finds element by its id",
                    "      LINK_TEXT  - finds element by its link text",
                    "      CLASS_NAME - finds element by class name",
                    "~",
                    "",
                    "See selenium documentation for information about xpaths.",
                    "",
                    "The third parameter `Search` is the search string.  Thhe format of this "
                    "depends on the search method.",
                    "",
                    "The final parameter `Element` is the element returned from the search.  If "
                    "The search fails, -1 will be returned."]


    def Process(self, btn, idx, split_line):
        auto = self.Get_param(btn, 1)
        method = self.Get_param(btn, 2)
        search = self.Get_param(btn, 3)

        element = -1
        try:
            element = auto.find_element(method.lower().replace("_", " "), search)
        except:
            traceback.print_exc()

        self.Set_param(btn, 4, element)                                 # pass the element back


    def Partial_validate_step_pass_1(self, ret, btn, idx, split_line):
        ret = super().Partial_validate_step_pass_1(ret, btn, idx, split_line)     # perform the original pass 1 validation

        if ret == None or ((type(ret) == bool) and ret):                          # if the original validation hasn't raised an error
            if not split_line[2] in BAGG_ALL:                                     # invalid subcommand
                c_ok = ', '.join(BAGG_ALL[:-1]) + ', or ' + BAGG_ALL[-1]
                s_err = f"Invalid subcommand {split_line[2]} when expecting {c_ok}."
                return (s_err, btn.Line(idx))
        return ret


scripts.Add_command(Bauto_Get_Element())  # register the command


# ##################################################
# ### CLASS BAUTO_GET_TABLE_SIZE                 ###
# ##################################################

# class that defines the BA_GET_TABLE_SIZE command to get the dimensions of a table
class Bauto_Get_Table_Size(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("BA_GET_TABLE_SIZE, Returns the dimensions of a table",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("Table",      False, AVV_REQD, PT_OBJ,  None,                       None),
            ("Rows",       False, AVV_REQD, PT_INT,  None,                       None),
            ("Cols",       False, AVV_REQD, PT_INT,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (3,           "    Return dimensions of table {1} into ({2}, {3})"),
            ) )

        self.doc = ["Returns the number of rows and columns for a table.  This table should "
                    "have previously been obtained by fetching a table element from a loaded "
                    "page.",
                    "",
                    "The first parameter `Table` is an element returned from a search.  it is "
                    "unlikely that any object other than a table will produce sensible results.",
                    "",
                    "The result `Rows` will be the number of rows in the table.  -1, will be "
                    "returned in case of error.",
                    "",
                    "The result `Cols` will be the number of columns in the 0th row of the table.",
                    "",
                    "Note that because HTML tables can have a variable number of columns, it "
                    "cannot be assumed that all rows will have this number of columns.  -1 will "
                    "be returned in case of error."]


    def Process(self, btn, idx, split_line):
        table = self.Get_param(btn, 1)

        rows = -1
        cols = -1
        try:
            r_elements = table.find_elements(By.TAG_NAME, "tr")
            rows = len(r_elements)
            if rows > 0:
                r_element = r_elements[0]
                cols = len(r_element.find_elements(By.TAG_NAME, "td")) + len(r_element.find_elements(By.TAG_NAME, "th"))
        except:
            traceback.print_exc()

        self.Set_param(btn, 2, rows)                                 # pass the dimensions back
        self.Set_param(btn, 3, cols)


scripts.Add_command(Bauto_Get_Table_Size())  # register the command


# ##################################################
# ### CLASS BAUTO_GET_TABLE_CELL                 ###
# ##################################################

# class that defines the BA_GET_TABLE_CELL command to get data from a table cell
class Bauto_Get_Table_Cell(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("BA_GET_TABLE_CELL, Returns the table cell element",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("Table",      False, AVV_REQD, PT_OBJ,  None,                       None),
            ("Row",        False, AVV_YES,  PT_INT,  None,                       None),
            ("Col",        False, AVV_YES,  PT_INT,  None,                       None),
            ("Cell",       False, AVV_REQD, PT_STR,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (4,           "    Return cell ({2}, {3}) from {1} into {4}"),
            ) )

        self.doc = ["The first parameter `Table` is an element returned from a search.  it is "
                    "unlikely that any object other than a table will produce sensible results.",
                    "",
                    "The `Row` and `Col` parameters specify the 0-based offset in "
                    "have previously been obtained by fetching a table element from a loaded"
                    "page.",
                    "",
                    "The parameter `Cell` will contain the cell from the table.  -1 will be "
                    "returned in case of error."]


    def Process(self, btn, idx, split_line):
        table = self.Get_param(btn, 1)
        row = self.Get_param(btn, 2)
        col = self.Get_param(btn, 3)

        cell = -1
        try:
            r_elements = table.find_elements(By.TAG_NAME, "tr")
            if len(r_elements) > row:
                r_element = r_elements[row]

                c_elements = r_element.find_elements(By.TAG_NAME, "td")
                if col >= len(c_elements):
                   col = col - len(c_elements)
                   c_elements = r_element.find_elements(By.TAG_NAME, "th")

                if len(c_elements) > col:
                    c_element = c_elements[col]
                    cell = c_element

        except:
            traceback.print_exc()

        self.Set_param(btn, 4, cell)                                 # pass the contents back


scripts.Add_command(Bauto_Get_Table_Cell())  # register the command


# ##################################################
# ### CLASS BAUTO_GET_ELEMENT_TEXT               ###
# ##################################################

# class that defines the BA_GET_ELEMENT_TEXT command to get text from an element
class Bauto_Get_Element_Text(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("BA_GET_ELEMENT_TEXT, Returns the text content of an element",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("Element",    False, AVV_REQD, PT_OBJ,  None,                       None),
            ("Text",       False, AVV_REQD, PT_STR,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2,           "    Return text of element {1} int {2}"),
            ) )

        self.doc = ["The first parameter `Element` is an element returned from a search.",
                    "",
                    "The `Text` parameters will be populated the text of the element.  -1 "
                    "will be returned in case of error."]


    def Process(self, btn, idx, split_line):
        element = self.Get_param(btn, 1)

        text = -1
        try:
            text = element.text

        except:
            traceback.print_exc()

        self.Set_param(btn, 2, text)                                 # pass the contents back


scripts.Add_command(Bauto_Get_Element_Text())  # register the command


# ##################################################
# ### CLASS BAUTO_CLICK_ELEMENT                  ###
# ##################################################

# class that defines the BA_CLICK command to click an element
class Bauto_Click_Element(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("BA_CLICK, Clicks on an element",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("Element",    False, AVV_REQD, PT_OBJ,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (1,           "    Click on {1}"),
            ) )

        self.doc = ["The first parameter `Element` is an element returned from a search.",
                    "",
                    "This method will click on that element.",
                    "",
                    "There is no return value."]


    def Process(self, btn, idx, split_line):
        element = self.Get_param(btn, 1)

        try:
            element.click()

        except:
            traceback.print_exc()


scripts.Add_command(Bauto_Click_Element())  # register the command


# ##################################################
# ### CLASS BAUTO_SEND_TEXT                      ###
# ##################################################

# class that defines the BA_SEND_TEXT command to send keys to an element
class Bauto_Send_Text(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("BA_SEND_TEXT, Sends keys to an element",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("Element",    False, AVV_REQD, PT_OBJ,  None,                       None),
            ("Text",       False, AVV_YES,  PT_STR,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (1,           "    Click on {1}"),
            ) )

        self.doc = ["The first parameter `Element` is an element returned from a search.",
                    "",
                    "This method will send text to that element.  Note that there are a few special "
                    "escape characters:",
                    "",
                    "~15",
                    "        `\\n` - will be replaced with a newline,",
                    "        `\h` - will be replaced with a press of the home key",
                    "        `\^` - will be replaced with a press of the arrow up key",
                    "~",
                    "",
                    "There is no return value."]


    def Process(self, btn, idx, split_line):
        element = self.Get_param(btn, 1)
        text = self.Get_param(btn, 2)
        for x, y in zip(ESCAPE_CHARS, REPLACE_CHARS):
            text = text.replace(x, y)

        try:
            element.send_keys(text)

        except:
            traceback.print_exc()


scripts.Add_command(Bauto_Send_Text())  # register the command


# ##################################################
# ### CLASS BAUTO_SHOW_ELEMENTS                  ###
# ##################################################

# class that defines the BA_SHOW_ELEMENTS command to dump elements inside the passed element
class Bauto_ShowElements(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("BA_SHOW_ELEMENTS, Print the elements within the passed element",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("Element",    False, AVV_REQD, PT_OBJ,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (1,           "    Show elements in {1}"),
            ) )


    def Process(self, btn, idx, split_line):
        element = self.Get_param(btn, 1)
        text = self.Get_param(btn, 2)

        try:
            e = element
            print(e)
            try:
                print(f"{0}:\n properties: {e.get_property('attributes')}\n text: {e.get_attribute('text')}\n content: {e.get_attribute('textContent')}")
            except:
                pass
            es = element.find_elements(BAG_XPATH.lower().replace("_", " "), ".//*")
            for i, e in enumerate(es):
                print(f"{i+1}:\n properties: {e.get_property('attributes')}\n text: {e.get_attribute('text')}\n content: {e.get_attribute('textContent')}")
            print(len(es))

        except:
            traceback.print_exc()


scripts.Add_command(Bauto_ShowElements())  # register the command
