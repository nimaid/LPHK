try:
    import launchpad_py as launchpad
except ImportError:
    try:
        import launchpad
    except ImportError:
        sys.exit("[LPHK] Error loading launchpad.py")

from getch import pause

lp = launchpad.Launchpad()

print("\nListing all MIDI devices...")
lp.ListAll()

pause("\nPress any key to exit...")
