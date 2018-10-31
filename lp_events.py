import copy, threading, time
import lp_colors

RUN_DELAY = 0.005 #0.005 == 200 FPS

def unbound_press(x, y):
    print("[lp_events] NOTHING BOUND TO BUTTON ("+str(x)+", "+str(y)+")")


press_funcs = [[unbound_press for y in range(9)] for x in range(9)]
pressed = [[False for y in range(9)] for x in range(9)]

timer = None

def init(lp_object):
    global timer
    timer = threading.Timer(RUN_DELAY, run, [lp_object])

def run(lp_object):
    global timer
    while True:
        event = lp_object.ButtonStateXY()
        if event != []:
            if event[2] == 0:
                pressed[event[0]][event[1]] = False
            else:
                pressed[event[0]][event[1]] = True
                press_funcs[event[0]][event[1]](event[0], event[1])
            lp_colors.update()
        else:
            break
    init(lp_object)
    timer.start()

def start(lp_object):
    lp_colors.init(lp_object)
    init(lp_object)
    run(lp_object)
    lp_colors.update()

def bind_func_with_colors(x, y, func, off_color):
    global press_funcs
    press_funcs[x][y] = func
    lp_colors.setXY(x, y, off_color)

def unbind(x, y):
    global press_funcs
    press_funcs[x][y] = unbound_press
    lp_colors.setXY(x, y, lp_colors.BLACK)
    lp_colors.update()

def unbind_all():
    global press_funcs
    press_funcs = [[unbound_press for y in range(9)] for x in range(9)]
    for x in range(9):
        for y in range(9):
            lp_colors.setXY(x, y, lp_colors.BLACK)
    lp_colors.update()
