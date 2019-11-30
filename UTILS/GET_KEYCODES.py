import keyboard

def press_callback(event):
    print("Name: '" + event.name + "', Scan Code: '" + str(keyboard.key_to_scan_codes(event.name)[0]) + "'")

keyboard.on_press(press_callback)

