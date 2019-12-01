import sys, os, subprocess
from datetime import datetime

print("\n!!!!!!!! DO NOT CLOSE THIS WINDOW WITHOUT SAVING !!!!!!!!\n")

LOG_TITLE = "LPHK.log"

# Test if this is a PyInstaller EXE or a .py file
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

# Test if there is a user folder specifiedUSER_PATH
USER_PATH = None
USERPATH_FILE = os.path.join(PROG_PATH, "USERPATH")
if os.path.exists(USERPATH_FILE):
    IS_PORTABLE = False
    with open(USERPATH_FILE, "r") as f:
        USER_PATH = f.read().strip().replace("\n", "")
    os.makedirs(USER_PATH, exist_ok=True)
else:
    IS_PORTABLE = True
    USER_PATH = PROG_PATH

# Get program version
with open(os.path.join(PATH, "VERSION"), "r") as f:
    VERSION = f.read().strip().replace("\n", "")

# Setup dual logging/printing
class Tee(object):
    def __init__(self, name, mode):
        self.file = open(name, mode)
        self.stdout = sys.stdout
        sys.stdout = self
    def __del__(self):
        sys.stdout = self.stdout
        self.file.close()
    def write(self, data):
        self.file.write(data)
        self.file.flush()
        self.stdout.write(data)
    def flush(self):
        self.file.flush()

log_path = os.path.join(USER_PATH, LOG_TITLE)
logger = Tee(log_path, 'w')

# Start printing output
def datetime_str():
   now = datetime.now()
   return now.strftime("%d/%m/%Y %H:%M:%S")

print("-------- BEGIN LOG", datetime_str(), "--------")
print("LPHK - LaunchPad HotKey - A Novation Launchpad Macro Scripting System")
print("Version:", VERSION)
print("Is compiled executable:", IS_EXE)
print("Is portable:", IS_PORTABLE)
print("Operating path:", PATH)
print("User path:", USER_PATH)
print("Program main file:", PROG_FILE)
print("Program main file path:", PROG_PATH, end="\n\n")

# Try to import launchpad.py
try:
    import launchpad_py as launchpad
except ImportError:
    try:
        import launchpad
    except ImportError:
        sys.exit("[LPHK] Error loading launchpad.py")

import lp_events, scripts, kb, files, sound, window

lp = launchpad.Launchpad()

EXIT_ON_WINDOW_CLOSE = True
def init():
    global EXIT_ON_WINDOW_CLOSE
    if len(sys.argv) > 1:
        if ("--debug" in sys.argv) or ("-d" in sys.argv):
            EXIT_ON_WINDOW_CLOSE = False
            print("[LPHK] Debugging mode active! Will not shut down on window close.")
            print("[LPHK] Run shutdown() to manually close the program correctly.")

        else:
            print("[LPHK] Invalid argument: " + sys.argv[1] + ". Ignoring...")

    sound.init(USER_PATH)

def shutdown():
    if lp_events.timer != None:
        lp_events.timer.cancel()
    scripts.to_run = []
    for x in range(9):
        for y in range(9):
            if scripts.threads[x][y] != None:
                scripts.threads[x][y].kill.set()
    if window.lp_connected:
        scripts.unbind_all()
        lp_events.timer.cancel()
        lp.Close()
        window.lp_connected = False
    if window.restart:
        if IS_EXE:
            os.startfile(sys.argv[0])
        else:
            os.execv(sys.executable, ["\"" + sys.executable + "\""] + sys.argv)
    sys.exit("[LPHK] Shutting down...")

def main():
    init()
    window.init(lp, launchpad, PATH, PROG_PATH, USER_PATH, VERSION)
    if EXIT_ON_WINDOW_CLOSE:
        shutdown()

main()
