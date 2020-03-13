import ms
from pynput import keyboard
from pynput.keyboard import KeyCode, Controller as KeyboardController

pressed = set()
keyboard_controller = KeyboardController()

media_key_map = {
    "vol_up": "media_volume_up",
    "vol_down": "media_volume_down",
    "mute": "media_volume_mute",
    "play_pause": "media_play_pause",
    "prev_track": "media_previous",
    "next_track": "media_next",
    "mouse_left": "left",
    "mouse_middle": "middle",
    "mouse_right": "right"
}


def sp(name):
    return _sp_pynput(name)


def _sp_pynput(name):
    # This is safe because we know the names in the pynput lib
    if name in media_key_map:
        name = media_key_map[name]

    try:
        return keyboard.Key[name]
    except KeyError:
        try:
            return KeyCode.from_char(name)
        except KeyError:
            return None


def press(key):
    pressed.add(key)
    if type(key) == str:
        if "mouse_" in key:
            ms.press(key[6:])
            return
    keyboard_controller.press(key)


def release(key):
    pressed.discard(key)
    if type(key) == str:
        if "mouse_" in key:
            ms.release(key[6:])
            return
    keyboard_controller.release(key)


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
    keyboard_controller.type(string)
