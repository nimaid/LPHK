try:
    import launchpad_py as launchpad
except ImportError:
    try:
        import launchpad
    except ImportError:
        sys.exit("[LPHK] Error loading launchpad.py")

lp = launchpad.Launchpad()


if lp.Check( 0, "mk2" ):
    lp = launchpad.LaunchpadMk2()
    if lp.Open( 0, "mk2" ):
        print('Connected to MkII! Yay!')
    else:
        raise Exception('MkII detected, but connection failed!')
elif lp.Check( 0, "pro" ):
    lp = launchpad.LaunchpadPro()
    if lp.Open( 0, "pro" ):
        print('Connected to Pro! Yay!')
    else:
        raise Exception('Pro detected, but connection failed!')
elif lp.Check( 0, "control xl" ) or lp.Check( 0, "launchkey" ) or lp.Check( 0, "dicer" ):
    raise Exception('Unsupported device detected!')
elif lp.Check():
    if lp.Open():
        print('Connected to Classic/Mini/S! Yay!')
    else:
        raise Exception('Classic/Mini/S detected, but connection failed!')
else:
    raise Exception('Launchpad appears to be unplugged!')

input("Press Enter to exit...")
