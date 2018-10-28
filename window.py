import tkinter as tk

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

def make():
    global root
    global app
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", close)
    app = Application(master=root)
    app.mainloop()

def close():
    root.destroy()

