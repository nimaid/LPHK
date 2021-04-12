import lp_colors, scripts
from time import sleep
import os, json, platform, subprocess
from constants import *

LAYOUT_DIR = "user_layouts"
SCRIPT_DIR = "user_scripts"
SUBROUTINE_DIR = "user_subroutines"

FILE_VERSION = "0.1.1"         # file is unchanged if no subroutines are saved
FILE_VERSION_SUBS = "0.2"      # file version if subroutines are saved

LAYOUT_EXT = ".lpl"
SCRIPT_EXT = ".lps"
SUBROUTINE_EXT = ".lpc"

LEGACY_LAYOUT_EXT = ".LPHKlayout"
LEGACY_SCRIPT_EXT = ".LPHKscript"

USER_PATH = None
LAYOUT_PATH = None
SCRIPT_PATH = None
SUBROUTINE_PATH = None

import window

curr_layout = None
in_error = False
layout_changed_since_load = False

def init(user_path_in):
    global USER_PATH
    global LAYOUT_PATH
    global SCRIPT_PATH
    global SUBROUTINE_PATH
    USER_PATH = user_path_in
    LAYOUT_PATH = os.path.join(USER_PATH, LAYOUT_DIR)
    SCRIPT_PATH = os.path.join(USER_PATH, SCRIPT_DIR)
    SUBROUTINE_PATH = os.path.join(USER_PATH, SUBROUTINE_DIR)

def save_layout(layout, name, printing=True):
    with open(name, "w") as f:
        json.dump(layout, f, indent=2, sort_keys=True)
    if printing:
        print("[files] Saved layout as " + name)

def load_layout_json(name, printing=True):
    with open(name, "r") as f:
        layout = json.load(f)
    if printing:
        print("[files] Loaded layout " + name)
    return layout

def load_layout_legacy(name, printing=True):
    layout = dict()
    layout["version"] = "LEGACY"

    layout["buttons"] = []
    with open(name, "r") as f:
        l = f.readlines()

        for x in range(9):
            layout["buttons"].append([])
            line = l[x][:-1].split(":LPHK_BUTTON_SEP:")
            for y in range(9):
                info = line[y].split(":LPHK_ENTRY_SEP:")

                color = None
                if not info[0].isdigit():
                    split = info[0].split(",")
                    color = [int(x) for x in split[:3]]
                else:
                    color = lp_colors.code_to_RGB(int(info[0]))
                script_text = info[1].replace(":LPHK_NEWLINE_REP:", "\n")

                layout["buttons"][-1].append({"color": color, "text": script_text})
    if printing:
        print("[files] Loaded legacy layout " + name)
    return layout

def load_layout(name, popups=True, save_converted=True, printing=True):
    basename_list = os.path.basename(name).split(os.path.extsep)
    ext = basename_list[-1]
    title = os.path.extsep.join(basename_list[:-1])

    if "." + ext == LEGACY_LAYOUT_EXT:
        # TODO: Error checking on resultant JSON
        layout = load_layout_legacy(name, printing=printing)


        if save_converted:
            name = os.path.dirname(name) + os.path.sep + title + LAYOUT_EXT
            if popups:
                window.app.popup(window.app, "Legacy layout loaded...", window.app.info_image, "The layout is in the legacy .LPHKlayout format. It will be\nconverted to the new .lpl format, and will be saved as such.", "OK")
            else:
                if printing:
                    print("[files] The layout is in the legacy .LPHKlayout format. It will be converted to the new .lpl format, and will be saved as such.")
                save_layout(layout, name)
    else:
        # TODO: Error checking on loaded JSON
        try:
            layout = load_layout_json(name, printing=printing)
        except json.decoder.JSONDecodeError:
            if popups:
                window.app.popup(window.app, "Error loading file!", window.app.info_image, "The layout is not in valid JSON format (the new .lpl extention).\n\nIf this was renamed from a .LPHKlayout file, please change\nthe extention back to .LPHKlayout and try loading again.", "OK")
            raise

    return layout

def save_lp_to_layout(name):
    layout = dict()

    has_subs = False

    layout["buttons"] = []
    for x in range(9):
        layout["buttons"].append([])
        for y in range(9):
            color = lp_colors.curr_colors[x][y]
            script_text = scripts.buttons[x][y].script_str

            layout["buttons"][-1].append({"color": color, "text": script_text})

    for x in scripts.VALID_COMMANDS:               # for all the commands that exist
        if x.startswith(SUBROUTINE_PREFIX):        # if this command is a subroutine
            if not has_subs:
                layout["subroutines"] = []         # only add the key if required
                has_subs = True
            cmd = scripts.VALID_COMMANDS[x]        # get the command
            layout["subroutines"] += [cmd.routine] # add the command to the list (name is embedded in the subroutine)

    if has_subs:                                   # file version depends on the existance of subroutines
        layout["version"] = FILE_VERSION_SUBS
    else:
        layout["version"] = FILE_VERSION

    save_layout(layout=layout, name=name)

