import sys

SCRIPT_QBF = "STRING The Quick Brown Fox\nSP_TAP enter"
SCRIPT_HW = "STRING echo \"Hello, world!\"\nSP_TAP enter"
SCRIPT_YT = "WEB youtube.com"
SCRIPT_IDC = "WEB_NEW tv.nimaid.com\nDELAY 2\nSP_TAP f11"
SCRIPT_TERM = "SP_PRESS ctrl\nSP_PRESS alt\nTAP t 0.1\nSP_RELEASE alt\nSP_RELEASE ctrl"
SCRIPT_SPACE = "SP_TAP space"
SCRIPT_F11 = "SP_TAP f11"
SCRIPT_DEV = "SP_PRESS ctrl\nSP_PRESS shift\nTAP j\nSP_RELEASE shift\nSP_RELEASE ctrl"

try:
    import launchpad_py as launchpad
except ImportError:
    try:
        import launchpad
    except ImportError:
        sys.exit("[launchpad_py] Error loading launchpad.py")

import lp_events, lp_colors, scripts, keyboard

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

    scripts.bind(0, 1, SCRIPT_YT, lp_colors.RED_THIRD)
    scripts.bind(0, 2, SCRIPT_QBF, lp_colors.AMBER_THIRD)

    scripts.bind(1, 1, SCRIPT_IDC, lp_colors.WHITE_THIRD)
    scripts.bind(1, 2, SCRIPT_SPACE, lp_colors.RED_THIRD)
    scripts.bind(1, 3, SCRIPT_F11, lp_colors.YELLOW_THIRD)
    scripts.bind(1, 4, SCRIPT_DEV, lp_colors.MINT_THIRD)

    scripts.bind(2, 1, SCRIPT_TERM, lp_colors.PURPLE_THIRD)
    scripts.bind(2, 2, SCRIPT_HW, lp_colors.PINK_THIRD)

main()

