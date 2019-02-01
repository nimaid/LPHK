# LPHK (LaunchPad HotKey)
A Novation Launchpad macro scripting system.

<a href="https://github.com/nimaid/LPHK"><img src="https://raw.githubusercontent.com/nimaid/LPHK/master/README_FILES/LPHK.png" alt="logo" height="300px" hspace="5"/></a><a href="https://discord.gg/mDCzB8X"><img src="https://raw.githubusercontent.com/nimaid/LPHK/master/README_FILES/discord.png" alt="logo" height="300px" hspace="5"/></a><a href="https://www.patreon.com/user?u=16848673"><img src="https://raw.githubusercontent.com/nimaid/LPHK/master/README_FILES/patreon.png" alt="logo" height="300px" hspace="5"/></a>
<img src="https://raw.githubusercontent.com/nimaid/LPHK/master/README_FILES/LPHK_update_3.png" alt="Update 3" width="800px" />

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
  * Automatic Glitch/Trick Execution (think ABH or propsurfing in Source)
  * Repetitive tasks (grinding)
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

This is still WIP and still a beta version. See below for a todo list. I have a life (a crazy one at that), so no promises on a delivery date. Feel free to offer your help! You can see project updates and ask questions on the [official Discord server](https://discord.gg/mDCzB8X)! You can also donate on the [official Patreon page](https://www.patreon.com/user?u=16848673) to help speed up development, or just say thanks!

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

### Program Usage (Post-Install)
* Before starting the program, make sure your Launchpad MkII (for now, Pro and others are coming) is connected to the computer.
* Click `Launchpad > Connect to Launchpad MkII...`.
  * If the connection is successful, the grid will appear, and the status bar at the bottom will turn green.
* The current mode is displayed in the upper right, in the gap between the circular buttons. Clicking this text will change the mode. There are four modes:
    * "Edit" mode: Click on a button to open the Script Edit window for that button.
      * All scripts are saved in the `.LPHKlayout` files, but the editor also has the ability to import/export single `.LPHKscript` files.
        * For examples, you can click `Import Script` and look through the `user_scripts/examples/` folder.
      * Select the button color, then click `Bind Button (x, y)`.
        * If there are syntax errors, this is when they will be caught, and you will be informed without the editor closing.
    * "Move" mode: Click on a button to highlight it, then click on a second button to move the script/color from the highlighted one.
      * The selected button will be unbound
      * The second button will have the selected button's old script and color bound to it
        * If the second button is already bound, you will get a dialog box with options.
    * "Swap" mode: Click on a button to highlight it, then click on a second button to swap the script/color with the highlighted one.
      * The selected button will have the second button's script and color bound to it.
      * The second button will have the selected button's old script and color bound to it.
    * "Copy" mode: Click on a button to highlight it, then click on a second button to copy the script/color to the highlighted one.
      * The selected button will remain unchanged.
      * The second button will have the selected button's old script and color bound to it.
        * If the second button is already bound, you will get a dialog box with options.
* Go to `Layout > Save layout as...` to save your current layout for future use, colors and all.
* Go to `Layout > Load layout...` to load an existing layout. Examples are in `user_layouts/examples/`.

#### The whole GUI is still rough around the edges, so don't be too supprised if something breaks. If it does, kindly open a detailed issue on GitHub so I can fix the error. :) And don't feel shy making feature requests, either!

## What is LPHKscript?
LPHKscript is a simple macro scripting language tailor made for LPHK. Syntax is closer to a shell/batch script than, say, JavaScript.

### Scheduling
Only one script runs at a time, and there is a scheduling system for them. If a script is scheduled, it's button will pulse red. If the script is running, the button will flash red quickly. This is true for the 8x8 grid, however, the function keys cannot flash or pulse, as a hardware limitation. These keys will be bright orange for scheduled and bright red for running.

When you press a script button, if there is a script running, it adds the script to the queue. If no scripts are running, the script is added to the queue and the queue execution is started. Tapping a scheduled script's button will unschedule it, and tapping a running scripts button will kill it. If that sounds confusing, load up `user_layouts/examples/all_delays_all_day.LPHKlayout` and press a bunch of buttons.

### Headers
Headers are commands that start with `@` and go on the first line of a script. They are used to put the scripting engine into different "modes", allowing you to do some interesting things.

#### The `@ASYNC` Header
There is one exception to the scheduling system. If the script has the `@ASYNC` header, it will run in the background and will not interact with the other scripts. It can still be prematurely killed by tapping the button. If this is used, it must be on the very first line.

#### The `@SIMPLE` Header
This is a quick way to bind a controller button to a simple keypress of (argument 1). This has the equivilant code to:
```
@ASYNC
PRESS (argument 1)
WAIT_UNPRESSED
RELEASE (argument 1)
```
If this is used, all other lines in the file must either be whitespace or comments. In addition, it must be on the very first line.

### Comments
Any line that starts with a dash `-` will be considered a comment, and will be ignored by the syntax validator/script parser. If a header is used, a comment cannot come before the header, as those must be on the first line, always.

### Commands List
Commands follow the format: `COMMAND arg1 arg2 ...`. Scripts are just a text file with newlines seperating commands.

* **Utility**
  * `DELAY`
    * Delays the script for (argument 1) seconds.
  * `GOTO_LABEL`
    * Goto label (argument 1).
  * `IF_PRESSED_GOTO_LABEL`
    * If the button the script is bound to is pressed, goto label (argument 1).
  * `IF_PRESSED_REPEAT_LABEL`
    * If the button the script is bound to is pressed, goto label (argument 1) a maximum of (argument 2) times.
  * `IF_UNPRESSED_GOTO_LABEL`
    * If the button the script is bound to is not pressed, goto label (argument 1).
  * `IF_UNPRESSED_REPEAT_LABEL`
    * If the button the script is bound to is not pressed, goto label (argument 1) a maximum of (argument 2) times.
  * `LABEL`
    * Sets a label named (argument 1) for use with the `*GOTO_LABEL` commands.
  * `REPEAT_LABEL`
    * Goto label (argument 1) a maximum of (argument 2) times.
  * `SOUND`
    * Play a sound named (argument 1) inside the `user_sounds/` folder.
      * Supports `.wav`, `.flac`, and `.ogg` only.
    * If (argument 2) supplied, set volume to (argument 2).
      * Range is 0 to 100
  * `WAIT_UNPRESSED`
    * Waits until the button the script is bound to is unpressed. (no arguments)
  * `WEB`
    * Open website (argument 1) in default browser.
  * `WEB_NEW`
    * Open website (argument 1) in default browser, try new window.
* **Keypresses**
  * `PRESS`
    * Presses the key (argument 1).
      * See valid key names below.
  * `RELEASE`
    * Releases the key (argument 1).
      * See valid key names below.
  * `STRING`
    * Types whatever text comes after it.
  * `TAP`
    * Taps the key (argument 1).
      * See valid key names below.
    * If (argument 2) supplied, tap (argument 2) number of times.
    * If (argument 3) supplied,  delay (argument 3) seconds before releasing each time.
* **Mouse Movement**
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
  * `M_RECALL`
    * Sets the mouse position to the last location stored with `M_STORE`.
      * Will not do anything if `M_STORE` has not been called in that script.
  * `M_RECALL_LINE`
    * Move the mouse cursor in a line to the last location stored with `M_STORE`.
      * Will not do anything if `M_STORE` has not been called in that script.
    * If (argument 1) supplied, delay (argument 1) milliseconds between each step.
    * If (argument 2) supplied, move (argument 2) pixels per step.
      * If not supplied, assumed to be 1
  * `M_SCROLL`
    * Scrolls the mouse vertically by (argument 1).
    * If (argument 2) supplied, scroll horizontally by (argument 2).
  * `M_SET`
    * Sets the absolute cursor posistion to (argument 1) horizontal and (argument 2) vertical.
  * `M_STORE`
    * Stores the current mouse position for use with the `M_RECALL*` commands.

For the `PRESS`, `RELEASE`, and `TAP` commands, all single character non-whitespace keys and the following key names are allowed:
* `alt`
* `alt_gr`
* `backspace`
* `caps_lock`
* `cmd`
* `crtl`
* `delete`
* `down`
* `end`
* `enter`
* `esc`
* `f1` - `f24`
* `home`
* `insert`
* `left`
* `menu`
* `mouse_left`
* `mouse_middle`
* `mouse_right`
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

For all commands, the arguments cannot contain the following strings, as they are reserved for the LPHKlayout file format:
* `LPHK_BUTTON_SEP`
* `LPHK_ENTRY_SEP`
* `LPHK_NEWLINE_REP`

## Known Issues

* If your game/application does not detect mouse movements, see if there is an option to turn off "raw input" in the settings. This setting bypasses all software and reads directly from the mouse, which you don't want for this.

## What still needs to be written? (in order of priority)
* Support for Launchpad Classic/S/Mini
  * Thanks to Patreon patron Korbinian Maag for fully funding the purchase of a LP Mini for developing this feature! Stay tuned!
  * Includes Behringer CMD Touch TC64 in Novation compatability mode
* Make script being edited highlighted
* Fix wierd bug where GOTO and DELAY didn't obey a kill command (caught on video)
* Add script status icons (bound, playing, queued)
* Let program function as a layout editor without LP connection
* Add syntax highlighting
* Add GUI scaling
* Support for Launchpad Pro
  * The lack of tactile feedback, inability to utilize the pressure sensitive inputs (launchpad.py limitation), and inconvenient function keys where the hand rests makes support for the LP Pro a lower priority.
* Add generalized macro recorder wizard
* Make `Add Command...` menu that acts as a guided helper for making commands
* Add mouse event capture prompts to `Add Command...` menu boxes
* Add keyboard event capture (incl. unknown keycodes) to `Add Commands...` menu boxes
* Add `CMD` command to run OS commands
  * Make multi-level scary warning dialog boxes when binding to a button (incl during load layout)
  * Give option (and strongly reccomend its use) for users to run command once and verify it does what they want before binding to button (incl during load layout)
* Add `@LOAD_LAYOUT` header command to load a specified layout
  * Check if layout currently exists when binding to a button (incl during load layout)
    * If not, prompt user if they want to continue anyway
* MIDI output command? (Low priority)
* Load layout header?

## What have you done so far?
* ~~Support for Launchpad MkII~~
* ~~Events system~~
* ~~Colors system~~
* ~~LPHKScript base iteration~~
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
* ~~Add `LABEL` command~~
* ~~Add `IF_PRESSED_GOTO_LABEL` command to jump from this line to a `LABEL` if the key is still pressed~~
* ~~Add `GOTO_LABEL` command~~
* ~~Add `IF_UNPRESSED_GOTO_LABEL` command to jump from this line to a `LABEL` if the key is unpressed~~
* ~~Add `REPEAT_LABEL` command to jump from this line to a `LABEL` n number of times max~~
* ~~Add `IF_PRESSED_REPEAT_LABEL` command to jump from this line to a `LABEL` if the key is still pressed n number of times max~~
* ~~Add `IF_UNPRESSED_REPEAT_LABEL` command to jump from this line to a `LABEL` if the key is unpressed n number of times max~~
* ~~Add `M_STORE`, `M_RECALL`, and `M_RECALL_LINE` functions to remember where the mouse was before execution~~
* ~~Fix syntax checking being done in `main_logic()` instead of the, you know, syntax checker?~~
* ~~Merge `SP_` functions into smart versions of their single-character counterparts~~
* ~~Add feature to syntax checking for SOUND to check if file exists/is usable~~
* ~~Do syntax checks on loading a layout~~
* ~~Add `@SIMPLE` header for simple keybinding of single keyboard keys~~
* ~~Merge `M_TAP`, `M_PRESS`, and `M_RELEASE` commands into their keyboard counterparts~~
* ~~Add button move/swap/copy feature~~
* ~~Fix button highlighting clipping at screen edges~~
* ~~Add warning prompts to move/copy~~
* ~~Add "Do you want to save your layout?" popup on exit if layout is unsaved.~~
* ~~Add save layout if changed prompt to load/new layout~~
* ~~Do not prompt to save blank layout~~
* ~~Do not warn about moving/copying to the same button~~