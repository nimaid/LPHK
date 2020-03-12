# Shush pycharm
# noinspection PyUnresolvedReferences
import launchpad_connector as lpcon

from getch import pause

MK2_NAME = "Launchpad MK2"
MK3MINI_NAME = "LPMiniMK3"
PRO_NAME = "Launchpad Pro"
CTRL_XL_NAME = "control xl"
LAUNCHKEY_NAME = "launchkey"
DICER_NAME = "dicer"

print("\nTrying to connect to launchpad...")

launchpad = lpcon.get_launchpad()

if launchpad is -1:
    print('Unsupported device detected!')
elif launchpad is None:
    print('Launchpad appears to be unplugged!')
else:
    name = lpcon.get_display_name(launchpad)
    if lpcon.connect(launchpad):
        print(f'Connected to {name}! Yay!')
    else:
        print(f'{name} detected, but connection failed!')


pause("\nPress any key to exit...")
lpcon.disconnect(launchpad)
