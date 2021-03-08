import sys, os, subprocess, argparse, global_vars
from datetime import datetime
from constants import *

print("\n!!!!!!!! DO NOT CLOSE THIS WINDOW WITHOUT SAVING !!!!!!!!\n")

LOG_TITLE = "LPHK.log"

# Test if this is a PyInstaller executable or a .py file
if getattr(sys, 'frozen', False):
    IS_EXE = True
    PROG_FILE = sys.executable
    PROG_PATH = os.path.dirname(PROG_FILE)
    PATH = sys._MEIPASS
else:
    IS_EXE = False
    PROG_FILE = os.path.realpath(__file__)
    PROG_PATH = os.path.dirname(PROG_FILE)
    PATH = PROG_PATH

# Test if there is a user folder specified
def get_first_textfile_line(file_path):
    file_lines = None
    with open(file_path, "r") as f:
        file_lines = f.readlines()
    first_line = file_lines[0]
    return first_line.strip()

USERPATH_FILE = os.path.join(PATH, "USERPATH")
if os.path.exists(USERPATH_FILE):
    IS_PORTABLE = False
    USER_PATH = get_first_textfile_line(USERPATH_FILE)
    os.makedirs(USER_PATH, exist_ok=True)
else:
    IS_PORTABLE = True
    USER_PATH = PROG_PATH

# Get program version
VERSION = get_first_textfile_line(os.path.join(PATH, "VERSION"))

# Setup dual logging/printing
LOG_PATH = os.path.join(USER_PATH, LOG_TITLE)

import logger
logger.start(LOG_PATH)


# Start printing output
def datetime_str():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


print("---------------- BEGIN LOG", datetime_str(), "----------------")
print("LPHK - LaunchPad HotKey - A Novation Launchpad Macro Scripting System")
print("Version:", VERSION)
print("Platform:", PLATFORM.capitalize())
print("Is compiled executable:", IS_EXE)
print("Is portable:", IS_PORTABLE)
print("Operating path:", PATH)
print("User path:", USER_PATH)
print("Program file path:", PROG_PATH)
print("Program file:", PROG_FILE)
print("Log file (this file):", LOG_PATH, end="\n\n")

# Try to import launchpad.py
try:
    import launchpad_py as launchpad_real
except ImportError:
    try:
        import launchpad as launchpad_real
    except ImportError:
        sys.exit("[LPHK] Error loading launchpad.py")
print("")

import lp_events, scripts, kb, files, sound, window
from utils import launchpad_connector

# just import the control modules to automatically integrate them
import command_list


# create a launchpad object, either real or fake
def Launchpad():
    if window.IsStandalone():
        import launchpad_fake
        return launchpad_fake.launchpad
    else:
        return launchpad_real.Launchpad()


LP = None

EXIT_ON_WINDOW_CLOSE = True

def init():
    global EXIT_ON_WINDOW_CLOSE

    ap = argparse.ArgumentParser()                             # argparse makes argument processing easy
    ap.add_argument(                                           # reimnplementation of debug (-d or --debug)
        "-d", "--debug",
        help = "Turn on debugging mode", action="store_true")
    ap.add_argument(                                           # option to automatically load a layout
        "-l", "--layout",
        help = "Load an initial layout",
        type=argparse.FileType('r'))
    ap.add_argument(                                           # option to start minimised
        "-m", "--minimised",
        help = "Start the application minimised", action="store_true")
    ap.add_argument(                                           # option to start without connecting to a Launchpad
        "-s", "--standalone",
        help = "Operate without connection to Launchpad", action="store_true")

    global_vars.ARGS = vars(ap.parse_args())                   # store the arguments in a place anything can get to

    if global_vars.ARGS['debug']:
        EXIT_ON_WINDOW_CLOSE = False
        print("[LPHK] Debugging mode active! Will not shut down on window close.")
        print("[LPHK] Run shutdown() to manually close the program correctly.")

    files.init(USER_PATH)
    sound.init(USER_PATH)
    
    global LP
    LP = Launchpad()

def shutdown():
    if lp_events.timer != None:                          # cancel any outstanding events
        lp_events.timer.cancel()

    scripts.to_run = []                                  # remove anything from the list of scripts scheduled to run

    for x in range(9):
        for y in range(9):
            if scripts.buttons[x][y].thread != None:
                scripts.buttons[x][y].thread.kill.set()  # request to kill any running threads

    if window.lp_connected:
        scripts.Unbind_all()                             # unbind all the buttons
        lp_events.timer.cancel()                         # cancel all the timers
        if LP != None and LP != -1:
            launchpad_connector.disconnect(LP)           # disconnect from the launchpad
        window.lp_connected = False

    logger.stop()                                        # stop logging

    if window.restart:
        window.restart = False                           # don't do this forever
        if IS_EXE:
            os.startfile(sys.argv[0])
        else:
            os.execv(sys.executable, ["\"" + sys.executable + "\""] + sys.argv)

    sys.exit("[LPHK] Shutting down...")


def main():
    init()
    window.init(LP, PATH, PROG_PATH, USER_PATH, VERSION, PLATFORM)
    if EXIT_ON_WINDOW_CLOSE:
        shutdown()


main()
