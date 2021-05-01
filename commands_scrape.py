# This module is VERY specific to Win32
import os, command_base, ms, kb, scripts, variables, win32gui, commands_win32, PIL, pytesseract, io, hashlib, imagehash, dhash, shutil, colorsys
from constants import *

LIB = "cmds_sscr" # name of this library (for logging)

T_PATH = shutil.which('tesseract')
if T_PATH == None or not os.path.isfile(T_PATH):   # T_PATH will be None if tesseract is not on the path
    T_PATH = os.getenv('LOCALAPPDATA') + '/Tesseract-OCR/tesseract.exe'
    if not os.path.isfile(T_PATH):
        T_PATH = os.getenv('PROGRAMFILES') + '/Tesseract-OCR/tesseract.exe'
        if not os.path.isfile(T_PATH):
            raise Exception("Tesseract OCR not installed or cannot be located")

pytesseract.pytesseract.tesseract_cmd = T_PATH


# ##################################################
# ### CLASS COMMAND_SCRAPE                       ###
# ##################################################

# class that defines additional scraping stuff
class Command_Scrape(commands_win32.Command_Win32):

    # scrapes an image relative to a window
    def get_image(self, hwnd, p_from, p_to):
        state = self.restore_window(hwnd, True)                  # restore the window in question and make it FG
        try:
            p_from = win32gui.ClientToScreen(hwnd, p_from)       # convert to screen coords
            p_to = win32gui.ClientToScreen(hwnd, p_to)
            box = p_from + p_to                                  # make a tuple with both coords
            image = PIL.ImageGrab.grab(bbox = box, all_screens=True)  # capture an image
            #image.save('C:/temp/temp.png')
        finally:
            self.reset_window(state)                             # restore windows something like previous states

        return image                                             # return the image


    # scrapes an image from the clipboard
    def get_copied_image(self, btn):
        tries = 5
        while tries >= 0:
            try:
                image = PIL.ImageGrab.grabclipboard()            # grab the image from he clipboard
                return image
            except:
                tries -= 1
                btn.Safe_sleep(0.5)
                
        return -1                                                # return the image


# ##################################################
# ### CLASS SCRAPE_SCREEN                        ###
# ##################################################

# class that defines the S_ command -- reads text from an image on the form
class Scrape_OCR_Form_Text(Command_Scrape):
    def __init__(
        self,
        ):

        super().__init__("S_GET_SCREEN, captures a part of the screen or of a window",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("X1 value",   False, AVV_YES,  PT_INT,  None,                       None),
            ("Y1 value",   False, AVV_YES,  PT_INT,  None,                       None),
            ("X2 value",   False, AVV_YES,  PT_INT,  None,                       None),
            ("Y2 value",   False, AVV_YES,  PT_INT,  None,                       None),
            ("Image",      False, AVV_REQD, PT_OBJ,  None,                       None),
            ("HWND",       True,  AVV_REQD, PT_INT,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (5,           "    captures current form from ({1}, {2}) to ({3}, {4}) into image {5}"),
            (6,           "    captures form {6} from ({1}, {2}) to ({3}, {4}) into image {5}"),
            ) )
            
        self.deprecated = True
        self.deprecated_use = "This command will not exist in the production release.  " + \
                              "Use S_GET_WIN instead. possibly in combination with the S_OCR command."

        self.doc = ["Captures a part of the screen from (`X1`,`Y1`) to (`X2`,`Y2`), "
                    "returning this in an image in `Image`.",
                    "",
                    "If a window handle (`HWND`) is passed, the coordinates are relative to "
                    "that window, otherwise the coordinates are screen absolute.",
                    ""
                    "The returned image can be passed to other commands that require an image."]

                    
    def Process(self, btn, idx, split_line):
        p_from = (self.Get_param(btn, 1), self.Get_param(btn, 2))     # Get the from coords
        p_to = (self.Get_param(btn, 3), self.Get_param(btn, 4))       # and the to coords

        hwnd = self.Get_param(btn, 6, win32gui.GetForegroundWindow()) # get the window we're using

        image = self.get_image(hwnd, p_from, p_to)                    # capture an image

        self.Set_param(btn, 5, image)                                 # pass the image back


scripts.Add_command(Scrape_OCR_Form_Text())  # register the command


# ##################################################
# ### CLASS SCRAPE_GET_WINDOW                    ###
# ##################################################

