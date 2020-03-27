import ms
from pynput import keyboard
from pynput.keyboard import KeyCode, Controller as KeyboardController
import pyautogui
from pyautogui import KEY_NAMES as pyautogui_keys

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
    return _sp_pyautogui(name)


def _sp_pyautogui(name):
    if name in media_key_map_pyautogui:
        name = media_key_map_pyautogui[name]

    if name in pyautogui_keys:
        return name

    return None


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
    # keyboard_controller.press(key)
    pyautogui.keyDown(key)


def release(key):
    pressed.discard(key)
    if type(key) == str:
        if "mouse_" in key:
            ms.release(key[6:])
            return
    # keyboard_controller.release(key)
    pyautogui.keyUp(key)


def release_all():
    for key in pressed.copy():
        release(key)


def tap(key):
    if type(key) == str:
        if "mouse_" in key:
            ms.click(key[6:])
            return
    # press(key)
    # release(key)
    pyautogui.press(key)


def write(string):
    # keyboard_controller.type(string)
    pyautogui.write(string)
