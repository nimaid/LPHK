import lp_colors, scripts
from time import sleep
import os, platform, subprocess

PATH = None
LAYOUT_EXT = ".LPHKlayout"
LAYOUT_PATH = "/user_layouts/"
SCRIPT_EXT = ".LPHKscript"
SCRIPT_PATH = "/user_scripts/"

BUTTON_SEPERATOR = ":LPHK_BUTTON_SEP:"
ENTRY_SEPERATOR = ":LPHK_ENTRY_SEP:"
NEWLINE_REPLACE = ":LPHK_NEWLINE_REP:"

import window

curr_layout = None
in_error = False
layout_changed_since_load = False

def init(path_in):
    global PATH
    PATH = path_in

def save_layout(name, add_path=True):
    final_path = None
    if add_path:
        final_path = PATH + LAYOUT_PATH + name + LAYOUT_EXT
    else:
        final_path = name
    with open(final_path, "w+") as f:
        for x in range(9):
            for y in range(9):
                color = lp_colors.curr_colors[x][y]

                f.write(str(color[0]))
                f.write(",")
                f.write(str(color[1]))
                f.write(",")
                f.write(str(color[2]))

                f.write(ENTRY_SEPERATOR)

                script_text = scripts.text[x][y].replace("\n", NEWLINE_REPLACE)
                f.write(script_text)

                if y < 8:
                    f.write(BUTTON_SEPERATOR)
            f.write("\n")
    print("[files] Saved layout as " + final_path)

def load_layout(name, add_path=True):
    global curr_layout
    global in_error
    global layout_changed_since_load
    
    converted_to_rg = False
    
    scripts.unbind_all()
    window.app.draw_canvas()
    
    final_path = None
    if add_path:
        final_path = PATH + LAYOUT_PATH + name + LAYOUT_EXT
    else:
        final_path = name
    with open(final_path, "r") as f:
        l = f.readlines()

        for x in range(9):
            line = l[x][:-1].split(BUTTON_SEPERATOR)
            for y in range(9):
                info = line[y].split(ENTRY_SEPERATOR)
                color = None
                if not info[0].isdigit():
                    split = info[0].split(",")
                    color = []
                    color.append(int(split[0]))
                    color.append(int(split[1]))
                    color.append(int(split[2]))
                else:
                    color = lp_colors.code_to_RGB(int(info[0]))
                if window.lp_mode == "Mk1":
                    if color[2] != 0:
                        color = lp_colors.RGB_to_RG(color)
                        converted_to_rg = True
                
                script_text = info[1].replace(NEWLINE_REPLACE, "\n")
                if script_text != "":
                    script_validation = scripts.validate_script(script_text)
                    if script_validation != True:
                        lp_colors.update_all()
                        window.app.draw_canvas()
                        in_error = True
                        window.app.save_script(window.app, x, y, script_text, open_editor = True, color = color)
                        in_error = False
                    else:
                        scripts.bind(x, y, script_text, color)
                else:
                    lp_colors.setXY(x, y, color)
        lp_colors.update_all()
        window.app.draw_canvas()
    curr_layout = final_path
    if converted_to_rg:
        window.app.popup(window.app, "Layout converted to Classic/Mini/S...", window.app.info_image, "The colors in this layout have been converted to be\ncompatable with the Launchpad Classic/Mini/S.\n\nChanges have not yet been saved to the file.", "OK")
        layout_changed_since_load = True
    else:
        layout_changed_since_load = False
    print("[files] Loaded layout " + final_path)

def import_script(name, add_path=True):
    final_path = None
    if add_path:
        final_path = PATH + LAYOUT_PATH + name + LAYOUT_EXT
    else:
        final_path = name
    with open(final_path, "r") as f:
        text = f.read()
        print("[files] Imported script as " + final_path)
        return text

def export_script(name, script, add_path=True):
    final_path = None
    if add_path:
        final_path = PATH + LAYOUT_PATH + name + LAYOUT_EXT
    else:
        final_path = name
    with open(final_path, "w+") as f:
        f.write(script)
        print("[files] Exported script as " + final_path)

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