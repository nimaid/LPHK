import launchpad_py as launchpad

MK2_NAME = "Launchpad MK2"
# MK3MINI_NAME = "LPMiniMK3"
MK3MINI_NAME = "minimk3"
PRO_NAME = "Launchpad Pro"
LPX_NAME = "lpx"
CTRL_XL_NAME = "control xl"
LAUNCHKEY_NAME = "launchkey"
DICER_NAME = "dicer"

PAD_MODES = {
    launchpad.Launchpad: "Mk1",
    launchpad.LaunchpadMk2: "Mk2",
    launchpad.LaunchpadMiniMk3: "Mk3",
    launchpad.LaunchpadPro: "Pro",
    launchpad.LaunchpadLPX: "Mk3"
}
PAD_TEXT = {
    launchpad.Launchpad: "Classic/Mini/S",
    launchpad.LaunchpadMk2: "MkII",
    launchpad.LaunchpadMiniMk3: "Mk3",
    launchpad.LaunchpadPro: "Pro (BETA)",
    launchpad.LaunchpadLPX: "LPX"
}


def get_launchpad():
    lp = launchpad.Launchpad()

    if lp.Check(0, MK2_NAME):
        return launchpad.LaunchpadMk2()
    # the MK3 has two midi devices, we need the second one
    if lp.Check(1, MK3MINI_NAME):
        return launchpad.LaunchpadMiniMk3()
    if lp.Check(0, PRO_NAME):
        return launchpad.LaunchpadPro()
    if lp.Check(1, LPX_NAME):
        return launchpad.LaunchpadLPX()

    # unsupported pads
    if lp.Check(0, CTRL_XL_NAME) or lp.Check(0, LAUNCHKEY_NAME) or lp.Check(0, DICER_NAME):
        return -1

    if lp.Check():
        return lp

    return None


def get_mode(pad):
    cls = type(pad)

    if cls not in PAD_MODES:
        return None

    return PAD_MODES[cls]


def get_display_name(pad):
    cls = type(pad)

    if cls not in PAD_TEXT:
        return "Unsupported"

    return PAD_TEXT[cls]


def connect(pad):
    mode = get_mode(pad)

    if mode == "Mk3":
        return pad.Open(1)

    return pad.Open()


def disconnect(pad):
    mode = get_mode(pad)
    
    if mode == "Mk3":
        pad.LedSetMode(0)
    
    pad.Close()
