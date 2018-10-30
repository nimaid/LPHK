import lp_colors, scripts

PATH = None
LAYOUT_EXT = ".LPHKlayout"
LAYOUT_PATH = "/user_layouts/"
SCRIPT_EXT = ".LPHKscript"
SCRIPT_PATH = "/user_scripts/"
BUTTON_SEPERATOR = ":LPHK_BUTTON_SEP:"
ENTRY_SEPERATOR = ":LPHK_ENTRY_SEP:"


curr_layout = None

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
                color = str(lp_colors.curr_colors[x][y])
                f.write(color)

                f.write(ENTRY_SEPERATOR)

                script_text = scripts.text[x][y].replace("\n", "\\n")
                f.write(script_text)

                if y < 8:
                    f.write(BUTTON_SEPERATOR)
            f.write("\n")
    print("[files] Saved layout as " + final_path)

def load_layout(name, add_path=True):
    global curr_layout
    scripts.unbind_all()
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
                color = int(info[0])
                script_text = info[1].replace("\\n", "\n")

                if script_text != "":
                    scripts.bind(x, y, script_text, color)
                else:
                    lp_colors.setXY(x, y, color)
    curr_layout = final_path
    print("[files] Loaded layout " + final_path)

def load_script(name, x=-1, y=-1, color=scripts.COLOR_DEFAULT):
    script_string = ""
    with open(PATH + SCRIPT_PATH + name + SCRIPT_EXT, "r") as f:
        l = f.readlines()

        for line in l:
            script_string += line

    script_string = script_string.rstrip()
    if (x >= 0) and (y >= 0):
        scripts.bind(x, y, script_string, color)
    elif (x >= 0) or (y >= 0):
        raise Exception("You must either set both x and y as positive numbers, or set neither")
    else:
        return script_string
