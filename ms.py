from pynput.mouse import Controller, Button
from bresenham import bresenham

controller = Controller()
buttons = ["left", "middle", "right"]


def get_pos():
    return controller.position


def set_pos(x, y):
    global controller
    controller.position = (x, y)


def move_to_pos(x, y):
    controller.move(x, y)


def click(button="left", clicks=1):
    _check_button(button)
    controller.click(Button[button], clicks)


def press(button="left"):
    _check_button(button)
    controller.press(Button[button])


def release(button="left"):
    _check_button(button)
    controller.release(Button[button])


def scroll(x, y):
    controller.scroll(x, y)


def line_coords(x1, y1, x2, y2):
    return list(bresenham(x1, y1, x2, y2))


def _check_button(btn):
    if btn not in buttons:
        raise ValueError('The mouse button specified is not valid')

