import sys, os
from datetime import datetime

PROG_PATH = os.path.dirname(os.path.abspath(__file__))

USER_MAINDIR = os.path.expanduser("~")

LOG_TITLE = "LPHK.log"

# Test if this is a PyInstaller EXE or a .py file
if getattr(sys, 'frozen', False):
    is_exe = True
    PATH = sys._MEIPASS
else:
    is_exe = False
    PATH = PROG_PATH

# Test if this is an installed version of LPHK
if os.path.exists(os.path.join(PROG_PATH, "INSTALLED")):
	INSTALLED = True
	USER_PATH = os.path.join(USER_MAINDIR, "LPHK")
	os.makedirs(USER_PATH, exist_ok=True)
else:
	INSTALLED = False
	USER_PATH = PROG_PATH

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

print("LPHK - LaunchPad HotKey - A Novation Launchpad Macro Scripting System")
print("!!!!!!!! DO NOT CLOSE THIS WINDOW WITHOUT SAVING !!!!!!!!")
print("-------- BEGIN LOG", datetime_str(), "--------\n")

EXIT_ON_WINDOW_CLOSE = True

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

def init():
    global EXIT_ON_WINDOW_CLOSE
    if len(sys.argv) > 1:
        if ("--debug" in sys.argv) or ("-d" in sys.argv):
            EXIT_ON_WINDOW_CLOSE = False
            print("[LPHK] Debugging mode active! Will not shut down on window close.")
            print("[LPHK] Run shutdown() to manually close the program correctly.")

        else:
            print("[LPHK] Invalid argument: " + sys.argv[1] + ". Ignoring...")

    files.init(PATH)
    sound.init(PATH)

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
        if is_exe:
            os.startfile(sys.argv[0])
        else:
            os.execv(sys.executable, ["\"" + sys.executable + "\""] + sys.argv)
    sys.exit("[LPHK] Shutting down...")

def main():
    init()
    window.init(lp, launchpad, PATH, PROG_PATH, USER_PATH)
    if EXIT_ON_WINDOW_CLOSE:
        shutdown()

main()
