import keyboard

media_keys = {"vol_up" : 57392, "vol_down" : 57390, "mute" : 57376, "play_pause" : 57378, "prev_track" : 57360, "next_track" : 57369}


def sp(name):
    try:
        return keyboard.key_to_scan_codes(str(name))[0]
    except:
        try:
            return media_keys[str(name)]
        except:
            return None

def press(key):
    keyboard.press(key)

def release(key):
    keyboard.release(key)

def tap(key):
    press(key)
    release(key)

