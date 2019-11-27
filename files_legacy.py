import lp_colors

LEGACY_LAYOUT_EXT = ".LPHKlayout"
LEGACY_SCRIPT_EXT = ".LPHKscript"

LEGACY_BUTTON_SEPERATOR = ":LPHK_BUTTON_SEP:"
LEGACY_ENTRY_SEPERATOR = ":LPHK_ENTRY_SEP:"
LEGACY_NEWLINE_REPLACE = ":LPHK_NEWLINE_REP:"

def load_legacy_layout(name):
    layout = dict()
    layout["version"] = "LEGACY"
    
    layout["buttons"] = []
    with open(name, "r") as f:
        l = f.readlines()

        for x in range(9):
            layout["buttons"].append([])
            line = l[x][:-1].split(LEGACY_BUTTON_SEPERATOR)
            for y in range(9):
                info = line[y].split(LEGACY_ENTRY_SEPERATOR)
                
                color = None
                if not info[0].isdigit():
                    split = info[0].split(",")
                    color = [int(x) for x in split[:3]]
                else:
                    color = lp_colors.code_to_RGB(int(info[0]))
                
                script_text = info[1].replace(LEGACY_NEWLINE_REPLACE, "\n")
                
                layout["buttons"][-1].append({"color": color, "text": script_text})
    
    print("[files] Loaded legacy layout " + name)
    return layout

