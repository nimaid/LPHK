# This module exists simply to list the command modules imported into LPHK

IMPORT_FATAL = False

import sys, traceback
from constants import *

# any mandatory command-related stuff should be listed here
import \
  commands_header, \
  commands_control, \
  commands_keys, \
  commands_mouse, \
  commands_pause, \
  commands_external

# This library could be considered optional, but is not platform specific
try:
    import commands_rpncalc
except ImportError:
    print("[LPHK] WARNING: RPN_EVAL command is not available")  
    traceback.print_exc()

# This library could be considered optional, and is also platform specific
if PLATFORM == "windows":
    try:
        import commands_win32
    except ImportError:
        print("[LPHK] ERROR: Windows specific commands are not available") 
        traceback.print_exc()
else: 
    print("[LPHK] WARNING: Windows specific commands can not be loaded") 

# This library could be considered optional, and is also platform specific
if PLATFORM == "windows":
    try:
        import commands_scrape
    except ImportError:
        print("[LPHK] ERROR: Screen scraping commands are not available")
        traceback.print_exc()
else: 
    print("[LPHK] WARNING: Screen scraping commands can not be loaded")

# Any that were not optional should set the error flag so we can exit
if IMPORT_FATAL:  # Not using this at present
    sys.exit("[LPHK] ERROR: Required command modules are absent")

