import sys

EXIT_ON_WINDOW_CLOSE = True

try:
    import launchpad_py as launchpad
except ImportError:
    try:
        import launchpad
    except ImportError:
        sys.exit("[launchpad_py] Error loading launchpad.py")

import lp_events, lp_colors, scripts, keyboard, files, parse, sound, window

PATH = sys.path[0]

lp = launchpad.LaunchpadMk2();

def init():
    global EXIT_ON_WINDOW_CLOSE
    if len(sys.argv) > 1:
        if (sys.argv[1] == "--debug") or (sys.argv[1] == "-d"):
            EXIT_ON_WINDOW_CLOSE = False
            print("[LPHK] Debugging mode active! Will not shut down on window close.")
            print("[LPHK] Run shutdown() to manually close the program correctly.")

        else:
            print("[LPHK] Invalid argument: " + sys.argv[1] + ". Ignoring...")

    lp.ButtonFlush()
    files.init(PATH)
    sound.init(PATH)
    lp_events.start(lp)

def shutdown():
    scripts.unbind_all()
    lp_events.timer.cancel()
    lp.Close()
    sys.exit("[LPHK] Sutting down...")

def main():
    if lp.Open(0, "mk2"):
        print("[LPHK] Connected to Launchpad Mk2!")
    else:
        print("[LPHK] Could not connect to Launchpad Mk2, exiting...")
        return

    init()
    window.make()
    if EXIT_ON_WINDOW_CLOSE:
        shutdown()

main()
