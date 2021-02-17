# This module is VERY specific to Win32
import command_base, ms, kb, scripts, variables, win32gui, commands_win32, PIL, pytesseract
from constants import *

LIB = "cmds_sscr" # name of this library (for logging)

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
        p_from = (self.Get_param(btn, 1), self.Get_param(btn, 2))
        p_to = (self.Get_param(btn, 3), self.Get_param(btn, 4))         
            
        hwnd = self.Get_param(btn, 6, win32gui.GetForegroundWindow())
        state = self.restore_window(hwnd, True)
        try: 
            import time
            time.sleep(1)
            p_from = win32gui.ClientToScreen(hwnd, p_from)        
            p_to = win32gui.ClientToScreen(hwnd, p_to)   
            box = p_from + p_to
            print("@@@", box)
            image = PIL.ImageGrab.grab(bbox = box)  # @@@ bugfix https://github.com/python-pillow/Pillow/issues/1547
            image.save('C:/temp/temp.png')
        finally:
            self.reset_window(state)

        pytesseract.pytesseract.tesseract_cmd = r'C:\Users\HE123240\AppData\Local\Tesseract-OCR\tesseract.exe'
        txt = pytesseract.image_to_string(image)
        print("@@@", txt)
            
        self.Set_param(btn, 5, txt)                                  # pass this back            

        
scripts.Add_command(Scrape_OCR_Form_Text())  # register the command