# class that defines the S_GET_WIN command -- returns an image from the screen
class Scrape_Get_Window(Command_Scrape):
    def __init__(
        self,
        ):

        super().__init__("S_GET_WIN, captures a part of the screen or of a window",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("X1 value",   False, AVV_YES,  PT_INT,  None,                       None),
            ("Y1 value",   False, AVV_YES,  PT_INT,  None,                       None),
            ("X2 value",   False, AVV_YES,  PT_INT,  None,                       None),
            ("Y2 value",   False, AVV_YES,  PT_INT,  None,                       None),
            ("Image",      False, AVV_REQD, PT_OBJ,  None,                       None),
            ("HWND",       True,  AVV_REQD, PT_INT,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (5,           "    captures current form from ({1}, {2}) to ({3}, {4}) into image {5}"),
            (6,           "    captures form {6} from ({1}, {2}) to ({3}, {4}) into image {5}"),
            ) )

        self.doc = ["Captures a part of the screen from (`X1`,`Y1`) to (`X2`,`Y2`), "
                    "returning this in an image in `Image`.",
                    "",
                    "If a window handle (`HWND`) is passed, the coordinates are relative to "
                    "that window, otherwise the coordinates are screen absolute.",
                    ""
                    "The returned image can be passed to other commands that require an image."]


    def Process(self, btn, idx, split_line):
        p_from = (self.Get_param(btn, 1), self.Get_param(btn, 2))     # Get the from coords
        p_to = (self.Get_param(btn, 3), self.Get_param(btn, 4))       # and the to coords

        hwnd = self.Get_param(btn, 6, win32gui.GetForegroundWindow()) # get the window we're using

        image = self.get_image(hwnd, p_from, p_to)                    # capture an image

        self.Set_param(btn, 5, image)                                 # pass the image back


scripts.Add_command(Scrape_Get_Window())  # register the command


# ##################################################
# ### CLASS SCRAPE_GET_CLIPBOARD                 ###
# ##################################################

# class that defines the S_GET_CLIP command -- reads text from an image on the form
class Scrape_Get_Clipboard(Command_Scrape):
    def __init__(
        self,
        ):

        super().__init__("S_GET_CLIP, Returns the image in the clipboard",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("Image",      False, AVV_REQD, PT_OBJ,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (1,           "    place clipboard image into image {1}"),
            ) )

        self.doc = ["Captures an image from the clipboard.  This is typically an image of the "
                    "most recent field where text has been copied, but it can be from any "
                    "source.",
                    "",
                    "The returned image can be passed to other commands that require an image."]


    def Process(self, btn, idx, split_line):
        image = self.get_copied_image(btn)                              # get clipboard image

        self.Set_param(btn, 1, image)                                   # pass the text back


scripts.Add_command(Scrape_Get_Clipboard())  # register the command


# ##################################################
# ### CLASS SCRAPE_OCR                           ###
# ##################################################

# class that defines the S_OCR command -- OCR on an image
class Scrape_OCR(Command_Scrape):
    def __init__(
        self,
        ):

        super().__init__("S_OCR, performs OCR on an image",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("Image",      False, AVV_REQD, PT_OBJ,  None,                       None),
            ("OCR value",  False, AVV_REQD, PT_STR,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2,           "    OCR image {1} to {2}"),
            ) )

        self.doc = ["Performs OCR on an image, returning the text.",
                    "",
                    "The image typically comes from one of the other `S_...` commands, "
                    "but could be sourced from elsewhere."]


    def Process(self, btn, idx, split_line):
        image = self.get_copied_image(btn)                            # get copied image

        txt = pytesseract.image_to_string(image)                      # OCR the image

        self.Set_param(btn, 1, txt)                                   # pass the text back


scripts.Add_command(Scrape_OCR())  # register the command


# ##################################################
# ### CLASS S_IMAGE_HASH                         ###
# ##################################################

