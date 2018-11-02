#! /usr/bin/python3

import sys

EXIT_ON_WINDOW_CLOSE = True

try:
    import launchpad_py as launchpad
except ImportError:
    try:
        import launchpad
    except ImportError:
        sys.exit("[LPHK] Error loading launchpad.py")

import lp_events, scripts, keyboard, files, sound, window

PATH = sys.path[0]

lp = launchpad.LaunchpadMk2()

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
    if window.lp_connected:
        scripts.unbind_all()
        lp_events.timer.cancel()
        lp.Close()
    sys.exit("[LPHK] Sutting down...")

def main():
    init()
    window.init(lp)
    if EXIT_ON_WINDOW_CLOSE:
        shutdown()

main()
