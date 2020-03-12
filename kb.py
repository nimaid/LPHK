import ms
from pynput import keyboard
from pynput.keyboard import KeyCode, Controller

media_keys = {
    "vol_up": 57392,
    "vol_down": 57390,
    "mute": 57376,
    "play_pause": 57378,
    "prev_track": 57360,
    "next_track": 57369,
    "mouse_left": "mouse_left",
    "mouse_middle": "mouse_middle",
    "mouse_right": "mouse_right"
}

pressed = set()
controller = Controller()


def sp(name):
    try:
        # return keyboard.key_to_scan_codes(str(name))[0]
        # return KeyCode.from_char(name)
        return keyboard.Key[name]
    except KeyError as e:
        print(str(e))
        try:
            # return keyboard.KeyCode[name]
            return KeyCode.from_char(name)
        except KeyError as e2:
            print(str(e2))
            return None


def press(key):
    print(key)

    pressed.add(key)
    if type(key) == str:
        if "mouse_" in key:
            ms.press(key[6:])
            return
    controller.press(key)


def release(key):
    pressed.discard(key)
    if type(key) == str:
        if "mouse_" in key:
            ms.release(key[6:])
            return
    controller.release(key)


def release_all():
    for key in pressed.copy():
        release(key)


def tap(key):
    if type(key) == str:
        if "mouse_" in key:
            ms.click(key[6:])
            return
    press(key)
    release(key)


def write(string):
    controller.type(string)
