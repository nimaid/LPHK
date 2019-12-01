import keyboard
import ms

media_keys = {"vol_up" : 57392, "vol_down" : 57390, "mute" : 57376, "play_pause" : 57378, "prev_track" : 57360, "next_track" : 57369, "mouse_left" : "mouse_left","mouse_middle" : "mouse_middle", "mouse_right" : "mouse_right"}

pressed = set()

def sp(name):
    try:
        return keyboard.key_to_scan_codes(str(name))[0]
    except ValueError:
        try:
            return media_keysa[str(name)]
        except KeyError:
            return None
    except:
        print("[KB] Error while processing key", name)
        raise

def press(key):
    pressed.add(key)
    if type(key) == str:
        if "mouse_" in key:
            ms.press(key[6:])
            return
    keyboard.press(key)

def release(key):
    pressed.discard(key)
    if type(key) == str:
        if "mouse_" in key:
            ms.release(key[6:])
            return
    keyboard.release(key)

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