# class that defines the S_HASH command -- Takes an image and calculates a checksum
class Scrape_Image_Hash(Command_Scrape):
    def __init__(
        self,
        ):

        super().__init__("S_HASH, returns a hash value that (almost) uniquely identifies an image",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("Image",      False, AVV_REQD, PT_OBJ,  None,                       None),
            ("Hash value", False, AVV_REQD, PT_INT,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2,           "    Hash image {1} into {2}"),
            ) )

        self.doc = ["Creates the hash of an image, returning a value that changes significantly "
                    "even with small changes to the original image.",
                    "",
                    "The image typically comes from one of the other `S_...` commands, "
                    "but could be sourced from elsewhere.",
                    "",
                    "This command is best used as part of a process to determine if 2 images "
                    "are identical."]


    def Process(self, btn, idx, split_line):
        image = self.Get_param(btn, 1)                                # get the image

        m = hashlib.md5()                                             # create an md5 hash object
        with io.BytesIO() as memf:                                    # write image to memory
            image.save(memf, 'PNG')                                   # as png (lossless)
            data = memf.getvalue()                                    # get the data
            m.update(data)                                            # put it in the hash object
            hash = m.hexdigest()                                      # calculate the md5 hash

        self.Set_param(btn, 2, hash)                                  # pass the hash back


scripts.Add_command(Scrape_Image_Hash())  # register the command


# ##################################################
# ### CLASS S_IMAGE_COLOUR                       ###
# ##################################################

# constants for S_IMAGE_COLOUR
SIC_MEAN    = "MEAN"
SIC_MODAL   = "MODAL"

SICG_ALL = [SIC_MEAN, SIC_MODAL]

# class that defines the S_COLOUR command -- Takes an image and calculates a checksum
class Scrape_Image_Colour(Command_Scrape):
    def __init__(
        self,
        ):

        super().__init__("S_COLOUR, determines the average R, G, and B values of an image",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("Image",      False, AVV_REQD, PT_OBJ,  None,                       None),
            ("Red",        False, AVV_REQD, PT_INT,  None,                       None),
            ("Green",      False, AVV_REQD, PT_INT,  None,                       None),
            ("Blue",       False, AVV_REQD, PT_INT,  None,                       None),
            ("Method",     True,  AVV_NO,   PT_WORD, None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (4,           "    average colour of image {1} in ({2}, {3}, {4})"),
            (5,           "    average colour of image {1} in ({2}, {3}, {4}) using method {5}"),
            ) )

        self.doc = ["Creates an average colour representation of an `Image`, returning "
                    "the `Red`, `Green`, and `Blue` values coresponding to that average."
                    "even with small changes to the original image.",
                    "",
                    "The image typically comes from one of the other `S_...` commands, "
                    "but could be sourced from elsewhere.",
                    "",
                    "This command is often used as part of a process to determine if a "
                    "copied field is of a certain colour.  Note that because an average "
                    "colour is created, the comparason is normally to a range of colours, "
                    "using the S_CDIST command."]


    def Process(self, btn, idx, split_line):
        image = self.Get_param(btn, 1)          # get the image
        method = self.Get_param(btn, 5, SIC_MEAN)

        pixels = image.load()                   # create the pixel map

        if method == SIC_MEAN:
            r = 0                               # initialise RGB and pixel count to 0
            g = 0
            b = 0
            p = 0

            for i in range(image.size[0]):      # for every col:
                for j in range(image.size[1]):  # for every row
                    px = pixels[i, j]
                    p += 1
                    r += px[0]
                    g += px[1]
                    b += px[2]

            if p > 0:                           # calc average data
               r = r // p
               g = g // p
               b = b // p

        elif method == SIC_MODAL:
            #Get colors from image object
            pixels = image.getcolors(image.size[0] * image.size[1])
            #Sort them by count number(first element of tuple)
            sorted_pixels = sorted(pixels, key=lambda t: t[0])
            #Get the most frequent color
            dominant_colour = sorted_pixels[-1][1]
            
            r = dominant_colour[0]
            g = dominant_colour[1]
            b = dominant_colour[2]
            
        self.Set_param(btn, 2, r)               # send back RGB
        self.Set_param(btn, 3, g)
        self.Set_param(btn, 4, b)


    def Partial_validate_step_pass_1(self, ret, btn, idx, split_line):
        ret = super().Partial_validate_step_pass_1(ret, btn, idx, split_line)     # perform the original pass 1 validation

        if ret == None or ((type(ret) == bool) and ret):                          # if the original validation hasn't raised an error
            if (len(split_line) > 5) and (not split_line[5] in SICG_ALL):         # invalid subcommand
                c_ok = ', '.join(SICG_ALL[:-1]) + ', or ' + SICG_ALL[-1]
                s_err = f"Invalid subcommand {split_line[1]} when expecting {c_ok}."
                return (s_err, btn.Line(idx))
        return ret


scripts.Add_command(Scrape_Image_Colour())  # register the command


# ##################################################
# ### CLASS S_IMAGE_FINGERPRINT                  ###
# ##################################################

