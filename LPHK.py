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
class TeeStdout(object):
    def __init__(self, file_in):
        self.file = file_in
        self.stdout = sys.stdout
        sys.stdout = self
    def __del__(self):
        sys.stdout = self.stdout
    def write(self, data):
        self.file.write(data)
        self.file.flush()
        self.stdout.write(data)
    def flush(self):
        self.file.flush()
class TeeStderr(object):
    def __init__(self, file_in):
        self.file = file_in
        self.stderr = sys.stderr
        sys.stderr = self
    def __del__(self):
        sys.stderr = self.stderr
    def write(self, data):
        self.file.write(data)
        self.file.flush()
        self.stderr.write(data)
    def flush(self):
        self.file.flush()

LOG_FILE = None
def start_logging(log_path):
    global LOG_FILE
    LOG_FILE = open(log_path, "w")
    stdout_logger = TeeStdout(LOG_FILE)
    stderr_logger = TeeStderr(LOG_FILE)
    return (stdout_logger, stderr_logger)
def stop_logging(loggers):
    global LOG_FILE
    for logger in loggers:
        logger.__del__()
    LOG_FILE.close()
    LOG_FILE = None

LOG_PATH = os.path.join(USER_PATH, LOG_TITLE)
loggers = start_logging(LOG_PATH)

# Start printing output
def datetime_str():
   now = datetime.now()
   return now.strftime("%d/%m/%Y %H:%M:%S")

print("---------------- BEGIN LOG", datetime_str(), "----------------")
print("LPHK - LaunchPad HotKey - A Novation Launchpad Macro Scripting System")
print("Version:", VERSION)
print("Is compiled executable:", IS_EXE)
print("Is portable:", IS_PORTABLE)
print("Operating path:", PATH)
print("User path:", USER_PATH)
print("Program file path:", PROG_PATH)
print("Program file:", PROG_FILE)
print("Log location (this file):", LOG_PATH, end="\n\n")

# Try to import launchpad.py
try:
    import launchpad_py as launchpad
except ImportError:
    try:
        import launchpad
    except ImportError:
        sys.exit("[LPHK] Error loading launchpad.py")
print("")

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
    stop_logging(loggers)
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
