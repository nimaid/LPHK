import sys
import tkinter as tk

try:
    import launchpad_py as launchpad
except ImportError:
    try:
        import launchpad
    except ImportError:
        sys.exit("[launchpad_py] Error loading launchpad.py")

import lp_events, lp_colors, scripts, keyboard, files, parse, sound

PATH = sys.path[0]

root = None
app = None

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
    def createWidgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

    def say_hi(self):
        print("hi there, everyone!")

lp = launchpad.LaunchpadMk2();

def init():
    lp.ButtonFlush()
    files.init(PATH)
    sound.init(PATH)
    lp_events.start(lp)

def close_window():
    root.destroy()

def shutdown():
    scripts.unbind_all()
    lp_events.timer.cancel()
    lp.Close()
    close_window()
    sys.exit("[LPHK] Sutting down...")

def make_window():
    global root
    global app
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", close_window)
    app = Application(master=root)
    app.mainloop()

def main():
    if lp.Open(0, "mk2"):
        print("[LPHK] Connected to Launchpad Mk2!")
    else:
        print("[LPHK] Could not connect to Launchpad Mk2, exiting...")
        return

    init()
    files.load_layout("default")
    make_window()


main()

