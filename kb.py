import ms
import sys

if sys.platform == 'win32':
    import system_apis.keyboard_win as keyboard_api
else:
    import system_apis.keyboard_unix as keyboard_api

pressed = set()


def sp(name):
    return keyboard_api.sp(name)


def press(key):
    pressed.add(key)
    if type(key) == str:
        if "mouse_" in key:
            ms.press(key[6:])
            return
    keyboard_api.press(key)


def release(key):
    pressed.discard(key)
    if type(key) == str:
        if "mouse_" in key:
            ms.release(key[6:])
            return
    keyboard_api.release(key)


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
    keyboard_api.write(string)