# class that defines the S_FINGERPRINT command -- Takes an image and calculates a fingerprint
class Scrape_Image_Fingerprint(Command_Scrape):
    def __init__(
        self,
        ):

        super().__init__("S_FINGERPRINT, Fingerprint an image",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("Image",      False, AVV_REQD, PT_OBJ,  None,                       None),
            ("Fingerprint",False, AVV_REQD, PT_INT,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (2,           "    Fingerprint of image {1} into {2}"),
            ) )

        self.doc = ["Creates a fingerprint of an image, returning a value that is "
                    "similar for similar images, and relatively insensitive to "
                    "small differences between images.",
                    "",
                    "The image typically comes from one of the other `S_...` commands, "
                    "but could be sourced from elsewhere.",
                    "",
                    "This command is best used as part of a process to determine if 2 images "
                    "are similar, often usinf the S+FDIST command."]


    def Process(self, btn, idx, split_line):
        image = self.Get_param(btn, 1)                                # get the image

        fingerprint = int(str(imagehash.dhash(image)),16)             # calculate an image fingerprint

        self.Set_param(btn, 2, fingerprint)                           # pass the hash back


scripts.Add_command(Scrape_Image_Fingerprint())  # register the command


# ##################################################
# ### CLASS SCRAPE_FINGERPRINT_DISTANCE          ###
# ##################################################

