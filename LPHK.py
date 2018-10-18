import sys

SCRIPT_QBF = "STRING The Quick Brown Fox Jumps Over The Lazy Dog\nSP_TAP enter"

try:
    import launchpad_py as launchpad
except ImportError:
    try:
        import launchpad
    except ImportError:
        sys.exit("[launchpad_py] Error loading launchpad.py")

import lp_events, lp_colors, keyboard

lp = launchpad.LaunchpadMk2();

def init():
    lp.ButtonFlush()
    lp_events.start(lp)

def main():
    if lp.Open(0, "mk2"):
        print("[LPHK] Connected to Launchpad Mk2!")
    else:
        print("[LPHK] Could not connect to Launchpad Mk2, exiting...")
        return

    init()

    keyboard.bind_script_to_button(0, 1, SCRIPT_QBF, lp_colors.AMBER)

main()

