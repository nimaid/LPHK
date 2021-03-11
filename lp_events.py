import copy, threading, time
import lp_colors

RUN_DELAY = 0.005 #0.005 == 200 FPS

def unbound_press(x, y):
    print("[lp_events] ("+str(x)+", "+str(y)+") Unbound button...")


press_funcs = [[unbound_press for y in range(9)] for x in range(9)]
pressed = [[False for y in range(9)] for x in range(9)]

timer = None # This is a global variable that is continually overwritten with the current timer event.
             # I'm not happy that this is the safest way of doing this, but so far it seems to have
             # worked.  The fact that we're using threads rather than different processes probably
             # allows us to get away with what is strictly not thread-safe logic.

# initialise an object by creating a timer object for it (but not starting it)
def init(lp_object):
    global timer
    global press_funcs
    timer = threading.Timer(RUN_DELAY, run, (lp_object,))

# "run" an object (a button) after a delay
def run(lp_object):
    global timer
    while True:                            # loop forever
        event = lp_object.ButtonStateXY()  # get a pending event
        if event != []:                    # if there is an event
            x = event[0]                   # determine the button it is
            y = event[1]
            if event[2] == 0:              # is this button released?
                pressed[x][y] = False
            else:                          # I presume this is "button pressed"
                pressed[x][y] = True
                press_funcs[x][y](x, y)    # do whatever you need to do with a pressed button
            lp_colors.updateXY(x, y)       # and update the button colour
        else:                              # but if there's no event pending
            break                          # break out of the loop
    init(lp_object)                        # and schedule this button to run after the delay
    timer.start()

# "start" an object by initialising it then running it.
def start(lp_object):
    lp_colors.init(lp_object)   # assign this to a global (what?!)
    init(lp_object)             # create the timer object for this lp_object (button)
    run(lp_object)              # "run" the object (why not just start the timer?)
    lp_colors.update_all()      # update all the colours after exiting

def bind_func_with_colors(x, y, func, off_color):
    global press_funcs
    press_funcs[x][y] = func
    lp_colors.setXY(x, y, off_color)

def unbind(x, y):
    global press_funcs
    press_funcs[x][y] = unbound_press
    lp_colors.setXY(x, y, [0,0,0])
    lp_colors.updateXY(x, y)

def unbind_all():
    global press_funcs
    press_funcs = [[unbound_press for y in range(9)] for x in range(9)]
    for x in range(9):
        for y in range(9):
            lp_colors.setXY(x, y, [0,0,0])
    lp_colors.raw_clear()

