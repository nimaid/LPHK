import lp_colors, scripts, files_legacy
from time import sleep
import os, json, platform, subprocess

PATH = None

LAYOUT_PATH = "/user_layouts/"
SCRIPT_PATH = "/user_scripts/"

LAYOUT_EXT = ".lpl"
SCRIPT_EXT = ".lps"

FILE_VERSION = "0.01"

import window

curr_layout = None
in_error = False
layout_changed_since_load = False

def init(path_in):
    global PATH
    PATH = path_in

def save_layout(layout, name):
    with open(name, "w") as f:
        json.dump(layout, f)
    print("[files] Saved layout as " + name)

def load_layout(name):
    with open(name, "r") as f:
        layout = json.load(f)
    print("[files] Loaded layout " + name)
    return layout
    
def save_lp_to_layout(name):
    layout = dict()
    layout["version"] = FILE_VERSION
    
    layout["buttons"] = []
    for x in range(9):
        layout["buttons"].append([])
        for y in range(9):
            color = lp_colors.curr_colors[x][y]
            script_text = scripts.text[x][y]
            
            layout["buttons"][-1].append({"color": color, "text": script_text})
    
    save_layout(layout=layout, name=name)

def load_layout_to_lp(name):
    global curr_layout
    global in_error
    global layout_changed_since_load
    
    converted_to_rg = False
    
    scripts.unbind_all()
    window.app.draw_canvas()
    
    basename_list = os.path.basename(name).split(os.path.extsep)
    ext = basename_list[-1]
    title = os.path.extsep.join(basename_list[:-1])
    
    if "." + ext == files_legacy.LEGACY_LAYOUT_EXT:
        # TODO: Error checking on resultant JSON
        layout = files_legacy.load_legacy_layout(name)
        
        name = os.path.dirname(name) + os.path.sep + title + LAYOUT_EXT
        window.app.popup(window.app, "Legacy layout loaded...", window.app.info_image, "The layout is in the legacy .LPHKlayout format. It will be\nconverted to the new .lpl format, and will be saved as such.", "OK")
        save_layout(layout, name)
    else:
        # TODO: Error checking on loaded JSON
        try:
            layout = load_layout(name)
        except json.decoder.JSONDecodeError:
            window.app.popup(window.app, "Error loading file!", window.app.info_image, "The layout is not in valid JSON format (the new .lpl extention).\n\nIf this was renamed from a .LPHKlayout file, please change\nthe extention back to .LPHKlayout and try loading again.", "OK")
            return
        
    for x in range(9):
        for y in range(9):
            button = layout["buttons"][x][y]
            color = button["color"]
            script_text = button["text"]
        
            if window.lp_mode == "Mk1":
                if color[2] != 0:
                    color = lp_colors.RGB_to_RG(color)
                    converted_to_rg = True
            
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
        
    curr_layout = name
    if converted_to_rg:
        window.app.popup(window.app, "Layout converted to Classic/Mini/S...", window.app.info_image, "The colors in this layout have been converted to be\ncompatable with the Launchpad Classic/Mini/S.\n\nChanges have not yet been saved to the file.", "OK")
        layout_changed_since_load = True
    else:
        layout_changed_since_load = False

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