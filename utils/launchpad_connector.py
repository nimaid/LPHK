import launchpad_py as launchpad

MK2_NAME = "Launchpad MK2"
MK3MINI_NAME = "LPMiniMK3"
PRO_NAME = "Launchpad Pro"
CTRL_XL_NAME = "control xl"
LAUNCHKEY_NAME = "launchkey"
DICER_NAME = "dicer"

PAD_MODES = {
    launchpad.Launchpad: "Mk1",
    launchpad.LaunchpadMk2: "Mk2",
    launchpad.LaunchpadPro: "Pro",
}
PAD_TEXT = {
    launchpad.Launchpad: "Classic/Mini/S",
    launchpad.LaunchpadMk2: "MkII",
    launchpad.LaunchpadPro: "Pro (BETA)",
}


def get_launchpad():
    lp = launchpad.Launchpad()

    if lp.Check(0, MK2_NAME) or lp.Check(0, MK3MINI_NAME):
        return launchpad.LaunchpadMk2()
    if lp.Check(0, PRO_NAME):
        return launchpad.LaunchpadPro()

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
    return pad.Open()


def disconnect(pad):
    pad.Close()
