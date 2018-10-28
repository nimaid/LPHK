# LPHK
A Novation Launchpad macro scripting language

## What does it do?
The goal of this project is to implement a macro scripting system for the Novation Launchpad, in order to use the launchpad as a scriptable, general purpose macro keyboard.

It uses "LPHKscript", a very simple scripting language similar to [DuckyScript](https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Duckyscript), and will have a GUI to enter scripts, set colors, and to save/load your setup.

## Why would you do that?
Because it could be very useful for editing, gaming, programming, and even program launchers.

## Does it work yet?
Sort of! You can bind scripts to buttons, save/load layout files, and bind single script text files.

Now the GUI and extention on the scripting language are the primary concerns. See below for a todo list. I have a life (a crazy one at that), so no promises on a delivery date. Feel free to offer your help!

## How do I use it?
Plug your Launchpad MkII (for now, Pro and others are coming) in, then run LPHK.py with Python 3, either through IDLE or "python3 LPHK.py".

The default layout is a demo. You technically can do all the binding/saving/loading with the `python3` -i option, via the `scripts`, `files`, and `lp_colors` libraries. A GUI is coming, as I am learning Tkinter. Most main functionality is already bound to functions, so I only really need to make buttons and things to run those functions. :) Stay tuned.

## What is LPHKscript?
LPHKscript is a simple hotkey scripting language tailor made for LPHK. Syntax is closer to a shell/batch script than, say, JavaScript.

Commands follow the format: `COMMAND arg1 arg2 ...`. Scripts are just a text file with newlines seperating commands.

The current command list is as follows:
* `STRING` - types (argument 1)
* `DELAY` - delays the script for (argument 1) seconds
* `TAP` - taps the normal character (argument 1), if (argument 2) supplied, delay (argument 1) seconds before releasing
* `PRESS` - presses normal character (argument 1)
* `RELEASE` - releases the normal character (argument 1)
* `SP_TAP` - taps the special character (argument 1), if (argument 2) supplied, delay (argument 1) seconds before releasing
* `SP_PRESS` - presses the special character (argument 1)
* `SP_RELEASE` - releases the spacial character (argument 1)
* `WEB` - open website (argument 1) in default browser
* `WEB_NEW` - open website (argument 1) in default browser, try new window
* `VAR_SET` - sets a global variable shared between all scripts
* `VAR_SET_EQ` - sets a global variable (argument 1) to the output of the expression string (argument 2), allowed to use previously defined global variables
* `SOUND` - play a sound named (argument 1)

## What still needs to be written?
### Global
* ~~MkII spacific interface~~
* Support all launchpads
* ~~Events system~~
* ~~Colors system~~
* ~~LPScript base iteration~~
* ~~Keyboard lib base~~
* ~~Proof of concept demo~~
* ~~Saving/Loading~~
* Looping/Control Flow
* ~~Variables/Expressions~~
* ~~Sound functionality~~
* Basic GUI