def load_layout_to_lp(name, popups=True, save_converted=True, preload=None):
    global curr_layout
    global in_error
    global layout_changed_since_load

    converted_to_rg = False

    scripts.Unbind_all()
    scripts.Unload_all()                         # remove all existing subroutines when you load a new layout
    window.Redraw(True)

    if preload == None:
        layout = load_layout(name, popups=popups, save_converted=save_converted)
    else:
        layout = preload

    # load subroutines before buttons so you don't get errors on buttons using them
    if "subroutines" in layout:                  # were subroutines saved?
        for sub in layout["subroutines"]:        # for all the subroutines that were saved
            load_subroutine(sub, 0, 'LAYOUT')    # load the subroutine

    for x in range(9):
        for y in range(9):
            button = layout["buttons"][x][y]
            color = button["color"]
            script_text = button["text"]

            if window.lp_mode == LP_MK1:
                if color[2] != 0:
                    color = lp_colors.RGB_to_RG(color)
                    converted_to_rg = True

            if script_text != "":
                script_validation = None
                try:
                    btn = scripts.Button(x, y, script_text)
                    script_validation = btn.Validate_script()
                except:
                    new_layout_func = lambda: window.app.unbind_lp(prompt_save = False)
                    if popups:
                        window.app.popup(window.app, "Script Validation Error", window.app.error_image, "Fatal error while attempting to validate script.\nPlease see LPHK.log for more information.", "OK", end_command = new_layout_func)
                    else:
                        print("[files] Fatal error while attempting to validate script.\nPlease see LPHK.log for more information.")
                    raise
                if script_validation != True:
                    btn.invalid_on_load = True
                    color = [0, 0, 0]
                else:
                    btn.invalid_on_load = False
                scripts.Bind(x, y, btn, color)
            else:
                lp_colors.setXY(x, y, color)

    lp_colors.update_all()
    window.Redraw(True)

    curr_layout = name
    if converted_to_rg:
        if popups:
            window.app.popup(window.app, "Layout converted to Classic/Mini/S...", window.app.info_image, "The colors in this layout have been converted to be\ncompatable with the Launchpad Classic/Mini/S.\n\nChanges have not yet been saved to the file.", "OK")
        else:
            print("[files] The colors in this layout have been converted to be compatable with the Launchpad Classic/Mini/S. Changes have not yet been saved to the file.")
        layout_changed_since_load = True
    else:
        layout_changed_since_load = False

# load all the subroutines in a file
def load_subroutines_to_lp(name, popups=True, preload=None):
    with open(name, 'r') as in_subs:
       subs = in_subs.read().split('\n===\n')

    loaded = []
    not_loaded = []
    s_tot = 0
    s_ok = 0
    s_fail = 0
    for i, sub in enumerate(subs):
        ok, name = load_subroutine(sub.splitlines(), i+1, name)
        name = name[5:]
        s_tot += 1
        if ok:
            s_ok += 1
            loaded.append(name)
        else:
            s_fail += 1
            not_loaded.append(name)

    s_tot = len(loaded)
    nl = '\n'

    if s_fail > 0:
        window.app.popup(window.app, "Subroutines loaded with errors", window.app.info_image, f"{s_fail} of {s_tot} subroutines not loaded due to errors:{nl}{nl}{nl.join(not_loaded)}", "OK")
    elif s_ok > 0:
        window.app.popup(window.app, "Subroutines loaded sucessfully", window.app.info_image, f"{s_tot} subroutines loaded sucessfully:{nl}{nl}{nl.join(loaded)}", "OK")
    else:
        window.app.popup(window.app, "Nothing to load", window.app.info_image, f"No subroutines found in file", "OK")

    validate_all_buttons()
    
def validate_all_buttons():
    b_tot = 0
    b_ok = 0
    b_fail = 0

    for x in range(9):
        for y in range(9):
            btn = scripts.buttons[x][y]

            if btn.script_str != "":
                b_tot += 1
                script_validation = None
                try:
                    script_validation = btn.Validate_script()
                except:
                    new_layout_func = lambda: window.app.unbind_lp(prompt_save = False)
                    if popups:
                        window.app.popup(window.app, "Script Validation Error", window.app.error_image, "Fatal error while attempting to validate script.\nPlease see LPHK.log for more information.", "OK", end_command = new_layout_func)
                    else:
                        print("[files] Fatal error while attempting to validate script.\nPlease see LPHK.log for more information.")
                    raise
                if script_validation != True:
                    b_fail += 1
                    btn.invalid_on_load = True
                else:
                    b_ok += 1
                    btn.invalid_on_load = False

    window.Redraw(True)

    if b_fail > 0:
        window.app.popup(window.app, "Buttons disabled", window.app.info_image, f"{b_fail} of {b_tot} buttons disabled due to errors", "OK")

# load a single subroutine
def load_subroutine(sub, sub_n, fname):
    import commands_subroutines
    
    while sub[0].strip() == "":              # trim leading blank lines
        sub = sub[1:]

    while sub[-1].strip() == "":             # trim trailing blank lines
        sub = sub[:-1]
    
    ok, name, params, err = commands_subroutines.Add_Function(sub, sub_n, fname) # Attempt to load the command

    if err == None:
        err = False

    return err, name

def import_script(name):
    with open(name, "r") as f:
        text = f.read()
        print("[files] Imported script as " + name)
        return text

def export_script(name, script):
    with open(name, "w+") as f:
        f.write(script)
        print("[files] Exported script as " + name)

def strip_lines(text):
    return "\n".join([line.strip() for line in text.split("\n")])

def open_file_folder(path):
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    except:
        print("[files] Could not open file or folder " + path)
