import ms
import sys

if sys.platform == 'win32':
    import system_apis.keyboard_win as keyboard_api
else:
    import system_apis.keyboard_unix as keyboard_api

pressed = set()


# convert key name to format ready for use
def sp(name):
    if "mouse_" in name:
        return name                # mouse keys are strings

    return keyboard_api.sp(name)   # real keys are keycodes of some sort


# to press a key
def press(key):
    pressed.add(key)               # add to the list of pressed keys
    if type(key) == str:           # if the key desciption is a string
        if "mouse_" in key:        # assume (but check that it's a mouse key)
            ms.press(key[6:])      # then strip "mouse_" and press it
            return
    keyboard_api.press(key)        # otherwise press the key by keycode


# to release a key
def release(key):
    pressed.discard(key)           # remove it from the list of pressed keys
    if type(key) == str:           # if the key desciption is a string
        if "mouse_" in key:        # assume (but check that it's a mouse key)
            ms.release(key[6:])    # then strip "mouse_" and release it
            return
    keyboard_api.release(key)      # otherwise release the key by keycode


# release all keys resorded as pressed
def release_all():
    for key in pressed.copy():     # for each key recorded as pressed (in no particular order)
        release(key)               # release the key

        
# tap a key
def tap(key):
    if type(key) == str:           # if it's a str
        if "mouse_" in key:        # assume (but check that it's a mouse key)
            ms.click(key[6:])      # "click" the mouse button
            return
    press(key)                     # otherwise press...
    release(key)                   # ...and immendiately release the key


# pretend we're typing
def write(string):
    keyboard_api.write(string)     # Emulates typing the contents of the string
