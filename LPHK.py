import sys

try:
    import launchpad_py as launchpad
except ImportError:
    try:
        import launchpad
    except ImportError:
        sys.exit("[launchpad_py] Error loading launchpad.py")

import lp_events, lp_colors, scripts, keyboard, files, parse

lp = launchpad.LaunchpadMk2();

def init():
    lp.ButtonFlush()
    files.init(sys.path[0])
    lp_events.start(lp)

def main():
    if lp.Open(0, "mk2"):
        print("[LPHK] Connected to Launchpad Mk2!")
    else:
        print("[LPHK] Could not connect to Launchpad Mk2, exiting...")
        return

    init()

    files.load_layout("default")

main()

