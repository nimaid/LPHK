try:
    import launchpad_py as launchpad
except ImportError:
    try:
        import launchpad
    except ImportError:
        sys.exit("[LPHK] Error loading launchpad.py")

from getch import pause

MK2_NAME = "Launchpad MK2"
MK3MINI_NAME = "LPMiniMK3"
PRO_NAME = "Launchpad Pro"
CTRL_XL_NAME = "control xl"
LAUNCHKEY_NAME = "launchkey"
DICER_NAME = "dicer"

print("\nTrying to connect to launchpad...")

lp = launchpad.Launchpad()

if lp.Check( 0, MK2_NAME ) or lp.Check( 0, MK3MINI_NAME ):
    lp = launchpad.LaunchpadMk2()
    if lp.Open( 0, MK2_NAME ):
        print('Connected to MkII/Mini Mk3! Yay!')
    else:
        print('MkII/Mini Mk3 detected, but connection failed!')
elif lp.Check( 0, PRO_NAME ):
    lp = launchpad.LaunchpadPro()
    if lp.Open( 0, PRO_NAME ):
        print('Connected to Pro! Yay!')
    else:
        print('Pro detected, but connection failed!')
elif lp.Check( 0, CTRL_XL_NAME ) or lp.Check( 0, LAUNCHKEY_NAME ) or lp.Check( 0, DICER_NAME ):
    print('Unsupported device detected!')
elif lp.Check():
    if lp.Open():
        print('Connected to Classic/Mini/S! Yay!')
    else:
        print('Classic/Mini/S detected, but connection failed!')
else:
    print('Launchpad appears to be unplugged!')

pause("\nPress any key to exit...")
