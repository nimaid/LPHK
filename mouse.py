from pynput.mouse import Controller, Button

controller = Controller()

def getXY():
    return controller.position

def setXY(x, y):
    global controller
    controller.position = (x, y)

def moveXY(x, y):
    controller.move(x, y)

def click(button="left", clicks=1):
    if button == "left":
        controller.click(Button.left, clicks)
    elif button == "middle":
        controller.click(Button.middle, clicks)
    elif button == "right":
        controller.click(Button.right, clicks)

def press(button="left"):
    if button == "left":
        controller.press(Button.left)
    elif button == "middle":
        controller.press(Button.middle)
    elif button == "right":
        controller.press(Button.right)

def release(button="left"):
    if button == "left":
        controller.release(Button.left)
    elif button == "middle":
        controller.release(Button.middle)
    elif button == "right":
        controller.release(Button.right)

def scroll(x, y):
    controller.scroll(x, y)

