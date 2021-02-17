# This module is VERY specific to Win32
import os, command_base, ms, kb, scripts, variables, win32gui, commands_win32, PIL, pytesseract
from constants import *

LIB = "cmds_sscr" # name of this library (for logging)

T_PATH = os.getenv('LOCALAPPDATA') + '/Tesseract-OCR/tesseract.exe'
if not os.path.isfile(T_PATH):
    T_PATH = os.getenv('PROGRAMFILES') + '/Tesseract-OCR/tesseract.exe'
    if not os.path.isfile(T_PATH):
        raise Exception("Tesseract OCR not installed or cannot be located")

pytesseract.pytesseract.tesseract_cmd = T_PATH


# ##################################################
# ### CLASS S_OCR_FORM_TEXT                      ###
# ##################################################

# class that defines the S_OCR_FORM_TEXT command -- reads text from an image on the form
class Scrape_OCR_Form_Text(commands_win32.Command_Win32):
    def __init__(
        self,
        ):

        super().__init__("S_OCR_FORM_TEXT",  # the name of the command as you have to enter it in the code
            LIB,
            (
            # Desc         Opt    Var   type     p1_val                      p2_val 
            ("X1 value",   False, True, PT_INT,  None,                       None),
            ("Y1 value",   False, True, PT_INT,  None,                       None),
            ("X2 value",   False, True, PT_INT,  None,                       None),
            ("Y2 value",   False, True, PT_INT,  None,                       None),
            ("OCR value",  False, True, PT_VAR,  None,                       None),
            ("HWND",       True,  True, PT_VAR,  None,                       None),
            ),
            (
            # num params, format string                           (trailing comma is important)
            (5,           "    OCR current form from ({1}, {2}) to ({3}, {4}) into {5}"), 
            (6,           "    OCR form {6} from ({1}, {2}) to ({3}, {4}) into {5}"), 
            ) )


    def Process(self, btn, idx, split_line):
        p_from = (self.Get_param(btn, 1), self.Get_param(btn, 2))     # Get the from coords
        p_to = (self.Get_param(btn, 3), self.Get_param(btn, 4))       # and the to coords     
            
        hwnd = self.Get_param(btn, 6, win32gui.GetForegroundWindow()) # get the windoe we're using
        state = self.restore_window(hwnd, True)                       # restore the window in question and make it FG
        try: 
            p_from = win32gui.ClientToScreen(hwnd, p_from)            # convert to screren coords  
            p_to = win32gui.ClientToScreen(hwnd, p_to)   
            box = p_from + p_to                                       # make a tuple with both coords
            image = PIL.ImageGrab.grab(bbox = box, all_screens=True)  # capture an image
            #image.save('C:/temp/temp.png')
        finally:
            self.reset_window(state)                                  # restore windows something like previous states

        txt = pytesseract.image_to_string(image)                      # OCR the image
            
        self.Set_param(btn, 5, txt)                                   # pass the text back            

        
scripts.Add_command(Scrape_OCR_Form_Text())  # register the command


