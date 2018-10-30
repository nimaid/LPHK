#TODO: make buttons a canvas so I can change colors

import tkinter as tk
from tkinter import filedialog
import os

import scripts, files, lp_colors

BUTTON_SIZE = 40

root = None
app = None
root_destroyed = None

layout_filetypes = [('LPHK layout files', files.LAYOUT_EXT)]

class Main_Window(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("LPHK - Novation Launchpad Macro Scripting System")
        self.pack(fill="both", expand=1)

        m = tk.Menu(self.master)
        self.master.config(menu=m)

        m_Layout = tk.Menu(m, tearoff=False)
        m_Layout.add_command(label="New layout...", command=self.unbind_lp)
        m_Layout.add_command(label="Load layout...", command=self.load_layout)
        m_Layout.add_command(label="Save layout...", command=self.save_layout)
        m_Layout.add_command(label="Save layout as...", command=self.save_layout_as)
        m.add_cascade(label="Layout", menu=m_Layout)

        c_gap = int(BUTTON_SIZE // 4)

        c_size = (BUTTON_SIZE * 9) + (c_gap * 8)
        self.c = tk.Canvas(self, width=c_size, height=c_size)
        self.c.bind("<Button-1>", self.click)
        self.c.grid(row=0, column=0, padx=c_gap, pady=c_gap)

        self.draw_canvas()

    def unbind_lp(self):
        scripts.unbind_all()
        files.curr_layout = None
        self.draw_canvas()

    def load_layout(self):
        name = filedialog.askopenfilename(parent=app,
                                          initialdir=os.getcwd() + "/user_layouts/",
                                          title="Load layout...:",
                                          filetypes=layout_filetypes)
        if name:
            files.load_layout(name, False)
            self.draw_canvas()

    def save_layout_as(self):
        name = filedialog.asksaveasfilename(parent=app,
                                            initialdir=os.getcwd() + "/user_layouts/",
                                            title="Save layout as...:",
                                            filetypes=layout_filetypes)
        if name:
            files.save_layout(name, False)
            files.load_layout(name, False)

    def save_layout(self):
        if files.curr_layout == None:
            self.save_layout_as()
        else:
            files.save_layout(files.curr_layout, False)

    def click(self, event):
        gap = int(BUTTON_SIZE // 4)

        column = int((event.x + (gap / 2)) // (BUTTON_SIZE + gap))
        row = int((event.y + (gap / 2)) // (BUTTON_SIZE + gap))

        self.script_entry_window(column, row)

        print("[window] Clicked at (" + str(column) + ", " + str(row) + ")")

    def draw_button(self, column, row, color="#000000", shape="square"):
        gap = int(BUTTON_SIZE // 4)

        x_start = (BUTTON_SIZE * column) + (gap * column)
        y_start = (BUTTON_SIZE * row) + (gap * row)
        x_end = x_start + BUTTON_SIZE
        y_end = y_start + BUTTON_SIZE

        if shape == "square":
            self.c.create_rectangle(x_start, y_start, x_end, y_end, fill=color, outline="")
        elif shape == "circle":
            shrink = BUTTON_SIZE / 10
            self.c.create_oval(x_start + shrink, y_start + shrink, x_end - shrink, y_end - shrink, fill=color, outline="")

    def draw_canvas(self):
        self.c.delete("all")
        for x in range(8):
            y = 0
            self.draw_button(x, y, color=lp_colors.getXY_RGB(x, y), shape="circle")

        for y in range(1, 9):
            x = 8
            self.draw_button(x, y, color=lp_colors.getXY_RGB(x, y), shape="circle")

        for x in range(8):
            for y in range(1, 9):
                self.draw_button(x, y, color=lp_colors.getXY_RGB(x, y))

    def script_entry_window(self, x, y):
        w = tk.Toplevel(self)
        w.winfo_toplevel().title("Editing script for button (" + str(x) + ", " + str(y) + ")")
        b = tk.Label(w, text="You pressed (" + str(x) + ", " + str(y) + ")")
        b.grid(column=0, row=0, padx=150, pady=20)

def make():
    global root
    global app
    global root_destroyed
    root = tk.Tk()
    root_destroyed = False
    root.protocol("WM_DELETE_WINDOW", close)
    root.resizable(False, False)
    app = Main_Window(root)
    app.mainloop()

def close():
    global root_destroyed
    if not root_destroyed:
        root.destroy()
        root_destroyed = True

