from pynput.keyboard import Controller, Listener

keyboard = Controller()

def on_press(key):
    print(key)

Listener(on_press=on_press).start()

