import ctypes
from ctypes import wintypes
import pyautogui

# code in this file comes from https://gist.github.com/Aniruddha-Tapas/1627257344780e5429b10bc92eb2f52a

user32 = ctypes.WinDLL('user32', use_last_error=True)

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_SCANCODE = 0x0008

MAPVK_VK_TO_VSC = 0

# C struct definitions

wintypes.ULONG_PTR = wintypes.WPARAM


class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx", wintypes.LONG),
                ("dy", wintypes.LONG),
                ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk", wintypes.WORD),
                ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg", wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))


class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))

    _anonymous_ = ("_input",)
    _fields_ = (("type", wintypes.DWORD),
                ("_input", _INPUT))


LPINPUT = ctypes.POINTER(INPUT)


# Functions

def press_key(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def release_key(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


# List of all codes for keys:
# https://msdn.microsoft.com/en-us/library/dd375731
key_map = {
    "alt": 0x12,
    "alt_gr": 0x12,  # TODO: find a way to send two keys

    "apps": 0x5D,

    "backspace": 0x08,
    "caps_lock": 0x14,

    # cmd and win keys are the same
    "cmd": 0x5B,
    "win": 0x5B,
    "win_r": 0x5C,

    "ctrl": 0x11,
    "ctrl_l": 0xA2,
    "ctrl_r": 0xA3,

    "delete": 0x2E,

    "down": 0x28,
    "end": 0x23,
    "enter": 0x0D,
    "esc": 0x1B,

    "f1": 0x70,
    "f2": 0x71,
    "f3": 0x72,
    "f4": 0x73,
    "f5": 0x74,
    "f6": 0x75,
    "f7": 0x76,
    "f8": 0x77,
    "f9": 0x78,
    "f10": 0x79,
    "f11": 0x7A,
    "f12": 0x7B,
    "f13": 0x7C,
    "f14": 0x7D,
    "f15": 0x7E,
    "f16": 0x7F,
    "f17": 0x80,
    "f18": 0x81,
    "f19": 0x82,
    "f20": 0x83,
    "f21": 0x84,
    "f22": 0x85,
    "f23": 0x86,
    "f24": 0x87,

    "home": 0x24,
    "insert": 0x2D,
    "left": 0x25,

    "menu": 0xA4,  # left menu key
    "menu_r": 0xA5,

    "mute": 0xAD,
    "next_track": 0xB0,
    "num_lock": 0x90,
    "page_down": 0x22,
    "page_up": 0x21,
    "pause": 0x13,
    "play_pause": 0xB3,
    "prev_track": 0xB1,
    "print_screen": 0x2C,
    "right": 0x27,
    "scroll_lock": 0x91,

    "shift": 0x10,
    "shift_l": 0xA0,
    "shift_r": 0xA1,

    "space": 0x20,
    "tab": 0x09,
    "up": 0x26,
    "vol_down": 0xAE,
    "vol_up": 0xAF,

    "0": 0x30,
    "1": 0x31,
    "2": 0x32,
    "3": 0x33,
    "4": 0x34,
    "5": 0x35,
    "6": 0x36,
    "7": 0x37,
    "8": 0x38,
    "9": 0x39,

    "num0": 0x60,
    "num1": 0x61,
    "num2": 0x62,
    "num3": 0x63,
    "num4": 0x64,
    "num5": 0x65,
    "num6": 0x66,
    "num7": 0x67,
    "num8": 0x68,
    "num9": 0x69,

    "a": 0x41,
    "b": 0x42,
    "c": 0x43,
    "d": 0x44,
    "e": 0x45,
    "f": 0x46,
    "g": 0x47,
    "h": 0x48,
    "i": 0x49,
    "j": 0x4A,
    "k": 0x4B,
    "l": 0x4C,
    "m": 0x4D,
    "n": 0x4E,
    "o": 0x4F,
    "p": 0x50,
    "q": 0x51,
    "r": 0x52,
    "s": 0x53,
    "t": 0x54,
    "u": 0x55,
    "v": 0x56,
    "w": 0x57,
    "x": 0x58,
    "y": 0x59,
    "z": 0x5A,

    "+": 0x6B,
    "-": 0xBD,
    "=": 0xBB,
    ".": 0xBE,
    ",": 0xBC,
    "*": 0x6A,
    "]": 0xDD,
    "[": 0xDB,
    ";": 0xBA,
    "'": 0xDE,
    "\\": 0xDC,
    "`": 0xC0,
}


def sp(name):
    if name in key_map:
        return key_map[name]

    return None


def press(key):
    press_key(key)


def release(key):
    release_key(key)


def write(string):
    pyautogui.write(string)
