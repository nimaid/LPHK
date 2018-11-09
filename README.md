# LPHK (LaunchPad HotKey)
A Novation Launchpad macro scripting system.

![Update 2](https://raw.githubusercontent.com/nimaid/LPHK/master/README_FILES/LPHK_update_2.png)

[First Look](https://www.youtube.com/watch?v=zZPt_lknhks)

[Scheduling System](https://www.youtube.com/watch?v=rv2YmPQvMr0&t=164s)

[Hackaday Early Writeup](https://hackaday.com/2018/11/04/launchpad-midi-controller-put-to-work-with-python/)

[DOOM on a Launchpad](https://www.youtube.com/watch?v=4o_fh3n8FME)

[Mouse Commands Demo - Maze](https://www.youtube.com/watch?v=w1YGSpT6aI8)

## What does it do?
The goal of this project is to implement a macro scripting system for the Novation Launchpad, in order to use the launchpad as a scriptable, general purpose macro keyboard.

It uses "LPHKscript", a very simple scripting language similar to [DuckyScript](https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Duckyscript), and has a GUI to enter scripts, set colors, and to save/load your setup.

I have specifically chosen to do my best to develop this using as many cross platform libraries as possible, with a hard requirement that Linux and Windows be supported, and a strong preference for Mac as well. The GUI is driven by TK, which works on all of the above plus Unix. The interface with the launchpad and several script functions are built on pygame, which is compatable with basically everything ever. Pretty much everything else is standard Python 3.

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
Yes! It does not have all the features I want just yet, and still has bugs, but it works! You can use the GUI to load/save layouts and edit button scripts/colors. It's not nearly as polished as I want yet, but it is functional!

This is still WIP and still a beta version. See below for a todo list. I have a life (a crazy one at that), so no promises on a delivery date. Feel free to offer your help!

## How do I use it?
Before using the program, there are some dependencies/libraries that you will need to install:

### Linux Install/Run Instructions
* Simply clone the project and run `install_dependencies.sh`. If it fails, run with `sudo`.
* Many distros will let you double click on `LPHK.py` to run it. If yours doesn't, look up how to associate `.py` files with the `python3` binary on your distro.
  * At this point, you should be able to use whatever functionality the program currently has.
  * If you have errors (or nothing happens), run the script in the command line by running "python3 LPHK.py" in the LPHK directory. Please open an issue on GitHub and copy the output when trying and failing to run via command prompt.

### Windows Install/Run Instructions
* First, download the lastest release of Python 3.x from https://www.python.org/.
* Install it, make a note of the default install location.
  * I suggest checking the option "Add Python 3.x to PATH", as it lets you easily use Python from the command line.
  * If performing a "Custom Installation" of Python 3, ensure "pip" and "tcl/tk and IDLE" are selected for install, at minimum.
* Clone LPHK into a folder of your choice. You can move the folder later, even to a USB drive.
* Run "install_dependencies.bat" to install required libraries via pip, which you just installed with Python 3.
* After installing all dependencies, right click on LPHK.py and select "Open with", then "Look for another app on this PC". Browse to that install location you noted earlier and select "python.exe".
  * At this point, you should be able to use whatever functionality the program currently has.
  * If you have errors (or nothing happens), run the script in the command line by running "python3 LPHK.py" in the LPHK directory. Please open an issue on GitHub and copy the output when trying and failing to run via command prompt.
    * (If this fails, use "python LPHK.py".)

### Post-Install Instructions
* Before starting the program, make sure your Launchpad MkII (for now, Pro and others are coming) is connected to the computer.
* Click `Launchpad > Connect to Launchpad MkII...`.
  * If the connection is successful, the grid will appear, and the status bar at the bottom will turn green.
* Click on a button to open the Script Edit window for that button.
  * All scripts are saved in the `.LPHKlayout` files, but the editor also has the ability to import/export single `.LPHKscript` files.
    * For examples, you can click `Import Script` and look through the `user_scripts/examples/` folder.
  * Select the button color and brightness, then click `Bind Button (x, y)`.
    * If there are syntax errors, this is when they will be caught, and you will be informed without the editor closing.
* Go to `Layout > Save layout as...` to save your current layout for future use, colors and all.
* Go to `Layout > Load layout...` to load an existing layout. Examples are in `user_layouts/examples/`.

#### The whole GUI is still rough around the edges, so don't be too supprised if something breaks. If it does, kindly open a detailed issue on GitHub so I can fix the error. :) And don't feel shy making feature requests, either!

## What is LPHKscript?
LPHKscript is a simple macro scripting language tailor made for LPHK. Syntax is closer to a shell/batch script than, say, JavaScript.

### Scheduling
Only one script runs at a time, and there is a sceduling system for them. If a script is scheduled, it's button will pulse red. If the script is running, the button will flash red quickly. This is true for the 8x8 grid, however, the function keys cannot flash or pulse, as a hardware limitation. These keys will be bright orange for scheduled and bright red for running.

When you press a script button, if there is a script running, it adds the script to the queue. If no scripts are running, the script is added to the queue and the queue execution is started. Tapping a scheduled script's button will unschedule it, and tapping a running scripts button will kill it. If that sounds confusing, load up `user_layouts/examples/all_delays_all_day.LPHKlayout` and press a bunch of buttons.

### The `@ASYNC` Header
There is one exception to the scheculing system. If the first line of a script is `@ASYNC`, the script will run in the background and will not interact with the other scripts. It can still be prematurely killed by tapping the button. If this is used, it must be on the very first line.

### Comments
Any line that starts with a dash `-` will be considered a comment, and will be ignored by the syntax validator/script parser. If `@ASYNC` is used, a comment cannot come before the `@ASYNC` command, as that must be on the first line, always.

### Commands List
Commands follow the format: `COMMAND arg1 arg2 ...`. Scripts are just a text file with newlines seperating commands.

* **Utility**
  * `DELAY`
    * Delays the script for (argument 1) seconds.
  * `SOUND`
    * Play a sound named (argument 1) inside the `user_sounds/` folder.
      * Supports `.wav` and `.ogg` only.
    * If (argument 2) supplied, set volume to (argument 2).
      * Range is 0 to 100
  * `WAIT_UNPRESSED`
    * Waits until the button the script is bound to is unpressed. (no arguments)
  * `WEB`
    * Open website (argument 1) in default browser.
  * `WEB_NEW`
    * Open website (argument 1) in default browser, try new window.
* **Keyboard**
  * `PRESS`
    * Presses normal character (argument 1).
      * Accepts any non-whitespace single character.
  * `RELEASE`
    * Releases the normal character (argument 1).
      * Accepts any non-whitespace single character.
  * `STRING`
    * Types whatever text comes after it.
  * `TAP`
    * Taps the normal character (argument 1).
      * Accepts any non-whitespace single character.
    * If (argument 2) supplied, tap (argument 2) number of times.
    * If (argument 3) supplied,  delay (argument 3) seconds before releasing each time.
  * `SP_PRESS`
    * Presses the special character (argument 1).
      * See below for a list of valid key names.
  * `SP_RELEASE`
    * Releases the special character (argument 1).
      * See below for a list of valid key names.
  * `SP_TAP`
    * Taps the special character (argument 1).
        * See below for a list of valid key names.
    * If (argument 2) supplied, tap (argument 2) number of times.
    * If (argument 3) supplied,  delay (argument 3) seconds before releasing each time.
* **Mouse**
  * `M_LINE`
    * Move the mouse in a line from absolute point (argument 1),(argument 2) to absolute point (argument 3),(argument 4).
    * If (argument 5) supplied, delay (argument 5) milliseconds between each step.
    * If (argument 6) supplied, move (argument 6) pixels per step.
      * If not supplied, assumed to be 1
  * `M_LINE_MOVE`
    * Move the mouse cursor in a line (argument 1) horizontally and (argument 2) vertically, relative to current position
    * If (argument 3) supplied, delay (argument 3) milliseconds between each step.
    * If (argument 4) supplied, move (argument 4) pixels per step.
      * If not supplied, assumed to be 1
  * `M_LINE_SET`
    * Move the mouse cursor in a line to absolute point (argument 1),(argument 2)
    * If (argument 3) supplied, delay (argument 3) milliseconds between each step.
    * If (argument 4) supplied, move (argument 4) pixels per step.
      * If not supplied, assumed to be 1
  * `M_MOVE`
    * Moves the mouse cursor (argument 1) horizontally and (argument 2) vertically, relative to current position.
  * `M_PRESS`
    * Presses the mouse button (argument 1).
      * See below for a list of valid button names.
  * `M_RELEASE`
    * Releases the mouse button (argument 1).
      * See below for a list of valid button names.
  * `M_SCROLL`
    * Scrolls the mouse vertically by (argument 1).
    * If (argument 2) supplied, scroll horizontally by (argument 2).
  * `M_SET`
    * Sets the absolute cursor posistion to (argument 1) horizontal and (argument 2) vertical.
  * `M_TAP`
    * Taps the mouse button (argument 1).
        * See below for a list of valid mouse button names.
    * If (argument 2) supplied, tap (argument 2) number of times.
    * If (argument 3) supplied,  delay (argument 3) seconds before releasing each time.


For all commands, the arguments cannot contain the following strings, as they are reserved for the LPHKlayout file format:
* `:LPHK_BUTTON_SEP:`
* `:LPHK_ENTRY_SEP:`
* `:LPHK_NEWLINE_REP:`

For `M_PRESS`, `M_RELEASE`, and `M_TAP`, the folowing button names are allowed:
* `left`
* `middle`
* `right`

For the `SP_` commands, the following key names are allowed:
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
* Support for Launchpad Pro
* Support for Launchpad Classic/S/Mini
  * Includes Behringer CMD Touch TC64 in Novation compatability mode
* Add generalized macro recorder wizard (!!!)
* Add `M_STORE`, `M_RECALL`, and `M_RECALL_LINE` functions to remember where the mouse was before execution
* Add `LABEL` and `GOTO_LABEL` commands
* Add `REPEAT_LABEL` command to jump from this line to a `LABEL` n number of times max
  * Defaults to 1
* Add `IF_PRESSED_GOTO_LABEL` command to jump from this line to a `LABEL` if the key is still pressed
* Add `IF_UNPRESSED_GOTO_LABEL` command to jump from this line to a `LABEL` if the key is unpressed
* Add `IF_PRESSED_REPEAT_LABEL` command to jump from this line to a `LABEL` if the key is still pressed n number of times max
  * Defaults to 1
* Add `IF_UNPRESSED_REPEAT_LABEL` command to jump from this line to a `LABEL` if the key is unpressed n number of times max
  * Defaults to 1
* Make `Add Command...` menu that acts as a guided helper for making commands
* Add mouse event capture prompts to `Add Command...` menu boxes
* Add keyboard event capture (incl. unknown keycodes) to `Add Commands...` menu boxes
* Add GUI scaling
* Add script status icons (bound, playing, queued)
* Add `CMD` command to run OS commands
  * Make multi-level scary warning dialog boxes when binding to a button (incl during load layout)
  * Give option (and strongly reccomend its use) for users to run command once and verify it does what they want before binding to button (incl during load layout)
* Add `@LOAD_LAYOUT` header command to load a specified layout
  * Check if layout currently exists when binding to a button (incl during load layout)
    * If not, prompt user if they want to continue anyway
* Add feature to SOUND to check if file currently exists when binding to a button (incl during load layout)
  * If not, prompt user if they want to continue anyway
* MIDI output command? (Low priority)
* Load layout command? (That could get messy, maybe not a script func, but a seperate GUI option to bind loading a specific layout)

## What have you done so far?
* ~~Support for Launchpad MkII~~
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
* ~~Add `M_MOVE`, `M_TAP`, `M_SCROLL`, and `M_SET` commands~~
* ~~Add `M_PRESS`, `M_RELEASE`, and `M_TAP` commands~~
* ~~Put save/load script into menu~~
* ~~Add `M_LINE`, `M_LINE_SET`, and `M_LINE_MOVE` commands~~
* ~~Add a `WAIT_UNPRESSED` command that delays while the button the script is bound to is pressed~~
* ~~Add `@ASYNC` header command to run script independent of other scripts~~
* ~~Add launchpad connection status indicator/remove popups~~
* ~~Add commenting script lines~~
* ~~Make pressing a running/queued button cancel/terminate execution~~
* ~~Make queued/playing buttons blink instead of be solid~~ (Big shout out to FMMT666 for [adding the features I needed to launchpad.py](https://github.com/FMMT666/launchpad.py/issues/31)!)
* ~~Make user defined colors RGB~~
* ~~Add RGB color selector~~
