import tkinter as tk
import tkinter.filedialog, tkinter.scrolledtext, tkinter.messagebox, tkcolorpicker
from PIL import ImageTk, Image
import os, sys
from functools import partial
import webbrowser

import scripts, files, lp_colors, lp_events
import script_examples
import ui_theme as theme
from utils import launchpad_connector as lpcon

BUTTON_SIZE = 48
HS_SIZE = 200
V_WIDTH = 50
STAT_ACTIVE_COLOR = theme.SUCCESS
STAT_INACTIVE_COLOR = theme.INACTIVE
SELECT_COLOR = theme.SELECT
DEFAULT_COLOR = [0, 0, 255]
MK1_DEFAULT_COLOR = [0, 255, 0]
INDICATOR_BPM = 480
BUTTON_FONT = theme.FONT_BUTTON

MODE_ORDER = ("edit", "move", "swap", "copy")
MODE_HINTS = {
    "edit": "Click a pad to edit its script and color.",
    "move": "Select a pad, then click a destination to move it.",
    "swap": "Select a pad, then click another to swap them.",
    "copy": "Select a pad, then click a destination to copy it.",
}

PATH = None
PROG_PATH = None
USER_PATH = None

VERSION = None

PLATFORM = None

MAIN_ICON = None

launchpad = None

root = None
app = None
root_destroyed = None
restart = False
lp_object = None


load_layout_filetypes = [('LPHK layout files', [files.LAYOUT_EXT, files.LEGACY_LAYOUT_EXT])]
load_script_filetypes = [('LPHK script files', [files.SCRIPT_EXT, files.LEGACY_SCRIPT_EXT])]

save_layout_filetypes = [('LPHK layout files', [files.LAYOUT_EXT])]
save_script_filetypes = [('LPHK script files', [files.SCRIPT_EXT])]

lp_connected = False
lp_mode = None
colors_to_set = [[DEFAULT_COLOR for y in range(9)] for x in range(9)]


def init(lp_object_in, launchpad_in, path_in, prog_path_in, user_path_in, version_in, platform_in):
    global lp_object
    global launchpad
    global PATH
    global PROG_PATH
    global USER_PATH
    global VERSION
    global PLATFORM
    global MAIN_ICON
    lp_object = lp_object_in
    launchpad = launchpad_in
    PATH = path_in
    PROG_PATH = prog_path_in
    USER_PATH = user_path_in
    VERSION = version_in
    PLATFORM = platform_in
    
    if PLATFORM == "windows":
        MAIN_ICON = os.path.join(PATH, "resources", "LPHK.ico")
    else:
        MAIN_ICON = os.path.join(PATH, "resources", "LPHK.gif")

    make()


