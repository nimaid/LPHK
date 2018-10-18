import threading
from functools import partial
import lp_events, lp_colors, keyboard

COLOR_ACTIVE = lp_colors.BLUE
COLOR_PRIMED = lp_colors.PINK

script_threads = [[None for y in range(9)] for x in range(9)]
script_running = False
scripts_to_run = []

def run_in_bg(func, x, y):
    global script_threads
    global scripts_to_run
    if not script_running:
        script_threads[x][y] = threading.Thread(None, func)
        script_threads[x][y].start()
    else:
        scripts_to_run.append((func, x, y))

def run_funcs(funcs_in):
    global script_running
    global scripts_to_run
    script_running = True
    for f in funcs_in:
        f()
    script_running = False
    if len(scripts_to_run) > 0:
        tup = scripts_to_run.pop(0)
        func = tup[0]
        x = tup[1]
        y = tup[2]
        run_in_bg(func, x, y)
    threading.Timer(0.01, lp_colors.update, ()).start()

def run_script(script_str, x, y):
    script_lines = script_str.split('\n')
    funcs_to_run = []
    for line in script_lines:
        split_line = line.split(' ')
        if split_line[0] == "STRING":
            funcs_to_run.append(partial(keyboard.controller.type, (" ".join(split_line[1:]))))
        elif split_line[0] == "DELAY":
            funcs_to_run.append(partial(sleep, (float(split_line[1]))))
        elif split_line[0] == "TAP":
            funcs_to_run.append(partial(keyboard.tap, (split_line[1])))
        elif split_line[0] == "PRESS":
            funcs_to_run.append(partial(keyboard.controller.press, (split_line[1])))
        elif split_line[0] == "RELEASE":
            funcs_to_run.append(partial(keyboard.controller.release, (split_line[1])))
        elif split_line[0] == "SP_TAP":
            if keyboard.sp(split_line[1]) != None:
                funcs_to_run.append(partial(keyboard.tap, (keyboard.sp(split_line[1]))))
        elif split_line[0] == "SP_PRESS":
            if keyboard.sp(split_line[1]) != None:
                funcs_to_run.append(partial(keyboard.controller.press, (keyboard.sp(split_line[1]))))
        elif split_line[0] == "SP_RELEASE":
            if keyboard.sp(split_line[1]) != None:
                funcs_to_run.append(partial(keyboard.controller.release, (keyboard.sp(split_line[1]))))
    script_func = partial(run_funcs, (funcs_to_run))
    run_in_bg(script_func, x, y)

def bind_script_to_button(x, y, script_down, off_color):
    script_down_bindable = lambda a, b : run_script(script_down, x, y)
    lp_events.bind_func_with_colors(x, y, script_down_bindable, off_color, COLOR_ACTIVE)
