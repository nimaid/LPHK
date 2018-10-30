# LPHK (LaunchPad HotKey)
A Novation Launchpad macro scripting system.

## What does it do?
The goal of this project is to implement a macro scripting system for the Novation Launchpad, in order to use the launchpad as a scriptable, general purpose macro keyboard.

It uses "LPHKscript", a very simple scripting language similar to [DuckyScript](https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Duckyscript), and will have a GUI to enter scripts, set colors, and to save/load your setup.

## Why would you do that?
Because it could be immensely useful for a wide variety of tasks, such as:
* Gaming, to bind:
  * Items
  * Volume
  * Attacks
  * Typed commands
  * Reference Website launcher
  * Window switcher
* Editing, to bind:
  * Cuts/insertions
  * Modes
  * Effects
  * Render
  * Preview
  * Scrubbing
* Programming, to bind:
  * Commenting code
  * Autotyping function/loop templates
  * Compiling/excuting
  * Breakpoints
  * Debugger
* ... and many more!

## Does it work yet?
Yes! It does not have all the features I want just yet, and still has bugs, but it works! You can use the GUI to load/save layouts and edit button scripts/colors. It's still buggy, and not nearly as polished as I want yet, but it is functional!

This is still WIP and still a beta version. See below for a todo list. I have a life (a crazy one at that), so no promises on a delivery date. Feel free to offer your help!

## How do I use it?
Plug your Launchpad MkII (for now, Pro and others are coming) in, then run LPHK.py with Python 3, either through IDLE or "python3 LPHK.py".

Go to "Layout > Load layout..." to load an existing layout. See the user_layouts/examples/ folder for more info.

The whole GUI is still rough around the edges, so don't be too supprised if something breaks. If it does, kindly open a detailed issue on GitHub so I can fix the error. :)

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
* `SOUND` - play a sound named (argument 1) inside the `user_sounds/` folder, `.wav` and `.ogg` only

For all commands, the arguments cannot contain the following strings:
* `:LPHK_BUTTON_SEP:`
* `:LPHK_ENTRY_SEP:`

For the `SP_` functions, the following values are allowed:
* `alt`
* `alt_gr`
* `alt_r`
* `backspace`
* `bright_down`
* `bright_up`
* `caps_lock`
* `cmd`
* `cmd_r`
* `crtl`
* `ctrl_r`
* `delete`
* `down`
* `end`
* `enter`
* `esc`
* `f1` - `f20`
* `home`
* `insert`
* `left`
* `menu`
* `mute`
* `next_track`
* `num_lock`
* `page_down`
* `page_up`
* `pause`
* `play_pause`
* `prev_track`
* `print_screen`
* `right`
* `scroll_lock`
* `shift`
* `shift_r`
* `space`
* `tab`
* `up`
* `vol_down`
* `vol_up`

## What still needs to be written?
* ~~MkII spacific interface~~
* Support for all launchpads
* ~~Events system~~
* ~~Colors system~~
* ~~LPScript base iteration~~
* ~~Keyboard lib base~~
* ~~Proof of concept demo~~
* ~~Saving/Loading~~
* ~~Sound functionality~~
* ~~Basic GUI~~
* ~~Save/load single scripts in GUI~~
* ~~Script entry error checking~~
* ~~Add launchpad connection menu~~
* Add a REPEAT command to do last command n number of times
* ~~Add launchpad connection status indicator/remove popups~~
* Add script status icons (playing, queued)
* Make queued/playing buttons blink instead of be solid
* MIDI output command? (Low priority)
* Load layout command? (That could get messy, maybe not a script func, but a seperate GUI option to bind loading a specific layout)
