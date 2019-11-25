import os
import json

BUTTON_SEPERATOR = ":LPHK_BUTTON_SEP:"
ENTRY_SEPERATOR = ":LPHK_ENTRY_SEP:"
NEWLINE_REPLACE = ":LPHK_NEWLINE_REP:"

def load_layout_to_object(name):
    layout = dict()
    
    layout["version"] = "0.01"
    
    layout["buttons"] = []
    with open(name, "r") as f:
        l = f.readlines()

        for x in range(9):
            layout["buttons"].append([])
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
                
                script_text = info[1].replace(NEWLINE_REPLACE, "\n")
                
                layout["buttons"][-1].append({"color": color, "text": script_text})
    
    return layout

def layout_to_json(source, dest=None):
    layout = load_layout_to_object(source)
    if dest == None:
        dest = source + ".json"
    with open(dest, "w") as f:
        json.dump(layout, f)
