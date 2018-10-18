from time import sleep
from pynput.keyboard import Key, Controller

controller = Controller()

def sp(name):
    try:
        return getattr(Key, str(name))
    except Exception as e:
        return None

def tap(key, wait=0):
    controller.press(key)
    sleep(wait)
    controller.release(key)

