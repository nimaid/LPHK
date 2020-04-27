from pynput import keyboard
from pynput.keyboard import KeyCode, Controller as KeyboardController

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

media_key_map_pyautogui = {
    "alt": "alt",
    "alt_gr": "altright",
    "shift_r": "shiftright",
    "scroll_lock": "scrolllock",
    "print_screen": "printscreen",
    "page_up": "pgup",
    "page_down": "pgdn",
    "num_lock": "numlock",
    "vol_up": "volumeup",
    "vol_down": "volumedown",
    "mute": "volumemute",
    "play_pause": "playpause",
    "prev_track": "prevtrack",
    "next_track": "nexttrack",
    "mouse_left": "left",
    "mouse_middle": "middle",
    "mouse_right": "right"
}


def sp(name):
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
    keyboard_controller.press(key)


def release(key):
    keyboard_controller.release(key)


def write(string):
    keyboard_controller.type(string)
