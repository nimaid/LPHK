import tkinter as tk
import tkinter.filedialog, tkinter.scrolledtext, tkinter.messagebox
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
        self.info_image = tk.PhotoImage(file="resources/info.png").subsample(2, 2)
        self.warning_image = tk.PhotoImage(file="resources/warning.png").subsample(2, 2)

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
        name = tk.filedialog.askopenfilename(parent=app,
                                          initialdir=os.getcwd() + "/user_layouts/",
                                          title="Load layout...:",
                                          filetypes=layout_filetypes)
        if name:
            files.load_layout(name, False)
            self.draw_canvas()

    def save_layout_as(self):
        name = tk.filedialog.asksaveasfilename(parent=app,
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
        w.winfo_toplevel().title("Editing Script for Button (" + str(x) + ", " + str(y) + ")")
        w.resizable(False, False)

        t = tk.scrolledtext.ScrolledText(w)
        t.grid(column=0, row=0, columnspan=6, padx=10, pady=10)

        t.insert(tk.INSERT, scripts.text[x][y])

        curr_color = lp_colors.getXY(x, y)
        curr_color_bright = None
        if curr_color != 0:
            curr_color_bright = lp_colors.COLOR_BRIGHTS[curr_color]
        else:
            curr_color_bright = ("Blue", "Third")

        c_label = tk.Label(w, text="Color:")
        c_label.grid(column=0, row=1, sticky=tk.E)

        color = tk.StringVar(w)
        color.set(curr_color_bright[0])
        color_select = tk.OptionMenu(w, color, *lp_colors.VALID_COLORS)
        color_select.grid(column=1, row=1, sticky=tk.W)

        b_label = tk.Label(w, text="Brightness:")
        b_label.grid(column=2, row=1, sticky=tk.E)

        bright = tk.StringVar(w)
        bright.set(curr_color_bright[1])
        bright_select = tk.OptionMenu(w, bright, *lp_colors.VALID_BRIGHTS)
        bright_select.grid(column=3, row=1, sticky=tk.W)

        unbind_func = lambda: self.unbind_destroy(x, y, w)
        unbind_button = tk.Button(w, text="Unbind Button (" + str(x) + ", " + str(y) + ")", command=unbind_func)
        unbind_button.grid(column=4, row=1)

        save_func = lambda: self.save_script(w, x, y, lp_colors.code_by_color_brightness(color.get(), bright.get()), t.get(1.0, tk.END))
        save_button = tk.Button(w, text="Save Script", command=save_func)
        save_button.grid(column=5, row=1)

        w.wait_visibility()
        w.grab_set()
        t.focus_set()

    def unbind_destroy(self, x, y, window):
        scripts.unbind(x, y)
        self.draw_canvas()
        window.destroy()

    def save_script(self, window, x, y, color, script_text):
        script_text = script_text.strip()

        script_validate = scripts.validate_script(script_text)
        if script_validate == True:
            if script_text != "":
                scripts.bind(x, y, script_text, color)
                self.draw_canvas()
                window.destroy()
            else:
                self.popup(window, "No Script Entered", self.info_image, "Please enter a script before saving.", "OK")
        else:
            self.popup(window, "Syntax Error", self.warning_image, "Invalid command: " + script_validate, "OK")

    def popup(self, window, title, image, text, button_text):
        popup = tk.Toplevel(window)
        popup.resizable(False, False)
        popup.wm_title(title)
        popup.tkraise(window)
        picture_label = tk.Label(popup, image=image)
        picture_label.photo = image
        picture_label.grid(column=0, row=0, rowspan=2, padx=10, pady=10)
        tk.Label(popup, text=text).grid(column=1, row=0, padx=10, pady=10)
        tk.Button(popup, text=button_text, command=popup.destroy).grid(column=1, row=1, padx=10, pady=10)
        popup.wait_visibility()
        popup.grab_set()

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

