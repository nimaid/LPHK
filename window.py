#TODO: make buttons a canvas so I can change colors

import tkinter as tk
from tkinter import filedialog
import os

import scripts, files, lp_colors

BUTTON_SIZE = 40
BUTTON_GAP = BUTTON_SIZE // 4

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

        c_size = (BUTTON_SIZE * 9) + (BUTTON_GAP * 8)
        c = tk.Canvas(self, width=c_size, height=c_size)
        c.bind("<Button-1>", self.click)
        c.grid(row=0, column=0, padx=BUTTON_GAP, pady=BUTTON_GAP)

        self.draw_canvas(c)

    def unbind_lp(self):
        scripts.unbind_all()
        files.curr_layout = None

    def load_layout(self):
        name = filedialog.askopenfilename(parent=app,
                                          initialdir=os.getcwd() + "/user_layouts/",
                                          title="Load layout...:",
                                          filetypes=layout_filetypes)
        if name:
            files.load_layout(name, False)

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
        column = int((event.x + (BUTTON_GAP / 2)) // (BUTTON_SIZE + BUTTON_GAP))
        row = int((event.y + (BUTTON_GAP / 2)) // (BUTTON_SIZE + BUTTON_GAP))

        print("[window] Clicked at (" + str(column) + ", " + str(row) + ")")

    def draw_button(self, canvas, column, row, color="#000000", shape="square"):
        x_start = (BUTTON_SIZE * column) + (BUTTON_GAP * column)
        y_start = (BUTTON_SIZE * row) + (BUTTON_GAP * row)
        x_end = x_start + BUTTON_SIZE
        y_end = y_start + BUTTON_SIZE

        if shape == "square":
            canvas.create_rectangle(x_start, y_start, x_end, y_end, fill=color)
        elif shape == "circle":
            shrink = BUTTON_SIZE / 10
            canvas.create_oval(x_start + shrink, y_start + shrink, x_end - shrink, y_end - shrink, fill=color, outline="")

    def draw_canvas(self, canvas):
        canvas.delete("all")
        for x in range(8):
            self.draw_button(canvas, x, 0, shape="circle")

        for y in range(1, 9):
            self.draw_button(canvas, 8, y, shape="circle")

        for x in range(8):
            for y in range(1, 9):
                self.draw_button(canvas, x, y)


def make():
    global root
    global app
    global root_destroyed
    root = tk.Tk()
    root_destroyed = False
    #root.geometry("600x400")
    root.protocol("WM_DELETE_WINDOW", close)
    app = Main_Window(root)
    app.mainloop()

def close():
    global root_destroyed
    if not root_destroyed:
        root.destroy()
        root_destroyed = True