# class that defines the S_FDIST command -- calculates the hamming difference between fingerprints
class Scrape_Fingerprint_Distance(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("S_FDIST, Calculate the distance between 2 fingerprints",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("F1",         False, AVV_YES,  PT_INT,  None,                       None),
            ("F2",         False, AVV_YES,  PT_INT,  None,                       None),
            ("Distance",   False, AVV_REQD, PT_INT,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (3,           "    Return the hamming distance between fingerprints {1} and {2} into {3}"),
            ) )

        self.doc = ["This command calculates the hamming distance between 2 fingerprints. "
                    "This can be used to determine how similar 2 images are.  The larger "
                    "the hamming distance, the more different the images are."]


    def Process(self, btn, idx, split_line):
        f1 = self.Get_param(btn, 1)                    # get the fingerprints
        f2 = self.Get_param(btn, 2)

        dist = dhash.get_num_bits_different(f1, f2)    # hamming distance (number of bits different)

        self.Set_param(btn, 3, dist)                   # pass the distance back


scripts.Add_command(Scrape_Fingerprint_Distance())  # register the command


# ##################################################
# ### CLASS SCRAPE_COLOUR_DISTANCE               ###
# ##################################################

# class that defines the S_CDIST command -- calculates the hamming difference between fingerprints
class Scrape_Colour_Distance(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("S_CDIST, Calculate the distance between 2 RGB values",
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val
            ("R1",         False, AVV_YES,  PT_INT,  None,                       None),
            ("G1",         False, AVV_YES,  PT_INT,  None,                       None),
            ("B1",         False, AVV_YES,  PT_INT,  None,                       None),
            ("R2",         False, AVV_YES,  PT_INT,  None,                       None),
            ("G2",         False, AVV_YES,  PT_INT,  None,                       None),
            ("B2",         False, AVV_YES,  PT_INT,  None,                       None),
            ("Distance",   False, AVV_REQD, PT_INT,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (7,           "    Return the hamming distance between colours ({1}, {2}, {3}) and ({4}, {5}, {6}) into {7}"),
            ) )

        self.doc = ["This can be used to determine how similar 2 colours are.  The larger "
                    "the distance, the more different the colours are."]


    def Process(self, btn, idx, split_line):
        r1 = self.Get_param(btn, 1)                    # get the colours
        g1 = self.Get_param(btn, 2)
        b1 = self.Get_param(btn, 3)

        r2 = self.Get_param(btn, 4)
        g2 = self.Get_param(btn, 5)
        b2 = self.Get_param(btn, 6)
        
        dist = abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)

        self.Set_param(btn, 7, dist)                   # pass the distance back


scripts.Add_command(Scrape_Colour_Distance())  # register the command


# ##################################################
# ### CLASS SCRAPE_RGB_TO_HSV                    ###
# ##################################################

# class that defines the S_RGB_TO_HSV command -- converts RGB to an HSV colour space
class Scrape_Rgb_To_Hsv(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("S_RGB_TO_HSV, Converts RGB to an HSV colour space",
            LIB,
            (
            # Desc         Opt    Var       type      p1_val                      p2_val
            ("R",          False, AVV_YES,  PT_INT,   None,                       None),
            ("G",          False, AVV_YES,  PT_INT,   None,                       None),
            ("B",          False, AVV_YES,  PT_INT,   None,                       None),
            ("H",          False, AVV_REQD, PT_FLOAT, None,                       None),
            ("S",          False, AVV_REQD, PT_FLOAT, None,                       None),
            ("V",          False, AVV_REQD, PT_FLOAT, None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (6,           "    converts RGB ({1}, {2}, {3}) to HSV ({4}, {5}, {6})"),
            ) )

        self.doc = ["This command converts an RGB value into an HSV value. "
                    "It can be used to determine the Hue, Saturation, and/or "
                    "Value (Brightness) of a colour.",
                    "",
                    "All values are in the range 0..255"]


    def Process(self, btn, idx, split_line):

        r = self.Get_param(btn, 1)                    # get the colours
        g = self.Get_param(btn, 2)
        b = self.Get_param(btn, 3)

        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)

        self.Set_param(btn, 4, int(h*255))
        self.Set_param(btn, 5, int(s*255))
        self.Set_param(btn, 6, int(v*255))


scripts.Add_command(Scrape_Rgb_To_Hsv())  # register the command


# ##################################################
# ### CLASS SCRAPE_RGB_TO_HSL                    ###
# ##################################################

# class that defines the S_RGB_TO_HSL command -- converts RGB to an HSL colour space
class Scrape_Rgb_To_Hsl(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("S_RGB_TO_HSL, Converts RGB to an HSL colour space",
            LIB,
            (
            # Desc         Opt    Var       type      p1_val                      p2_val
            ("R",          False, AVV_YES,  PT_INT,   None,                       None),
            ("G",          False, AVV_YES,  PT_INT,   None,                       None),
            ("B",          False, AVV_YES,  PT_INT,   None,                       None),
            ("H",          False, AVV_REQD, PT_FLOAT, None,                       None),
            ("S",          False, AVV_REQD, PT_FLOAT, None,                       None),
            ("L",          False, AVV_REQD, PT_FLOAT, None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (6,           "    converts RGB ({1}, {2}, {3}) to HSV ({4}, {5}, {6})"),
            ) )

        self.doc = ["This command converts an RGB value into an HSL value. "
                    "It can be used to determine the Hue, Saturation, and/or "
                    "Luminance of a colour.",
                    "",
                    "All values are in the range 0..255"]


    def Process(self, btn, idx, split_line):

        r = self.Get_param(btn, 1)                    # get the colours
        g = self.Get_param(btn, 2)
        b = self.Get_param(btn, 3)

        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)

        self.Set_param(btn, 4, int(h*255))
        self.Set_param(btn, 5, int(s*255))
        self.Set_param(btn, 6, int(l*255))


scripts.Add_command(Scrape_Rgb_To_Hsl())  # register the command


# ##################################################
# ### CLASS SCRAPE_RGB_TO_Brightness             ###
# ##################################################

# class that defines the S_RGB_TO_B command -- an alternative routine to calculate the perceptual brightness of a colour
class Scrape_Rgb_To_Brightness(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("S_RGB_TO_B, An alternative routine to calculate the perceptual brightness of a colour",
            LIB,
            (
            # Desc         Opt    Var       type      p1_val                      p2_val
            ("R",          False, AVV_YES,  PT_INT,   None,                       None),
            ("G",          False, AVV_YES,  PT_INT,   None,                       None),
            ("B",          False, AVV_YES,  PT_INT,   None,                       None),
            ("Bright",     False, AVV_REQD, PT_FLOAT, None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (4,           "    converts RGB ({1}, {2}, {3}) to Brightness ({4})"),
            ) )

        self.doc = ["This command converts an RGB value into an alternative brightness "
                    "value.  It can be used to determine Value (Brightness) of a colour "
                    "in a more perceptually correct manner.",
                    "",
                    "All values are in the range 0..255"]


    def Process(self, btn, idx, split_line):
        r = self.Get_param(btn, 1)                    # get the colours
        g = self.Get_param(btn, 2)
        b = self.Get_param(btn, 3)

        br = 0.243863271*r + 0.673319569*g + 0.08281716*b
        v = cmax * 100

        self.Set_param(btn, 4, int(br))


scripts.Add_command(Scrape_Rgb_To_Brightness())  # register the command
