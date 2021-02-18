# This module is VERY specific to Win32
import os, command_base, ms, kb, scripts, variables, win32gui, commands_win32, PIL, pytesseract, io, hashlib, imagehash, dhash
from constants import *

LIB = "cmds_sscr" # name of this library (for logging)

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


# ##################################################
# ### CLASS S_OCR_FORM_TEXT                      ###
# ##################################################

# class that defines the S_OCR_FORM_TEXT command -- reads text from an image on the form
class Scrape_OCR_Form_Text(Command_Scrape):
    def __init__(
        self,
        ):

        super().__init__("S_OCR",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val 
            ("X1 value",   False, AVV_YES,  PT_INT,  None,                       None),
            ("Y1 value",   False, AVV_YES,  PT_INT,  None,                       None),
            ("X2 value",   False, AVV_YES,  PT_INT,  None,                       None),
            ("Y2 value",   False, AVV_YES,  PT_INT,  None,                       None),
            ("OCR value",  False, AVV_REQD, PT_TEXT, None,                       None),
            ("HWND",       True,  AVV_REQD, PT_INT,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (5,           "    OCR current form from ({1}, {2}) to ({3}, {4}) into {5}"), 
            (6,           "    OCR form {6} from ({1}, {2}) to ({3}, {4}) into {5}"), 
            ) )


    def Process(self, btn, idx, split_line):
        p_from = (self.Get_param(btn, 1), self.Get_param(btn, 2))     # Get the from coords
        p_to = (self.Get_param(btn, 3), self.Get_param(btn, 4))       # and the to coords     
            
        hwnd = self.Get_param(btn, 6, win32gui.GetForegroundWindow()) # get the window we're using
        
        image = self.get_image(hwnd, p_from, p_to)                    # capture an image

        txt = pytesseract.image_to_string(image)                      # OCR the image
            
        self.Set_param(btn, 5, txt)                                   # pass the text back            

        
scripts.Add_command(Scrape_OCR_Form_Text())  # register the command


# ##################################################
# ### CLASS S_IMAGE_HASH                         ###
# ##################################################

# class that defines the S_HASH command -- Takes an image and calculates a checksum
class Scrape_Image_Hash(Command_Scrape):
    def __init__(
        self,
        ):

        super().__init__("S_HASH",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val 
            ("X1 value",   False, AVV_YES,  PT_INT,  None,                       None),
            ("Y1 value",   False, AVV_YES,  PT_INT,  None,                       None),
            ("X2 value",   False, AVV_YES,  PT_INT,  None,                       None),
            ("Y2 value",   False, AVV_YES,  PT_INT,  None,                       None),
            ("Hash value", False, AVV_REQD, PT_INT,  None,                       None),
            ("HWND",       True,  AVV_REQD, PT_INT,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (5,           "    Hash of current form from ({1}, {2}) to ({3}, {4}) into {5}"), 
            (6,           "    Hash of form {6} from ({1}, {2}) to ({3}, {4}) into {5}"), 
            ) )


    def Process(self, btn, idx, split_line):
        p_from = (self.Get_param(btn, 1), self.Get_param(btn, 2))     # Get the from coords
        p_to = (self.Get_param(btn, 3), self.Get_param(btn, 4))       # and the to coords     
            
        hwnd = self.Get_param(btn, 6, win32gui.GetForegroundWindow()) # get the window we're using

        image = self.get_image(hwnd, p_from, p_to)                    # capture an image

        m = hashlib.md5()                                             # create an md5 hash object
        with io.BytesIO() as memf:                                    # write image to memory
            image.save(memf, 'PNG')                                   # as png (lossless)
            data = memf.getvalue()                                    # get the data
            m.update(data)                                            # put it in the hash object
            hash = m.hexdigest()                                      # calculate the md5 hash
            
        self.Set_param(btn, 5, hash)                                  # pass the hash back            

        
scripts.Add_command(Scrape_Image_Hash())  # register the command


# ##################################################
# ### CLASS S_IMAGE_FINGERPRINT                  ###
# ##################################################

# class that defines the S_FINGERPRINT command -- Takes an image and calculates a fingerprint
class Scrape_Image_Fingerprint(Command_Scrape):
    def __init__(
        self,
        ):

        super().__init__("S_FINGERPRINT",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var       type     p1_val                      p2_val 
            ("X1 value",   False, AVV_YES,  PT_INT,  None,                       None),
            ("Y1 value",   False, AVV_YES,  PT_INT,  None,                       None),
            ("X2 value",   False, AVV_YES,  PT_INT,  None,                       None),
            ("Y2 value",   False, AVV_YES,  PT_INT,  None,                       None),
            ("Fingerprint",False, AVV_REQD, PT_INT,  None,                       None),
            ("HWND",       True,  AVV_REQD, PT_INT,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (5,           "    Fingerprint of current form from ({1}, {2}) to ({3}, {4}) into {5}"), 
            (6,           "    Fingerprint of form {6} from ({1}, {2}) to ({3}, {4}) into {5}"), 
            ) )


    def Process(self, btn, idx, split_line):
        p_from = (self.Get_param(btn, 1), self.Get_param(btn, 2))     # Get the from coords
        p_to = (self.Get_param(btn, 3), self.Get_param(btn, 4))       # and the to coords     
            
        hwnd = self.Get_param(btn, 6, win32gui.GetForegroundWindow()) # get the window we're using
        state = self.restore_window(hwnd, True)                       # restore the window in question and make it FG
        try: 
            p_from = win32gui.ClientToScreen(hwnd, p_from)            # convert to screen coords  
            p_to = win32gui.ClientToScreen(hwnd, p_to)   
            box = p_from + p_to                                       # make a tuple with both coords
            image = PIL.ImageGrab.grab(bbox = box, all_screens=True)  # capture an image
            image.save('C:/temp/temp.png')
        finally:
            self.reset_window(state)                                  # restore windows something like previous states

        fingerprint = int(str(imagehash.dhash(image)),16)             # calculate an image fingerprint
            
        self.Set_param(btn, 5, fingerprint)                           # pass the hash back            

        
scripts.Add_command(Scrape_Image_Fingerprint())  # register the command


# ##################################################
# ### CLASS SCRAPE_FINGERPRINT_DISTANCE          ###
# ##################################################

# class that defines the S_FDIST command -- calculates the hamming difference between fingerprints
class Scrape_Fingerprint_Distance(command_base.Command_Basic):
    def __init__(
        self,
        ):

        super().__init__("S_FDIST",  # the name of the command as you have to enter it in the code
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


    def Process(self, btn, idx, split_line):
        f1 = self.Get_param(btn, 1)                    # get the fingerprints
        f2 = self.Get_param(btn, 2)
        
        dist = dhash.get_num_bits_different(f1, f2)    # hamming distance (number of bits different)
                    
        self.Set_param(btn, 3, dist)                   # pass the distance back            

        
scripts.Add_command(Scrape_Fingerprint_Distance())  # register the command
