import sys

SCRIPT_QBF = "STRING The Quick Brown Fox Jumps Over The Lazy Dog\nSP_TAP enter"
SCRIPT_HW = "STRING Hello, world!\nSP_TAP enter"
SCRIPT_YT = "STRING youtube.com\nSP_TAP enter"
SCRIPT_TNC = "STRING tv.nimaid.com\nSP_TAP enter"

try:
    import launchpad_py as launchpad
except ImportError:
    try:
        import launchpad
    except ImportError:
        sys.exit("[launchpad_py] Error loading launchpad.py")

import lp_events, lp_colors, scripts

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

    scripts.bind_script_to_button(0, 1, SCRIPT_YT, lp_colors.RED)
    scripts.bind_script_to_button(1, 1, SCRIPT_QBF, lp_colors.AMBER)
    scripts.bind_script_to_button(2, 1, SCRIPT_HW, lp_colors.YELLOW)
    scripts.bind_script_to_button(3, 1, SCRIPT_TNC, lp_colors.LIGHTBLUE)

main()

