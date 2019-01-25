import tkinter as tk
import tkinter.filedialog, tkinter.scrolledtext, tkinter.messagebox, tkcolorpicker
from PIL import ImageTk, Image
import os
from functools import partial

import scripts, files, lp_colors, lp_events

BUTTON_SIZE = 40
HS_SIZE = 200
V_WIDTH = 50
STAT_ACTIVE_COLOR = "#080"
STAT_INACTIVE_COLOR = "#444"
DEFAULT_COLOR = [0, 0, 255]
INDICATOR_BPM = 480
BUTTON_FONT = ("helvetica", 11, "bold")

root = None
app = None
root_destroyed = None
restart = False
lp_object = None

layout_filetypes = [('LPHK layout files', files.LAYOUT_EXT)]
script_filetypes = [('LPHK script files', files.SCRIPT_EXT)]

lp_connected = False
colors_to_set = [[[0, 0, 255] for y in range(9)] for x in range(9)]

def init(lp_object_in):
    global lp_object
    lp_object = lp_object_in

    make()

class Main_Window(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_window()

        self.info_image = ImageTk.PhotoImage(Image.open("resources/info.png"))
        self.warning_image = ImageTk.PhotoImage(Image.open("resources/warning.png"))
        self.error_image = ImageTk.PhotoImage(Image.open("resources/error.png"))
        self.alert_image = ImageTk.PhotoImage(Image.open("resources/alert.png"))
        self.scare_image = ImageTk.PhotoImage(Image.open("resources/scare.png"))
        self.grid_drawn = False
        self.grid_rects = [[None for y in range(9)] for x in range(9)]

    def init_window(self):
        self.master.title("LPHK - Novation Launchpad Macro Scripting System")
        self.pack(fill="both", expand=1)

        self.m = tk.Menu(self.master)
        self.master.config(menu=self.m)

        self.m_Launchpad = tk.Menu(self.m, tearoff=False)
        self.m_Launchpad.add_command(label="Connect to Launchpad MkII...", command=self.connect_MkII)
        self.m_Launchpad.add_command(label="Disonnect from Launchpad...", command=self.disconnect_lp)
        self.m_Launchpad.add_command(label="Redetect...", command=self.redetect_lp)
        self.m.add_cascade(label="Launchpad", menu=self.m_Launchpad)

        self.disable_lp_disconnect()

        self.m_Layout = tk.Menu(self.m, tearoff=False)
        self.m_Layout.add_command(label="New layout...", command=self.unbind_lp)
        self.m_Layout.add_command(label="Load layout...", command=self.load_layout)
        self.m_Layout.add_command(label="Save layout...", command=self.save_layout)
        self.m_Layout.add_command(label="Save layout as...", command=self.save_layout_as)
        self.m.add_cascade(label="Layout", menu=self.m_Layout)
        
        self.m_Button = tk.Menu(self.m, tearoff=False)
        def nop():
            pass
        self.m_Button.add_command(label="(WIP) Move button...", command=nop)
        self.m_Button.add_command(label="(WIP) Swap buttons...", command=nop)
        self.m_Button.add_command(label="(WIP) Copy button...", command=nop)
        self.m.add_cascade(label="Button", menu=self.m_Button)

        self.disable_menu("Layout")
        self.disable_menu("Button")

        c_gap = int(BUTTON_SIZE // 4)

        c_size = (BUTTON_SIZE * 9) + (c_gap * 8)
        self.c = tk.Canvas(self, width=c_size, height=c_size)
        self.c.bind("<Button-1>", self.click)
        self.c.grid(row=0, column=0, padx=c_gap, pady=c_gap)

        self.stat = tk.Label(self, text="No Launchpad Connected", bg=STAT_INACTIVE_COLOR, fg="#fff")
        self.stat.grid(row=1, column=0, sticky=tk.EW)
        self.stat.config(font=("Courier", BUTTON_SIZE // 3, "bold"))

    def enable_menu(self, name):
        self.m.entryconfig(name, state="normal")

    def disable_menu(self, name):
        self.m.entryconfig(name, state="disabled")

    def enable_lp_disconnect(self):
        self.m_Launchpad.entryconfig("Disonnect from Launchpad...", state="normal")

    def disable_lp_disconnect(self):
        self.m_Launchpad.entryconfig("Disonnect from Launchpad...", state="disabled")

    def connect_MkII(self):
        global lp_connected
        try:
            if lp_object.Open(0, "mk2"):
                lp_connected = True
                lp_object.ButtonFlush()
                lp_object.LedCtrlBpm(INDICATOR_BPM)
                lp_events.start(lp_object)
                self.draw_canvas()
                self.enable_menu("Layout")
                self.enable_menu("Button")
                self.enable_lp_disconnect()

                self.stat["text"] = "Connected to Launchpad MkII"
                self.stat["bg"] = STAT_ACTIVE_COLOR
            else:
                self.popup(self, "Connect to Launchpad MkII...", self.error_image, "Could not connect to Launchpad MkII!\nPlug in your USB cable and try the 'Redetect...' option from the 'Launchpad' menu.", "OK")
        except:
            self.popup(self, "Connect to Launchpad MkII...", self.error_image, "Fatal error while connecting to Launchpad MkII!\nDisconnect and reconnect your USB cable, then use the 'Redetect...' option from the 'Launchpad' menu.", "OK")

    def disconnect_lp(self):
        global lp_connected
        try:
            scripts.unbind_all()
            lp_events.timer.cancel()
            lp_object.Close()
        except:
            self.redetect_lp()
        lp_connected = False

        self.clear_canvas()

        self.disable_menu("Layout")
        self.disable_menu("Button")
        self.disable_lp_disconnect()

        self.stat["text"] = "No Launchpad Connected"
        self.stat["bg"] = STAT_INACTIVE_COLOR

    def redetect_lp(self):
        global restart
        restart = True
        close()

    def unbind_lp(self):
        scripts.unbind_all()
        files.curr_layout = None
        self.draw_canvas()

    def load_layout(self):
        name = tk.filedialog.askopenfilename(parent=app,
                                          initialdir=os.getcwd() + files.LAYOUT_PATH,
                                          title="Load layout...",
                                          filetypes=layout_filetypes)
        if name:
            files.load_layout(name, False)
            self.draw_canvas()

    def save_layout_as(self):
        name = tk.filedialog.asksaveasfilename(parent=app,
                                            initialdir=os.getcwd() + files.LAYOUT_PATH,
                                            title="Save layout as...",
                                            filetypes=layout_filetypes)
        if name:
            if files.LAYOUT_EXT not in name:
                name += files.LAYOUT_EXT
            files.save_layout(name, False)
            files.load_layout(name, False)

    def save_layout(self):
        if files.curr_layout == None:
            self.save_layout_as()
        else:
            files.save_layout(files.curr_layout, False)
            files.load_layout(files.curr_layout, False)

    def click(self, event):
        gap = int(BUTTON_SIZE // 4)

        column = int((event.x + (gap / 2)) // (BUTTON_SIZE + gap))
        row = int((event.y + (gap / 2)) // (BUTTON_SIZE + gap))

        if self.grid_drawn and ((column, row) != (8, 0)):
            self.script_entry_window(column, row)

    def draw_button(self, column, row, color="#000000", shape="square"):
        gap = int(BUTTON_SIZE // 4)

        x_start = (BUTTON_SIZE * column) + (gap * column)
        y_start = (BUTTON_SIZE * row) + (gap * row)
        x_end = x_start + BUTTON_SIZE
        y_end = y_start + BUTTON_SIZE

        if shape == "square":
            return self.c.create_rectangle(x_start, y_start, x_end, y_end, fill=color, outline="")
        elif shape == "circle":
            shrink = BUTTON_SIZE / 10
            return self.c.create_oval(x_start + shrink, y_start + shrink, x_end - shrink, y_end - shrink, fill=color, outline="")

    def draw_canvas(self):
        if self.grid_drawn:
            for x in range(8):
                y = 0
                self.c.itemconfig(self.grid_rects[x][y], fill=lp_colors.getXY_RGB(x, y))

            for y in range(1, 9):
                x = 8
                self.c.itemconfig(self.grid_rects[x][y], fill=lp_colors.getXY_RGB(x, y))

            for x in range(8):
                for y in range(1, 9):
                    self.c.itemconfig(self.grid_rects[x][y], fill=lp_colors.getXY_RGB(x, y))
        else:
            for x in range(8):
                y = 0
                self.grid_rects[x][y] = self.draw_button(x, y, color=lp_colors.getXY_RGB(x, y), shape="circle")

            for y in range(1, 9):
                x = 8
                self.grid_rects[x][y] = self.draw_button(x, y, color=lp_colors.getXY_RGB(x, y), shape="circle")

            for x in range(8):
                for y in range(1, 9):
                    self.grid_rects[x][y] = self.draw_button(x, y, color=lp_colors.getXY_RGB(x, y))
            self.grid_drawn = True

    def clear_canvas(self):
        self.c.delete("all")
        self.grid_rects = [[None for y in range(9)] for x in range(9)]
        self.grid_drawn = False

    def script_entry_window(self, x, y, text_override=None, color_override=None):
        global color_to_set
        
        w = tk.Toplevel(self)
        w.winfo_toplevel().title("Editing Script for Button (" + str(x) + ", " + str(y) + ")...")
        w.resizable(False, False)
        
        def validate_func():
            nonlocal x, y, t
            
            text_string = t.get(1.0, tk.END)
            script_validate = scripts.validate_script(text_string)
            if script_validate != True and files.in_error:
                self.save_script(w, x, y, text_string)
            else:
                w.destroy()
        w.protocol("WM_DELETE_WINDOW", validate_func)

        e_m = tk.Menu(w)
        w.config(menu=e_m)

        e_m_Script = tk.Menu(e_m, tearoff=False)

        t = tk.scrolledtext.ScrolledText(w)
        t.grid(column=0, row=0, rowspan=3, padx=10, pady=10)
        
        if text_override == None:
            t.insert(tk.INSERT, scripts.text[x][y])
        else:
            t.insert(tk.INSERT, text_override)
        t.bind("<<Paste>>", self.custom_paste)
        t.bind("<Control-Key-a>", self.select_all)

        import_script_func = lambda: self.import_script(t, w)
        e_m_Script.add_command(label="Import script...", command=import_script_func)
        export_script_func = lambda: self.export_script(t, w)
        e_m_Script.add_command(label="Export script...", command=export_script_func)
        e_m.add_cascade(label="Script", menu=e_m_Script)
        
        if color_override == None:
            colors_to_set[x][y] =  lp_colors.getXY(x, y)
        else:
            colors_to_set[x][y] = color_override
        
        if type(colors_to_set[x][y]) == int:
            rgb = lp_colors.RGB[colors_to_set[x][y]]
            colors_to_set[x][y] = []
            for c in range(3):
                val = rgb[c + 1]
                colors_to_set[x][y].append(int(val + val, 16))
        
        if all(c < 4 for c in colors_to_set[x][y]):
            colors_to_set[x][y] = DEFAULT_COLOR
        
        ask_color_func = lambda: self.ask_color(w, color_button, x, y, colors_to_set[x][y])
        color_button = tk.Button(w, text="Select Color", command=ask_color_func)
        color_button.grid(column=1, row=0, padx=(0, 10), pady=(10, 50), sticky="nesw")
        color_button.config(font=BUTTON_FONT)
        start_color_str = lp_colors.list_RGB_to_string(colors_to_set[x][y])
        self.button_color_with_text_update(color_button, start_color_str)

        save_script_func = lambda: self.save_script(w, x, y, t.get(1.0, tk.END))
        save_button = tk.Button(w, text="Bind Button (" + str(x) + ", " + str(y) + ")", command=save_script_func)
        save_button.grid(column=1, row=1, padx=(0,10), sticky="nesw")
        save_button.config(font=BUTTON_FONT)
        save_button.config(bg="#c3d9C3")

        unbind_func = lambda: self.unbind_destroy(x, y, w)
        unbind_button = tk.Button(w, text="Unbind Button (" + str(x) + ", " + str(y) + ")", command=unbind_func)
        unbind_button.grid(column=1, row=2, padx=(0,10), pady=10, sticky="nesw")
        unbind_button.config(font=BUTTON_FONT)
        unbind_button.config(bg="#d9c3c3")

        w.wait_visibility()
        w.grab_set()
        t.focus_set()
        w.wait_window()
        
    def ask_color(self, window, button, x, y, default_color):
        global colors_to_set
        color = tkcolorpicker.askcolor(color=tuple(default_color), parent=window, title="Select Color for Button (" + str(x) + ", " + str(y) + ")...")
        if color[0] != None:
            color_to_set = [int(min(255, max(0, c))) for c in color[0]]
            if all(c < 4 for c in color_to_set):
                rerun = lambda: self.ask_color(window, button, x, y, default_color)
                self.popup(window, "Invalid Color", self.warning_image, "That color is too dark to see.", "OK", rerun)
            else:
                colors_to_set[x][y] = color_to_set
                self.button_color_with_text_update(button, color[1])

    def button_color_with_text_update(self, button, color):
        button.configure(bg=color, activebackground=color)
        color_rgb = []
        for c in range(3):
            start_index = c * 2
            val = color[start_index + 1:start_index + 3]
            color_rgb.append(int(val, 16))
        luminance = lp_colors.luminance(color_rgb[0], color_rgb[1], color_rgb[2])
        if luminance > 0.5:
            button.configure(fg="black", activeforeground="black")
        else:
            button.configure(fg="white", activeforeground="white")

    def custom_paste(self, event):
        try:
            event.widget.delete("sel.first", "sel.last")
        except:
            pass
        event.widget.insert("insert", event.widget.clipboard_get())
        return "break"

    def select_all(self, event):
        event.widget.tag_add(tk.SEL, "1.0", tk.END)
        event.widget.mark_set(tk.INSERT, "1.0")
        event.widget.see(tk.INSERT)
        return "break"

    def unbind_destroy(self, x, y, window):
        scripts.unbind(x, y)
        self.draw_canvas()
        window.destroy()

    def save_script(self, window, x, y, script_text, open_editor = False, color=None):
        global colors_to_set
        
        script_text = script_text.strip()
        
        def open_editor_func():
            nonlocal x, y
            if open_editor:
                    self.script_entry_window(x, y, script_text, color)

        script_validate = scripts.validate_script(script_text)
        if script_validate == True:
            if script_text != "":
                script_text = files.strip_lines(script_text)
                scripts.bind(x, y, script_text, colors_to_set[x][y])
                self.draw_canvas()
                lp_colors.updateXY(x, y)
                window.destroy()
            else:
                self.popup(window, "No Script Entered", self.info_image, "Please enter a script to bind.", "OK", end_command = open_editor_func)
        else:
            self.popup(window, "(" + str(x) + ", " + str(y) + ") Syntax Error", self.error_image, "Error in line: " + script_validate[1] + "\n" + script_validate[0], "OK", end_command = open_editor_func)

    def import_script(self, textbox, window):
        name = tk.filedialog.askopenfilename(parent=window,
                                             initialdir=os.getcwd() + files.SCRIPT_PATH,
                                             title="Import script...",
                                             filetypes=script_filetypes)
        if name:
            text = files.import_script(name, False)
            text = files.strip_lines(text)
            textbox.delete("1.0", tk.END)
            textbox.insert(tk.INSERT, text)

    def export_script(self, textbox, window):
        name = tk.filedialog.asksaveasfilename(parent=window,
                                               initialdir=os.getcwd() + files.SCRIPT_PATH,
                                               title="Export script...",
                                               filetypes=script_filetypes)
        if name:
            if files.SCRIPT_EXT not in name:
                name += files.SCRIPT_EXT
            text = textbox.get("1.0", tk.END)
            text = files.strip_lines(text)
            files.export_script(name, text, False)

    def popup(self, window, title, image, text, button_text, end_command=None):
        popup = tk.Toplevel(window)
        popup.resizable(False, False)
        popup.wm_title(title)
        popup.tkraise(window)

        def run_end():
            popup.destroy()
            if end_command != None:
                end_command()

        picture_label = tk.Label(popup, image=image)
        picture_label.photo = image
        picture_label.grid(column=0, row=0, rowspan=2, padx=10, pady=10)
        tk.Label(popup, text=text, justify=tk.LEFT).grid(column=1, row=0, padx=10, pady=10)
        tk.Button(popup, text=button_text, command=run_end).grid(column=1, row=1, padx=10, pady=10)
        popup.wait_visibility()
        popup.grab_set()
        popup.wait_window()
    
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

