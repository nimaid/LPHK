import sys, os
from datetime import datetime

# Test if this is a PyInstaller EXE or a .py file
if getattr(sys, 'frozen', False):
    is_exe = True
    PATH = sys._MEIPASS
else:
    is_exe = False
    PATH = os.path.dirname(os.path.abspath(__file__))

# Setup dual logging/printing
class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
f = open('last_session.log', 'w')
backup = sys.stdout
sys.stdout = Tee(sys.stdout, f)

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
    window.init(lp, launchpad, PATH)
    if EXIT_ON_WINDOW_CLOSE:
        shutdown()

main()
