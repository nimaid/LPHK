from time import sleep
import threading
import scripts, lp_colors

DELAY_EXIT_CHECK = 0.025

def safe_delay(delay_time, x=None, y=None):
    if None in [x, y]:
        # If any are not set
        print("NORMAL DELAY")
        sleep(delay_time)
    else:
        print("SAFE DELAY")
        while delay_time > DELAY_EXIT_CHECK:
            sleep(DELAY_EXIT_CHECK)
            delay_time -= DELAY_EXIT_CHECK
            if scripts.threads[x][y].kill.is_set():
                scripts.threads[x][y].kill.clear()
                if not scripts.run_async[x][y]:
                    scripts.running = False
                threading.Timer(scripts.EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
                return
        if delay_time > 0:
            sleep(delay_time)