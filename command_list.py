# This module exists simply to list the command modules imported into LPHK

IMPORT_FATAL = False

import sys

import \
  commands_header, \
  commands_control, \
  commands_keys, \
  commands_mouse, \
  commands_pause, \
  commands_external

# This library could be considered optional
try:
    import commands_rpncalc
except:
    print("[LPHK] WARNING: RPN_EVAL command is not available")  

# This library could be considered optional  
try:
    import commands_win32
except:
    print("[LPHK] WARNING: Windows specific commands are not available")  

# This library could be considered optional  
try:
    import commands_scrape
except:
    print("[LPHK] WARNING: Screen scraping commands are unavailable")  

# Any that were not optional should set the error flag so we can exit
if IMPORT_FATAL:
    sys.exit("[LPHK] ERROR: Required command modules are absent")