class Main_Window(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bg=theme.BG)
        self.master = master
        self.mode_buttons = {}
        self.grid_drawn = False
        self.grid_rects = [[None for y in range(9)] for x in range(9)]
        self.button_mode = "edit"
        self.last_clicked = None
        self.outline_box = None
        self.init_window()
        
        self.about_image = ImageTk.PhotoImage(Image.open(PATH + "/resources/LPHK-banner.png"))
        self.info_image = ImageTk.PhotoImage(Image.open(PATH + "/resources/info.png"))
        self.warning_image = ImageTk.PhotoImage(Image.open(PATH + "/resources/warning.png"))
        self.error_image = ImageTk.PhotoImage(Image.open(PATH + "/resources/error.png"))
        self.alert_image = ImageTk.PhotoImage(Image.open(PATH + "/resources/alert.png"))
        self.scare_image = ImageTk.PhotoImage(Image.open(PATH + "/resources/scare.png"))

    def _set_toplevel_icon(self, window):
        if MAIN_ICON is None:
            return
        if os.path.splitext(MAIN_ICON)[1].lower() == ".gif":
            return
        try:
            window.iconbitmap(MAIN_ICON)
        except tk.TclError:
            pass

    def init_window(self):
        global root
        
        self.master.title("LPHK - Novation Launchpad Macro Scripting System")
        self.master.configure(bg=theme.BG)
        self.pack(fill="both", expand=1)
        self.configure(bg=theme.BG, padx=theme.PAD_LG, pady=theme.PAD_LG)

        self.m = tk.Menu(self.master)
        self.master.config(menu=self.m)

        self.m_Launchpad = tk.Menu(self.m, tearoff=False)
        self.m_Launchpad.add_command(label="Redetect (Restart)", command=self.redetect_lp)
        self.m.add_cascade(label="Launchpad", menu=self.m_Launchpad)

        self.m_Layout = tk.Menu(self.m, tearoff=False)
        self.m_Layout.add_command(label="New Layout", command=self.unbind_lp)
        self.m_Layout.add_command(label="Load Layout", command=self.load_layout)
        self.m_Layout.add_command(label="Save Layout", command=self.save_layout)
        self.m_Layout.add_command(label="Save Layout As...", command=self.save_layout_as)
        self.m.add_cascade(label="Layout", menu=self.m_Layout)

        self.disable_menu("Layout")
        
        self.m_Help = tk.Menu(self.m, tearoff=False)
        open_readme = lambda: webbrowser.open("https://github.com/nimaid/LPHK#lphk-launchpad-hotkey")
        self.m_Help.add_command(label="Open README...", command=open_readme)
        open_scripting = lambda: webbrowser.open("https://github.com/nimaid/LPHK#what-is-lphkscript-table-of-contents")
        self.m_Help.add_command(label="Scripting Help...", command=open_scripting)
        open_user_folder = lambda: files.open_file_folder(USER_PATH)
        self.m_Help.add_command(label="User Folder...", command=open_user_folder)
        open_prog_folder = lambda: files.open_file_folder(PROG_PATH)
        self.m_Help.add_command(label="Program Folder...", command=open_prog_folder)
        display_info = lambda: self.popup(self, "About LPHK", self.about_image, "A Novation Launchpad Macro Scripting System\nMade by Ella Jameson (nimaid)\n\nVersion: " + VERSION + "\nFile format version: " + files.FILE_VERSION, "Done")
        self.m_Help.add_command(label="About LPHK", command=display_info)
        self.m.add_cascade(label="Help", menu=self.m_Help)

        # Header: brand + status pill
        header = tk.Frame(self, bg=theme.BG)
        header.grid(row=0, column=0, sticky="ew", pady=(0, theme.PAD))

        brand_col = tk.Frame(header, bg=theme.BG)
        brand_col.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(
            brand_col,
            text="LPHK",
            bg=theme.BG,
            fg=theme.TEXT,
            font=theme.FONT_BRAND,
        ).pack(anchor="w")

        tk.Label(
            brand_col,
            text="Launchpad macro scripting",
            bg=theme.BG,
            fg=theme.TEXT_SECONDARY,
            font=theme.FONT_SUBTITLE,
        ).pack(anchor="w")

        self.stat = tk.Label(header, text="No Launchpad Connected", anchor="center")
        self.stat.pack(side=tk.RIGHT, padx=(theme.PAD, 0))
        theme.style_status_pill(self.stat, connected=False)

        # Mode toolbar
        toolbar = tk.Frame(self, bg=theme.BG)
        toolbar.grid(row=1, column=0, sticky="ew", pady=(0, theme.PAD))

        tk.Label(
            toolbar,
            text="Mode",
            bg=theme.BG,
            fg=theme.TEXT_SECONDARY,
            font=theme.FONT_HINT,
        ).pack(side=tk.LEFT, padx=(0, theme.GAP))

        mode_group = tk.Frame(toolbar, bg=theme.BG)
        mode_group.pack(side=tk.LEFT)

        for idx, mode in enumerate(MODE_ORDER):
            btn = tk.Button(
                mode_group,
                text=mode.capitalize(),
                command=partial(self.set_button_mode, mode),
            )
            btn.pack(side=tk.LEFT, padx=(0 if idx == 0 else 4, 0))
            self.mode_buttons[mode] = btn

        self._refresh_mode_controls()

        # Pad stage (white bezel)
        bezel = tk.Frame(
            self,
            bg=theme.SURFACE,
            highlightbackground=theme.BORDER,
            highlightthickness=1,
            bd=0,
        )
        bezel.grid(row=2, column=0, sticky="nsew")

        pad_inner = tk.Frame(bezel, bg=theme.SURFACE, padx=theme.PAD, pady=theme.PAD)
        pad_inner.pack()

        c_gap = int(BUTTON_SIZE // 4)
        c_size = (BUTTON_SIZE * 9) + (c_gap * 9)
        self.c = tk.Canvas(
            pad_inner,
            width=c_size,
            height=c_size,
            bg=theme.PAD_CANVAS_BG,
            highlightthickness=0,
            bd=0,
        )
        self.c.bind("<Button-1>", self.click)
        self.c.pack()

        # Footer hint
        self.hint = tk.Label(
            self,
            text=MODE_HINTS["edit"],
            bg=theme.BG,
            fg=theme.TEXT_SECONDARY,
            font=theme.FONT_HINT,
            anchor="w",
        )
        self.hint.grid(row=3, column=0, sticky="ew", pady=(theme.PAD, 0))
    
    def _refresh_mode_controls(self):
        for mode, btn in self.mode_buttons.items():
            theme.style_mode_button(btn, active=(mode == self.button_mode))
        if hasattr(self, "hint"):
            self.hint.configure(text=MODE_HINTS.get(self.button_mode, ""))

    def set_button_mode(self, mode):
        if mode not in MODE_ORDER:
            return
        self.button_mode = mode
        self.last_clicked = None
        self._refresh_mode_controls()
        if self.grid_drawn:
            self.draw_canvas()

    def raise_above_all(self):
        self.master.attributes('-topmost', 1)
        self.master.attributes('-topmost', 0)
    
    def enable_menu(self, name):
        self.m.entryconfig(name, state="normal")

    def disable_menu(self, name):
        self.m.entryconfig(name, state="disabled")
    
    def connect_dummy(self):
        # WIP
        global lp_connected
        global lp_mode
        global lp_object
        
        lp_connected = True
        lp_mode = "Dummy"
        self.draw_canvas()
        self.enable_menu("Layout")
        self.stat["text"] = "Connected to Dummy"
        theme.style_status_pill(self.stat, connected=True)

    def connect_lp(self):
        global lp_connected
        global lp_mode
        global lp_object

        lp = lpcon.get_launchpad()

        if lp == -1:
            self.popup(self, "Connect to Unsupported Device", self.error_image,
                       """The device you are attempting to use is not currently supported by LPHK,
                       and there are no plans to add support for it.
                       Please voice your feature requests on the Discord or on GitHub.""",
                       "OK")

        if lp is None:
            self.popup_choice(self, "No Launchpad Detected...", self.error_image,
                              """Could not detect any connected Launchpads!
                              Disconnect and reconnect your USB cable,
                              then click 'Redetect Now'.""",
                              [["Ignore", None], ["Redetect Now", self.redetect_lp]]
                              )
            return

        if lpcon.connect(lp):
            lp_connected = True
            lp_object = lp
            lp_mode = lpcon.get_mode(lp)

            lp_object.ButtonFlush()

            # special case?
            if lp_mode != "Mk1":
                lp_object.LedCtrlBpm(INDICATOR_BPM)

            lp_events.start(lp_object)
            self.draw_canvas()
            self.enable_menu("Layout")
            self.stat["text"] = f"Connected to {lpcon.get_display_name(lp)}"
            theme.style_status_pill(self.stat, connected=True)
            # search for a startup layout and load it
            if os.path.isfile(os.path.join(files.LAYOUT_PATH, "startup.lpl")):
                files.load_layout_to_lp(os.path.join(files.LAYOUT_PATH, "startup.lpl"))

    def disconnect_lp(self):
        global lp_connected
        try:
            scripts.unbind_all()
            lp_events.timer.cancel()
            lpcon.disconnect(lp_object)
        except:
            self.redetect_lp()
        lp_connected = False

        self.clear_canvas()

        self.disable_menu("Layout")

        self.stat["text"] = "No Launchpad Connected"
        theme.style_status_pill(self.stat, connected=False)

    def redetect_lp(self):
        global restart
        restart = True
        close()

    def unbind_lp(self, prompt_save=True):
        if prompt_save:
            self.modified_layout_save_prompt()
        scripts.unbind_all()
        files.curr_layout = None
        self.draw_canvas()

    def load_layout(self):
        self.modified_layout_save_prompt()
        name = tk.filedialog.askopenfilename(parent=app,
                                          initialdir=files.LAYOUT_PATH,
                                          title="Load layout",
                                          filetypes=load_layout_filetypes)
        if name:
            files.load_layout_to_lp(name)

    def save_layout_as(self):
        name = tk.filedialog.asksaveasfilename(parent=app,
                                            initialdir=files.LAYOUT_PATH,
                                            title="Save layout as...",
                                            filetypes=save_layout_filetypes)
        if name:
            if files.LAYOUT_EXT not in name:
                name += files.LAYOUT_EXT
            files.save_lp_to_layout(name)
            files.load_layout_to_lp(name)

    def save_layout(self):
        if files.curr_layout == None:
            self.save_layout_as()
        else:
            files.save_lp_to_layout(files.curr_layout)
            files.load_layout_to_lp(files.curr_layout)
    
    def click(self, event):
        gap = int(BUTTON_SIZE // 4)
        
        
        column = min(8, int(event.x // (BUTTON_SIZE + gap)))
        row = min(8, int(event.y // (BUTTON_SIZE + gap)))

        if self.grid_drawn:
            if(column, row) == (8, 0):
            #mode change
                self.last_clicked = None
                if self.button_mode == "edit":
                    self.button_mode = "move"
                elif self.button_mode == "move":
                    self.button_mode = "swap"
                elif self.button_mode == "swap":
                    self.button_mode = "copy"
                else:
                    self.button_mode = "edit"
                self._refresh_mode_controls()
                self.draw_canvas()
            else:
                if self.button_mode == "edit":
                    self.last_clicked = (column, row)
                    self.draw_canvas()
                    self.script_entry_window(column, row)
                    self.last_clicked = None
                else:
                    if self.last_clicked == None:
                        self.last_clicked = (column, row)
                    else:
                        move_func = partial(scripts.move, self.last_clicked[0], self.last_clicked[1], column, row)
                        swap_func = partial(scripts.swap, self.last_clicked[0], self.last_clicked[1], column, row)
                        copy_func = partial(scripts.copy, self.last_clicked[0], self.last_clicked[1], column, row)
                        
                        if self.button_mode == "move":
                            if scripts.is_bound(column, row) and ((self.last_clicked) != (column, row)):
                                self.popup_choice(self, "Button Already Bound", self.warning_image, "You are attempting to move a button to an already\nbound button. What would you like to do?", [["Overwrite", move_func], ["Swap", swap_func], ["Cancel", None]])
                            else:
                                move_func()
                        elif self.button_mode == "copy":
                            if scripts.is_bound(column, row) and ((self.last_clicked) != (column, row)):
                                self.popup_choice(self, "Button Already Bound", self.warning_image, "You are attempting to copy a button to an already\nbound button. What would you like to do?", [["Overwrite", copy_func], ["Swap", swap_func], ["Cancel", None]])
                            else:
                                copy_func()
                        elif self.button_mode == "swap":
                            swap_func()
                        self.last_clicked = None
                self.draw_canvas()
                    
    def draw_button(self, column, row, color="#000000", shape="square"):
        gap = int(BUTTON_SIZE // 4)
        fill = theme.display_pad_color(color)
        outline = theme.pad_outline_for(fill)

        x_start = round((BUTTON_SIZE * column) + (gap * column) + (gap / 2))
        y_start = round((BUTTON_SIZE * row) + (gap * row) + (gap / 2))
        x_end = x_start + BUTTON_SIZE
        y_end = y_start + BUTTON_SIZE

        if shape == "square":
            return self.c.create_rectangle(x_start, y_start, x_end, y_end, fill=fill, outline=outline)
        elif shape == "circle":
            shrink = BUTTON_SIZE / 10
            return self.c.create_oval(
                x_start + shrink, y_start + shrink, x_end - shrink, y_end - shrink,
                fill=fill, outline=outline,
            )

    def draw_canvas(self):
        if self.last_clicked != None:
            if self.outline_box == None:
                gap = int(BUTTON_SIZE // 4)

                x_start = round((BUTTON_SIZE * self.last_clicked[0]) + (gap * self.last_clicked[0]))
                y_start = round((BUTTON_SIZE * self.last_clicked[1]) + (gap * self.last_clicked[1]))
                x_end = round(x_start + BUTTON_SIZE + gap)
                y_end = round(y_start + BUTTON_SIZE + gap)
                
                if (self.last_clicked[1] == 0) or (self.last_clicked[0] == 8):
                    self.outline_box = self.c.create_oval(x_start + (gap // 2), y_start + (gap // 2), x_end - (gap // 2), y_end - (gap // 2), fill=SELECT_COLOR, outline="")
                else:
                    self.outline_box = self.c.create_rectangle(x_start, y_start, x_end, y_end, fill=SELECT_COLOR, outline="")
                self.c.tag_lower(self.outline_box)
        else:
            if self.outline_box != None:
                self.c.delete(self.outline_box)
                self.outline_box = None
        
        if self.grid_drawn:
            for x in range(8):
                y = 0
                fill = theme.display_pad_color(lp_colors.getXY_RGB(x, y))
                self.c.itemconfig(self.grid_rects[x][y], fill=fill, outline=theme.pad_outline_for(fill))

            for y in range(1, 9):
                x = 8
                fill = theme.display_pad_color(lp_colors.getXY_RGB(x, y))
                self.c.itemconfig(self.grid_rects[x][y], fill=fill, outline=theme.pad_outline_for(fill))

            for x in range(8):
                for y in range(1, 9):
                    fill = theme.display_pad_color(lp_colors.getXY_RGB(x, y))
                    self.c.itemconfig(self.grid_rects[x][y], fill=fill, outline=theme.pad_outline_for(fill))
            
            self.c.itemconfig(self.grid_rects[8][0], text=self.button_mode.capitalize(), fill=theme.TEXT)
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
            
            gap = int(BUTTON_SIZE // 4)
            text_x = round((BUTTON_SIZE * 8) + (gap * 8) + (BUTTON_SIZE / 2) + (gap / 2))
            text_y = round((BUTTON_SIZE / 2) + (gap / 2))
            self.grid_rects[8][0] = self.c.create_text(
                text_x, text_y,
                text=self.button_mode.capitalize(),
                font=theme.FONT_MODE,
                fill=theme.TEXT,
            )
            
            self.grid_drawn = True

    def clear_canvas(self):
        self.c.delete("all")
        self.grid_rects = [[None for y in range(9)] for x in range(9)]
        self.grid_drawn = False

    def script_entry_window(self, x, y, text_override=None, color_override=None):
        global color_to_set
        
        w = tk.Toplevel(self)
        w.winfo_toplevel().title("Edit Button (" + str(x) + ", " + str(y) + ")")
        w.resizable(False, False)
        w.configure(bg=theme.BG)
        self._set_toplevel_icon(w)
        
        def validate_func():
            nonlocal x, y, t
            
            text_string = t.get(1.0, tk.END)
            try:
                script_validate = scripts.validate_script(text_string)
            except:
                #self.save_script(w, x, y, text_string) # This will fail and throw a popup error
                self.popup(w, "Script Validation Error", self.error_image, "Fatal error while attempting to validate script.\nPlease see LPHK.log for more information.", "OK")
                raise
            if script_validate != True and files.in_error:
                self.save_script(w, x, y, text_string)
            else:
                w.destroy()
        w.protocol("WM_DELETE_WINDOW", validate_func)

        e_m = tk.Menu(w)
        w.config(menu=e_m)

        e_m_Script = tk.Menu(e_m, tearoff=False)

        body = tk.Frame(w, bg=theme.BG, padx=theme.PAD_LG, pady=theme.PAD_LG)
        body.grid(column=0, row=0, sticky="nsew")

        tk.Label(
            body,
            text="Edit Button (" + str(x) + ", " + str(y) + ")",
            bg=theme.BG,
            fg=theme.TEXT,
            font=theme.FONT_UI_BOLD,
            anchor="w",
        ).grid(column=0, row=0, columnspan=2, sticky="ew", pady=(0, theme.PAD))

        editor_frame = tk.Frame(
            body,
            bg=theme.SURFACE,
            highlightbackground=theme.BORDER,
            highlightthickness=1,
            bd=0,
        )
        editor_frame.grid(column=0, row=1, padx=(0, theme.PAD), sticky="nsew")

        t = tk.scrolledtext.ScrolledText(editor_frame, width=48, height=16)
        t.pack(fill="both", expand=True, padx=1, pady=1)
        theme.style_scrolled_text(t)
        
        if text_override == None:
            t.insert(tk.INSERT, scripts.text[x][y])
        else:
            t.insert(tk.INSERT, text_override)
        t.bind("<<Paste>>", self.custom_paste)
        t.bind("<Control-Key-a>", self.select_all)

        import_script_func = lambda: self.import_script(t, w)
        e_m_Script.add_command(label="Import script", command=import_script_func)
        export_script_func = lambda: self.export_script(t, w)
        e_m_Script.add_command(label="Export script", command=export_script_func)
        e_m.add_cascade(label="Script", menu=e_m_Script)

        actions = tk.Frame(body, bg=theme.BG)
        actions.grid(column=1, row=1, sticky="n")
        
        if color_override == None:
            colors_to_set[x][y] =  lp_colors.getXY(x, y)
        else:
            colors_to_set[x][y] = color_override
        
        if type(colors_to_set[x][y]) == int:
            colors_to_set[x][y] = lp_colors.code_to_RGB(colors_to_set[x][y])
        
        if all(c < 4 for c in colors_to_set[x][y]):
            if lp_mode == "Mk1":
                colors_to_set[x][y] = MK1_DEFAULT_COLOR
            else:
                colors_to_set[x][y] = DEFAULT_COLOR
        
        ask_color_func = lambda: self.ask_color(w, color_button, x, y, colors_to_set[x][y])
        color_button = tk.Button(actions, text="Select Color", command=ask_color_func)
        color_button.pack(fill="x", pady=(0, 10))
        color_button.config(font=BUTTON_FONT, relief=tk.FLAT, borderwidth=0, padx=theme.BUTTON_PAD_X, pady=theme.BUTTON_PAD_Y, cursor="hand2")
        start_color_str = lp_colors.list_RGB_to_string(colors_to_set[x][y])
        self.button_color_with_text_update(color_button, start_color_str)

        save_script_func = lambda: self.save_script(w, x, y, t.get(1.0, tk.END))
        save_button = tk.Button(actions, text="Bind Button (" + str(x) + ", " + str(y) + ")", command=save_script_func)
        save_button.pack(fill="x", pady=(0, 10))
        theme.style_primary_button(save_button)

        unbind_func = lambda: self.unbind_destroy(x, y, w)
        unbind_button = tk.Button(actions, text="Unbind Button (" + str(x) + ", " + str(y) + ")", command=unbind_func)
        unbind_button.pack(fill="x")
        theme.style_danger_button(unbind_button)

        # Example scripts — click a chip to load a starter into the editor
        examples_frame = tk.Frame(body, bg=theme.BG)
        examples_frame.grid(column=0, row=2, columnspan=2, sticky="ew", pady=(theme.PAD, 0))

        example_tip = tk.Label(
            examples_frame,
            text="Examples — click to load into the editor (edit before binding)",
            bg=theme.BG,
            fg=theme.TEXT_SECONDARY,
            font=theme.FONT_HINT,
            anchor="w",
        )
        example_tip.pack(fill="x", pady=(0, 6))

        chips = tk.Frame(examples_frame, bg=theme.BG)
        chips.pack(fill="x")

        tip_detail = tk.Label(
            examples_frame,
            text="Hover a button for a short description.",
            bg=theme.BG,
            fg=theme.TEXT_SECONDARY,
            font=theme.FONT_HINT,
            anchor="w",
        )
        tip_detail.pack(fill="x", pady=(8, 0))

        def load_example(script_text, tip_text):
            t.delete("1.0", tk.END)
            t.insert(tk.INSERT, script_text.rstrip() + "\n")
            tip_detail.configure(text=tip_text)
            t.focus_set()

        cols = 4
        for idx, example in enumerate(script_examples.EXAMPLES):
            btn = tk.Button(
                chips,
                text=example["label"],
                command=partial(load_example, example["script"], example["tip"]),
            )
            theme.style_chip_button(btn)
            btn.grid(
                row=idx // cols,
                column=idx % cols,
                sticky="ew",
                padx=(0 if idx % cols == 0 else 4, 0),
                pady=(0 if idx < cols else 4, 0),
            )
            btn.bind(
                "<Enter>",
                lambda _e, tip=example["tip"]: tip_detail.configure(text=tip),
            )
        for col in range(cols):
            chips.columnconfigure(col, weight=1)

        w.wait_visibility()
        w.grab_set()
        t.focus_set()
        w.wait_window()

    def classic_askcolor(self, color=(255, 0, 0), title="Color Chooser"):
        w = tk.Toplevel(self)
        w.winfo_toplevel().title(title)
        w.resizable(False, False)
        w.configure(bg=theme.BG)
        self._set_toplevel_icon(w)
        
        w.protocol("WM_DELETE_WINDOW", w.destroy)
        
        color = ""
        
        def return_color(col):
            nonlocal color
            color = col
            w.destroy()

        tk.Label(
            w,
            text=title,
            bg=theme.BG,
            fg=theme.TEXT,
            font=theme.FONT_UI_BOLD,
        ).grid(row=0, column=0, padx=theme.PAD_LG, pady=(theme.PAD_LG, theme.PAD), sticky="w")
        
        button_frame = tk.Frame(w, bg=theme.BG)
        button_frame.grid(row=1, column=0, padx=theme.PAD_LG, pady=(0, theme.PAD_LG))
        
        def make_grid_button(column, row, color_hex, func=None, size=100):
            nonlocal w
            f = tk.Frame(button_frame, width=size, height=size, bg=theme.BG)

            b = tk.Button(f, command=func, relief=tk.FLAT, borderwidth=0, cursor="hand2")
            
            f.rowconfigure(0, weight = 1)
            f.columnconfigure(0, weight = 1)
            f.grid_propagate(0)
            
            f.grid(column=column, row=row)
            b.grid(padx=(0, 8), pady=(0, 8), sticky="nesw")
            b.config(bg=color_hex, activebackground=color_hex)
        
        def make_color_button(button_color, column, row, size=100):
            button_color_hex = "#%02x%02x%02x" % button_color
            
            b_func = lambda: return_color(button_color)
            make_grid_button(column, row, button_color_hex, b_func, size)
        
        for c in range(4):
            for r in range(4):
                if not (c == 0 and r == 3):
                    red = int(c * (255 / 3))
                    green = int((3 - r) * (255 / 3))
                    
                    make_color_button((red, green, 0), c, r, size=75)

        w.wait_visibility()
        w.grab_set()
        w.wait_window()
        
        if color:
            hex = "#%02x%02x%02x" % color
            return color, hex
        else:
            return None, None
       
    def ask_color(self, window, button, x, y, default_color):
        global colors_to_set
        
        if lp_mode == "Mk1":
            color = self.classic_askcolor(color=tuple(default_color), title="Select Color for Button (" + str(x) + ", " + str(y) + ")")
        else:
            color = tkcolorpicker.askcolor(color=tuple(default_color), parent=window, title="Select Color for Button (" + str(x) + ", " + str(y) + ")")
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
        try:
            script_validate = scripts.validate_script(script_text)
        except:
            self.popup(window, "Script Validation Error", self.error_image, "Fatal error while attempting to validate script.\nPlease see LPHK.log for more information.", "OK", end_command = open_editor_func)
            raise
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
                                             initialdir=files.SCRIPT_PATH,
                                             title="Import script",
                                             filetypes=load_script_filetypes)
        if name:
            text = files.import_script(name)
            text = files.strip_lines(text)
            textbox.delete("1.0", tk.END)
            textbox.insert(tk.INSERT, text)

    def export_script(self, textbox, window):
        name = tk.filedialog.asksaveasfilename(parent=window,
                                               initialdir=files.SCRIPT_PATH,
                                               title="Export script",
                                               filetypes=save_script_filetypes)
        if name:
            if files.SCRIPT_EXT not in name:
                name += files.SCRIPT_EXT
            text = textbox.get("1.0", tk.END)
            text = files.strip_lines(text)
            files.export_script(name, text)

    def popup(self, window, title, image, text, button_text, end_command=None):
        popup = tk.Toplevel(window)
        popup.resizable(False, False)
        popup.configure(bg=theme.BG)
        self._set_toplevel_icon(popup)
        popup.wm_title(title)
        popup.tkraise(window)

        def run_end():
            popup.destroy()
            if end_command != None:
                end_command()

        body = tk.Frame(popup, bg=theme.BG, padx=theme.PAD_LG, pady=theme.PAD_LG)
        body.grid(column=0, row=0)

        picture_label = tk.Label(body, image=image, bg=theme.BG)
        picture_label.photo = image
        picture_label.grid(column=0, row=0, rowspan=3, padx=(0, theme.PAD_LG), pady=0)

        tk.Label(
            body,
            text=title,
            bg=theme.BG,
            fg=theme.TEXT,
            font=theme.FONT_UI_BOLD,
            justify=tk.LEFT,
            anchor="w",
        ).grid(column=1, row=0, sticky="w", pady=(0, 8))

        tk.Label(
            body,
            text=text,
            bg=theme.BG,
            fg=theme.TEXT_SECONDARY,
            font=theme.FONT_DIALOG_BODY,
            justify=tk.LEFT,
            anchor="w",
        ).grid(column=1, row=1, sticky="w", pady=(0, theme.PAD))

        btn = tk.Button(body, text=button_text, command=run_end)
        theme.style_primary_button(btn)
        btn.grid(column=1, row=2, sticky="e")

        popup.wait_visibility()
        popup.grab_set()
        popup.wait_window()
    
    def popup_choice(self, window, title, image, text, choices):
        popup = tk.Toplevel(window)
        popup.resizable(False, False)
        popup.configure(bg=theme.BG)
        self._set_toplevel_icon(popup)
        popup.wm_title(title)
        popup.tkraise(window)
        
        def run_end(func):
            popup.destroy()
            if func != None:
                func()

        body = tk.Frame(popup, bg=theme.BG, padx=theme.PAD_LG, pady=theme.PAD_LG)
        body.grid(column=0, row=0)

        picture_label = tk.Label(body, image=image, bg=theme.BG)
        picture_label.photo = image
        picture_label.grid(column=0, row=0, rowspan=3, padx=(0, theme.PAD_LG), pady=0)

        tk.Label(
            body,
            text=title,
            bg=theme.BG,
            fg=theme.TEXT,
            font=theme.FONT_UI_BOLD,
            justify=tk.LEFT,
            anchor="w",
        ).grid(column=1, row=0, columnspan=max(1, len(choices)), sticky="w", pady=(0, 8))

        tk.Label(
            body,
            text=text,
            bg=theme.BG,
            fg=theme.TEXT_SECONDARY,
            font=theme.FONT_DIALOG_BODY,
            justify=tk.LEFT,
            anchor="w",
        ).grid(column=1, row=1, columnspan=max(1, len(choices)), sticky="w", pady=(0, theme.PAD))

        btn_row = tk.Frame(body, bg=theme.BG)
        btn_row.grid(column=1, row=2, columnspan=max(1, len(choices)), sticky="e")

        for idx, choice in enumerate(choices):
            run_end_func = partial(run_end, choice[1])
            btn = tk.Button(btn_row, text=choice[0], command=run_end_func)
            # Last non-cancel action as primary when multiple; Cancel as secondary
            label_lower = choice[0].lower()
            if label_lower in ("cancel", "discard", "ignore"):
                theme.style_secondary_button(btn)
            elif idx == 0 or label_lower in ("ok", "save", "overwrite", "redetect now", "done"):
                theme.style_primary_button(btn)
            else:
                theme.style_secondary_button(btn)
            btn.pack(side=tk.LEFT, padx=(8 if idx else 0, 0))

        popup.wait_visibility()
        popup.grab_set()
        popup.wait_window()
    
    def modified_layout_save_prompt(self):
        if files.layout_changed_since_load == True:
            layout_empty = True
            for x_texts in scripts.text:
                for text in x_texts:
                    if text != "":
                        layout_empty = False
                        break
            
            if not layout_empty:
                self.popup_choice(self, "Save Changes?", self.warning_image, "You have made changes to this layout.\nWould you like to save this layout before exiting?", [["Save", self.save_layout], ["Save As...", self.save_layout_as], ["Discard", None]])

def make():
    global root
    global app
    global root_destroyed
    global redetect_before_start
    root = tk.Tk()
    root_destroyed = False
    root.protocol("WM_DELETE_WINDOW", close)
    root.resizable(False, False)
    root.configure(bg=theme.BG)
    if MAIN_ICON != None:
        if os.path.splitext(MAIN_ICON)[1].lower() == ".gif":
            root.call('wm', 'iconphoto', root._w, tk.PhotoImage(file=MAIN_ICON))
        else:
            root.iconbitmap(MAIN_ICON)
    app = Main_Window(root)
    app.raise_above_all()
    app.after(100, app.connect_lp)
    app.mainloop()


def close():
    global root_destroyed, launchpad
    app.modified_layout_save_prompt()
    app.disconnect_lp()

    if not root_destroyed:
        root.destroy()
        root_destroyed = True
