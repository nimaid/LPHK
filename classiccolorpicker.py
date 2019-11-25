import tkcolorpicker

def askcolor(color="red", parent=None, title="Color Chooser"):
    #TODO: Make a better color picker for the classic
    color = tkcolorpicker.askcolor(color=color, parent=parent, title=title)
    
    return color
    