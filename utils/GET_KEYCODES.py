import pyautogui
from pynput import keyboard
from time import sleep


def press_callback(key):
    # print("Name: '" + event.name + "', Scan Code: '" + str(keyboard.key_to_scan_codes(event.name)[0]) + "'")
    print('{0} pressed'.format(key))

    if hasattr(key, 'vk'):
        print('vk code {0} pressed'.format(key.vk))


def release_callback(key):
    print('{0} released'.format(key))


listener = keyboard.Listener(
    on_press=press_callback,
    on_release=release_callback)
listener.start()

print("Reading keys. Press CTRL-C to exit...")


while True:
    sleep(60)
