import tkinter as tk
from tkinter import filedialog
import os

root = None
app = None
root_destroyed = None

import scripts, files

class Main_Window(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.layout_filetypes = [('LPHK layout files', '.LPHKlayout')]

    def init_window(self):
        self.master.title("LPHK - Novation Launchpad Macro Scripting System")
        self.pack(fill="both", expand=1)

        m = tk.Menu(self.master)
        self.master.config(menu=m)

        m_File = tk.Menu(m, tearoff=False)
        m_File.add_command(label="Load layout...", command=self.load_layout)
        m_File.add_command(label="Save layout...", command=self.save_layout)
        m_File.add_command(label="Save layout as...", command=self.save_layout_as)
        m.add_cascade(label="File", menu=m_File)

        b_unbind = tk.Button(self, text="Unbind All", command=self.unbind_lp)
        b_unbind.grid(row=0, column=0)

        b_unbind2 = tk.Button(self, text="Unbind All", command=self.unbind_lp)
        b_unbind2.grid(row=0, column=1)

    def unbind_lp(self):
        scripts.unbind_all()
        files.curr_layout = None

    def load_layout(self):
        name = filedialog.askopenfilename(parent=app,
                                          initialdir=os.getcwd() + "/user_layouts/",
                                          title="Load layout...:",
                                          filetypes=self.layout_filetypes)
        if name:
            files.load_layout(name, False)

    def save_layout_as(self):
        name = filedialog.asksaveasfilename(parent=app,
                                            initialdir=os.getcwd() + "/user_layouts/",
                                            title="Save layout as...:",
                                            filetypes=self.layout_filetypes)
        if name:
            files.save_layout(name, False)
            files.load_layout(name, False)

    def save_layout(self):
        if files.curr_layout == None:
            self.save_layout_as()
        else:
            files.save_layout(files.curr_layout, False)

def make():
    global root
    global app
    global root_destroyed
    root = tk.Tk()
    root_destroyed = False
    root.geometry("600x400")
    root.protocol("WM_DELETE_WINDOW", close)
    app = Main_Window(root)
    app.mainloop()

def close():
    global root_destroyed
    if not root_destroyed:
        root.destroy()
        root_destroyed = True

