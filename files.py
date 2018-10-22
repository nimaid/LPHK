import lp_colors, scripts

PATH = None
EXT = ".LPHK"

def init(path_in):
    global PATH
    PATH = path_in + "/user_layouts/"

def save_layout(name):
    with open(PATH + name + EXT, "w+") as f:
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
    with open(PATH + name + EXT, "r") as f:
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
