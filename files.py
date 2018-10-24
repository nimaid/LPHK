import lp_colors, scripts

PATH = None
LAYOUT_EXT = ".LPHKlayout"
LAYOUT_PATH = "/user_layouts/"
SCRIPT_EXT = ".LPHKscript"
SCRIPT_PATH = "/user_scripts/"


def init(path_in):
    global PATH
    PATH = path_in

def save_layout(name):
    with open(PATH + LAYOUT_PATH + name + LAYOUT_EXT, "w+") as f:
        for x in range(9):
            for y in range(9):
                color = str(lp_colors.curr_colors[x][y])
                f.write(color)

                f.write("~~")

                script_text = scripts.text[x][y].replace("\n", "\\n")
                f.write(script_text)

                if y < 8:
                    f.write("||")
            f.write("\n")

def load_layout(name):
    scripts.unbind_all()
    with open(PATH + LAYOUT_PATH + name + LAYOUT_EXT, "r") as f:
        l = f.readlines()

        for x in range(9):
            line = l[x][:-1].split("||")
            for y in range(9):
                info = line[y].split("~~")
                color = int(info[0])
                script_text = info[1].replace("\\n", "\n")

                if script_text != "":
                    scripts.bind(x, y, script_text, color)
                else:
                    lp_colors.setXY(x, y, color)

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
