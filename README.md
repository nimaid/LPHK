# LPHK (LaunchPad HotKey)
A Novation Launchpad macro scripting system.

<a href="https://github.com/nimaid/LPHK"><img src="https://raw.githubusercontent.com/nimaid/LPHK/master/README_FILES/LPHK.png" alt="logo" height="300px" hspace="5"/></a><a href="https://discord.gg/mDCzB8X"><img src="https://raw.githubusercontent.com/nimaid/LPHK/master/README_FILES/discord.png" alt="logo" height="300px" hspace="5"/></a><a href="https://www.patreon.com/user?u=16848673"><img src="https://raw.githubusercontent.com/nimaid/LPHK/master/README_FILES/patreon.png" alt="logo" height="300px" hspace="5"/></a>
<img src="https://raw.githubusercontent.com/nimaid/LPHK/master/README_FILES/LPHK_update_3.png" alt="Update 3" width="800px" />

## Table of Contents
* [Links](https://github.com/nimaid/LPHK#links-table-of-contents)
* [What does it do?](https://github.com/nimaid/LPHK#what-does-it-do-table-of-contents)
* [Why would you do that?](https://github.com/nimaid/LPHK#why-would-you-do-that-table-of-contents)
* [Does it work yet?](https://github.com/nimaid/LPHK#does-it-work-yet-table-of-contents) (yes)
* [How do I get it? (Installation)](https://github.com/nimaid/LPHK#how-do-i-get-it-installation-table-of-contents)
  * [Windows Install/Run Instructions](https://github.com/nimaid/LPHK#windows-installrun-instructions-table-of-contents)
  * [Linux Install/Run Instructions](https://github.com/nimaid/LPHK#linux-installrun-instructions-table-of-contents)
* [How do I use it? (Post-Install)](https://github.com/nimaid/LPHK#how-do-i-use-it-post-install-table-of-contents)
* [What is LPHKscript?](https://github.com/nimaid/LPHK#what-is-lphkscript-table-of-contents)
  * [Scheduling](https://github.com/nimaid/LPHK#scheduling-table-of-contents)
  * [Headers](https://github.com/nimaid/LPHK#headers-table-of-contents)
  * [Comments](https://github.com/nimaid/LPHK#comments-table-of-contents)
  * [Commands List](https://github.com/nimaid/LPHK#commands-list-table-of-contents)
    * [Utility](https://github.com/nimaid/LPHK#utility-table-of-contents)
    * [Keypresses](https://github.com/nimaid/LPHK#keypresses-table-of-contents)
    * [Mouse Movement](https://github.com/nimaid/LPHK#mouse-movement-table-of-contents)
  * [Key Names](https://github.com/nimaid/LPHK#key-names-table-of-contents)
* [Known Issues / Troubleshooting](https://github.com/nimaid/LPHK#known-issues--troubleshooting-table-of-contents)
* [What still needs to be written? (in order of priority)](https://github.com/nimaid/LPHK#what-still-needs-to-be-written-in-order-of-priority-table-of-contents)
* [What have you done so far?](https://github.com/nimaid/LPHK#what-have-you-done-so-far-table-of-contents)

## Links [[Table of Contents]](https://github.com/nimaid/LPHK#table-of-contents)
* [Video Tutorial, Updates, and Plans](https://www.youtube.com/watch?v=XdJutWBEAqI)
* [First Look](https://www.youtube.com/watch?v=zZPt_lknhks)
* [Scheduling System](https://www.youtube.com/watch?v=rv2YmPQvMr0&t=164s)
* [Hackaday Early Writeup](https://hackaday.com/2018/11/04/launchpad-midi-controller-put-to-work-with-python/)
* [DOOM on a Launchpad](https://www.youtube.com/watch?v=4o_fh3n8FME)
* [Mouse Commands Demo - Maze](https://www.youtube.com/watch?v=w1YGSpT6aI8)
* [Medium.com Advanced Soundboard Writeup](https://medium.com/@lloydduhon/podcasting-tips-converting-a-novation-launchpad-to-a-soundboard-for-your-podcast-660962bbcf6c)

## What does it do? [[Table of Contents]](https://github.com/nimaid/LPHK#table-of-contents)
The goal of this project is to implement a macro scripting system for the Novation Launchpad, in order to use the launchpad as a scriptable, general purpose macro keyboard.

It uses "LPHKscript", a very simple scripting language similar to [DuckyScript](https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Duckyscript), and has a GUI to enter scripts, set colors, and to save/load your setup.

I have specifically chosen to do my best to develop this using as many cross platform libraries as possible, with a hard requirement that Linux and Windows be supported, and a strong preference for Mac as well. The GUI is driven by TK, which works on all of the above plus Unix. The interface with the launchpad and several script functions are built on pygame, which is compatable with basically everything ever. Pretty much everything else is standard Python 3.

## Why would you do that? [[Table of Contents]](https://github.com/nimaid/LPHK#table-of-contents)
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
  * Compiling/executing
  * Breakpoints
  * Debugger
* ... and many more!

## Does it work yet? [[Table of Contents]](https://github.com/nimaid/LPHK#table-of-contents)
Yes! It does not have all the features I want just yet, and still has bugs, but it works! You can use the GUI to load/save layouts and edit button scripts/colors. It's not nearly as polished as I want yet, but it is functional!

This is still WIP and still a beta version. See below for a todo list. I have a life (a crazy one at that), so no promises on a delivery date. Feel free to offer your help! You can see project updates and ask questions on the [official Discord server](https://discord.gg/mDCzB8X)! You can also donate on the [official Patreon page](https://www.patreon.com/user?u=16848673) to help speed up development, or just say thanks!

## How do I get it? (Installation) [[Table of Contents]](https://github.com/nimaid/LPHK#table-of-contents)
First, get a local copy of the GitHub repository. Click the green "Clone or download" button. The easiest path forward if you don't know what any of this this means is to then click "Download ZIP". Extract that .zip file, and you have a local copy of the repository!

Before using the program, we need to install some things:

### Windows Install/Run Instructions [[Table of Contents]](https://github.com/nimaid/LPHK#table-of-contents)
THE FOLLOWING INSTRUCTIONS ARE FOR THE BETA INSTALLER, WHICH AIMS TO BE PAINLESS TO USE. IF THIS FAILS, PLEASE SHARE IT ON THE DISCORD (OR AS A GITHUB ISSUE), AND IN THE MEANTIME TRY THE `LEGACY WINDOWS INSTALL INSTRUCTIONS`.

* Download the latest `.exe` setup file from https://github.com/nimaid/LPHK/releases/latest
* Run the `.exe` file and follow the on-screen setup instructions.
  * It is recommend to use the default install location
  * The setup wizard will install MiniConda3 if no conda is found
  * It will also create various shortcuts
* To run LPHK, use one of the shortcuts, either the `Start Menu` or `Desktop` one.
* You can uninstall LPHK like any other program, with the Windows `Add or remove programs` utility.
  * There will also be an uninstaller named `unins000.exe` in the program folder.

---- LEGACY WINDOWS INSTALL INSTRUCTIONS ----

ONLY USE IF THE ABOVE INSTALLER FAILS, AND AFTER SHARING THE ERROR ON DISCORD OR AS AN ISSUE.

* First, download the latest release of Python 3.x from https://www.python.org/.
* Install it, make a note of the default install location.
  * **YOU MUST** check the option "Add Python 3.x to PATH", as it lets Python and it's programs be used from the command line.
  * If performing a "Custom Installation" of Python 3, **YOU MUST** ensure "pip" and "tcl/tk and IDLE" are selected for install, at minimum.
* Run "install_dependencies.bat" to install required libraries via pip, which you just installed with Python 3.
* After installing all dependencies, right click on LPHK.py and select "Open with", then "Look for another app on this PC". Browse to that install location you noted earlier and select "python.exe".
  * At this point, you should be able to use whatever functionality the program currently has.
  * If you have errors (or nothing happens), run the script in the command line by running "python3 LPHK.py" in the LPHK directory. Please open an issue on GitHub and copy the output when trying and failing to run via command prompt.
    * (If this fails, use "python LPHK.py".)

### Linux Install/Run Instructions [[Table of Contents]](https://github.com/nimaid/LPHK#table-of-contents)
THE FOLLOWING INSTRUCTIONS ARE FOR THE BETA INSTALLER, WHICH AIMS TO BE PAINLESS TO USE. IF THIS FAILS, PLEASE SHARE IT ON THE DISCORD (OR AS A GITHUB ISSUE), AND IN THE MEANTIME TRY THE `LEGACY LINUX INSTALL INSTRUCTIONS`.

* Run `install_beta/install_linux.bash` via a `bash` shell (NOT `sh`, `fish`, etc.)
  * You can do this via terminal or, if it's set up, by double clicking it.
* One of three things will happen:
  * If LPHK is already installed, it will prompt if you would like to uninstall it. Type either `y` or `n` and press `enter`.
    * At the moment, this only uninstalls the conda environment. You still have to manually delete the LPHK files and shortcuts.
    * If Miniconda3 is installed in `~/miniconda3/`, it will prompt if you would like to uninstall that as well. Type either `y` or `n` and press `enter`.
  * If you do not have a conda distribution installed, it will prompt you if you want to install Miniconda3 and LPHK. Type `y` and press `enter`.
  * If a conda distribution is already installed, the installer will prompt you if you want to install LPHK. Type `y` and press `enter`.
* To run LPHK, use the command `[your lphk directory]/run.bash`.
  * `.desktop` shortcuts are coming soon!
  
---- LEGACY LINUX INSTALL INSTRUCTIONS ----

ONLY USE IF THE ABOVE INSTALLER FAILS, AND AFTER SHARING THE ERROR ON DISCORD OR AS AN ISSUE.

* Run `install_dependencies.bash`. If it fails, run with `sudo`.
* Many distros will let you double click on `LPHK.py` to run it. If yours doesn't, look up how to associate `.py` files with the `python3` binary on your distro.
  * At this point, you should be able to use whatever functionality the program currently has.
  * If you have errors (or nothing happens), run the script in the command line by running "python3 LPHK.py" in the LPHK directory. Please open an issue on GitHub and copy the output when trying and failing to run via command prompt.

## How do I use it? (Post-Install) [[Table of Contents]](https://github.com/nimaid/LPHK#table-of-contents)
* Before starting the program, make sure your Launchpad Classic/Mini/S or MkII is connected to the computer.
  * If you have a Launchpad Pro, there is currently beta support for it. Please put it in `Live` mode by following the instructions in the pop-up when trying to connect in the next step. For more info, see the [User Manual](https://d2xhy469pqj8rc.cloudfront.net/sites/default/files/novation/downloads/10581/launchpad-pro-gsg-en.pdf).
* Click `Launchpad > Connect to Launchpad...`.
  * If the connection is successful, the grid will appear, and the status bar at the bottom will turn green.
* The current mode is displayed in the upper right, in the gap between the circular buttons. Clicking this text will change the mode. There are four modes:
    * "Edit" mode: Click on a button to open the Script Edit window for that button.
      * All scripts are saved in the `.lpl` (LaunchPad Layout) files, but the editor also has the ability to import/export single `.lps` (LaunchPad Script) files.
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

#### The whole GUI is still rough around the edges, so don't be too surprised if something breaks. If it does, kindly open a detailed issue on GitHub so I can fix the error. :) And don't feel shy making feature requests, either!

## What is LPHKscript? [[Table of Contents]](https://github.com/nimaid/LPHK#table-of-contents)
LPHKscript is a simple macro scripting language tailor made for LPHK. Syntax is closer to a shell/batch script than, say, JavaScript.

### Scheduling [[Table of Contents]](https://github.com/nimaid/LPHK#table-of-contents)
Only one script runs at a time, and there is a scheduling system for them. If a script is scheduled, it's button will pulse red. If the script is running, the button will flash red quickly. This is true for the 8x8 grid, however, the function keys cannot flash or pulse, as a hardware limitation. These keys will be bright orange for scheduled and bright red for running.

When you press a script button, if there is a script running, it adds the script to the queue. If no scripts are running, the script is added to the queue and the queue execution is started. Tapping a scheduled script's button will unschedule it, and tapping a running scripts button will kill it. If that sounds confusing, load up `user_layouts/examples/all_delays_all_day.lpl` and press a bunch of buttons.

### Headers [[Table of Contents]](https://github.com/nimaid/LPHK#table-of-contents)
Headers are commands that start with `@` and go on the first line of a script. They are used to put the scripting engine into different "modes", allowing you to do some interesting things.

#### The `@ASYNC` Header [[Table of Contents]](https://github.com/nimaid/LPHK#table-of-contents)
There is one exception to the scheduling system. If the script has the `@ASYNC` header, it will run in the background and will not interact with the other scripts. It can still be prematurely killed by tapping the button. If this is used, it must be on the very first line.

#### The `@SIMPLE` Header [[Table of Contents]](https://github.com/nimaid/LPHK#table-of-contents)
This is a quick way to bind a controller button to a simple keypress of (argument 1). This has the equivalent code to:
```
@ASYNC
PRESS (argument 1)
WAIT_UNPRESSED
RELEASE (argument 1)
```
If this is used, all other lines in the file must either be whitespace or comments. In addition, it must be on the very first line.

### Comments [[Table of Contents]](https://github.com/nimaid/LPHK#table-of-contents)
Any line that starts with a dash `-` will be considered a comment, and will be ignored by the syntax validator/script parser. If a header is used, a comment cannot come before the header, as those must be on the first line, always.

### Commands List [[Table of Contents]](https://github.com/nimaid/LPHK#table-of-contents)
Commands follow the format: `COMMAND arg1 arg2 ...`. Scripts are just a text file with newlines separating commands.

#### Utility [[Table of Contents]](https://github.com/nimaid/LPHK#table-of-contents)
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
* `OPEN`
  * Opens the file or folder (argument 1).
* `REPEAT_LABEL`
  * Goto label (argument 1) a maximum of (argument 2) times.
* `RESET_REPEATS`
  * Reset the counter on all repeats. (no arguments)
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
  
#### Keypresses [[Table of Contents]](https://github.com/nimaid/LPHK#table-of-contents)
* `PRESS`
  * Presses the key (argument 1).
    * See valid key names below.
* `RELEASE`
  * Releases the key (argument 1).
    * See valid key names below.
* `RELEASE_ALL`
  * Releases all pressed keys, including those pressed by other scripts. (no arguments)
* `STRING`
  * Types whatever text comes after it.
* `TAP`
  * Taps the key (argument 1).
    * See valid key names below.
  * If (argument 2) supplied, tap (argument 2) number of times.
  * If (argument 3) supplied,  delay (argument 3) seconds before releasing each time.
  
#### Mouse Movement [[Table of Contents]](https://github.com/nimaid/LPHK#table-of-contents)
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
  * Sets the absolute cursor position to (argument 1) horizontal and (argument 2) vertical.
* `M_STORE`
  * Stores the current mouse position for use with the `M_RECALL*` commands.

### Key Names [[Table of Contents]](https://github.com/nimaid/LPHK#table-of-contents)
For the `PRESS`, `RELEASE`, and `TAP` commands, all single character non-whitespace keys and the following key names are allowed:
* `alt`
* `alt_gr`
* `backspace`
* `caps_lock`
* `cmd`
* `ctrl`
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

## Known Issues / Troubleshooting [[Table of Contents]](https://github.com/nimaid/LPHK#table-of-contents)
* The USB connection on the Launchpads, quite frankly, suck. If the angle is wrong, the Launchpad may receive power, but will not be able to transmit or receive data. While using the Launchpad, if you wiggle the connection somehow, it will straight up break the MIDI library I use. You will have to do the following:
  * Click on "Launchpad > Disconnect from Launchpad xxx..."
  * Unplug your Launchpad and wait about 5 seconds for the capacitors inside the Launchpad to drain. (It stays powered for a few seconds after losing it's connection, we want it dead as a doorknob)
  * Connect the Launchpad via USB
    * If you see the rainbow wipe effect and are left with no lights on, the connection is good
    * If the pad has psychedelic waves of colors exploding everywhere, it is getting power but cannot transmit or receive data. Try again, maybe with a different cable
    * If it does not light up at all, try again with a different cable or USB port
  * Click on "Launchpad > Redetect...". This will kill the program and restart it. This resets the MIDI library
  * If this does not fix the problem, or if the LP can connect and light up, but not receive input:
    * Try a different cable
    * Try a different USB port
    * Unplug and restart the program manually
    * Maybe restart your computer?
    * At this point IDK, maybe the USB on your Launchpad needs to be replaced.
* If your game/application does not detect mouse movements, see if there is an option to turn off "raw input" in the settings. This setting bypasses all software and reads directly from the mouse, which you don't want for this.

## What still needs to be written? (in order of priority) [[Table of Contents]](https://github.com/nimaid/LPHK#table-of-contents)
* Let program function as a layout editor without LP connection
  * Would probably be easier to write a "Dummy LP" class
* Make an installer for Windows and Linux
  * ~~Should use a `conda` environment created from an `environment.yml` file~~
  * Should copy LPHK files into an appropriate directory (like `Program Files`)
  * ~~Should give options to add various shortcuts~~ (Linux stull TODO)
* Add auto-update feature using `git`
  * ~~There will be a VERSION file in the main directory with the version string~~
    * This can be polled at `https://raw.githubusercontent.com/nimaid/LPHK/master/VERSION`
      * For example: `wget -qO- https://raw.githubusercontent.com/nimaid/LPHK/master/VERSION`
  * This will be displayed in the `Help > About LPHK` dialog.
  * If this string does not match the newest one at the above link, prompt to update
* Make `PRESS`, `RELEASE`, `TAP`, and `@SIMPLE` accept multiple keys
  * Will accept multiple arguemnts seperated by spaces
  * Will be pressed in the order `arg1`, `arg2`... and unpress in the order ...`arg2`, `arg1`
* Add `@LOAD_LAYOUT` header command to load a specified layout
  * Check if layout currently exists when binding to a button (incl during load layout)
    * If not, prompt user if they want to continue anyway
* Add startup config file
  * Default layout specification
  * Auto connect setting
  * Force launchpad model setting
  * Option to minimize to system tray
* Add settings menu to configure the startup config
* Add more color customization
    * Make new fields in the `.lpl` layout format
      * Add `run_color` to set the "running" color
        * Default is red (255, 0, 0)
      * Add `schedule_color` to set the "scheduled" color
        * Default is red (255, 0, 0)
      * Add `run_color_mode` to set the "running" color mode
        * `flash` is a quick blinking (default)
        * `pulse` is a slow fade in and fade out
        * `solid` is coninuously on
      * Add `schedule_color_mode` to set the "scheduled" color mode
        * `pulse` is a slow fade in and fade out (default)
        * `flash` is a quick blinking
        * `solid` is coninuously on
    * Add more selectors to script entry window
* Add a `Sound` menu with `Choose default output device...` option
* Add more sound commands
  * Use different sound library that supports playing an arbitrary number of sounds, and controlling each sound individually while it plays
  * Add optional label argument to `SOUND`
  * Add `SOUND_VOLUME` to set the sound volume by label
  * Add `SOUND_STOP` to stop playing sound by label and delete the sound label
  * Add `SOUND_ALL_*` commands to stop/change the volume of all sounds
* [Refactor code to make LPHKscript functions in auto-implementing modules, for ease of delevopment](https://github.com/nimaid/LPHK/issues/3)
  * A new testing branch will be created while the functional code is re-worked. To avoid merging issues, pull requests may have acceptance delayed until the refactor is complete.
  * There are a few complex refactoring tasks required for this, I will be crossing them off here on the testing branch:
    * ~~Make a killable delay/time library that monitors thread kill flags~~
    * ~~Port keyboard functions over to LPHKfunction modules~~
    * Make `commands.py` module to house the actual command logic
    * Move `@SIMPLE` to keyboard module.
      * Allow F['COMMAND']['macro'] = True to disallow other non-comment lines in the script. Default is False.
        * Macros will automatically have `_` added to the beginning (`@` will only be for headers)
        * `validate_script()` will take care of making sure macros are alone (after comment/nl stripping)
      * Allow F['COMMAND']['macro_async'] = True to enable async on a macro. Default is False, ignored if not a macro.
        * When importing functions on startup, make a dict to keep track of what macros are async
        * `scripts.py` will have a `run_async` dict to keep track of if a script is async
        * (Comments/nl stripped) During scheduling of the script, if first line is `@ASYNC` or is an async macro (1 functional line), then run_async[x][y] is set, otherwise unset
    * Write the importer library (test standalone w/ simple delay)
    * ~~Lobotomize the program (read: remove the hellish logic in scripts.py)~~
    * Integrate the importer into the main program (scripts.py)
    * Find and kill all of the bugs
    * Port the rest of the old logic to LPHKfuction modules
    * Deal with the Pandora's box that porting those functions will open (this list will probably grow)
    * Make a way for modules to use standard commands, and to use other modules
    * Take a drink and merge the branches
* Allow named arguments for certain commands
* Simply strip comments and empty lines before sending to logic, that way, first line can be a comment and second a header.
* Let `SOUND` use spaces in it's path if it has double quotes around it
* Add a `Choose default MIDI device` option to the `Sound` menu. (For multiple launchpads plugged in)
* Add a third argument to `SOUND` for overriding the default sound device
* Add variables and mathematical evaluation (mostly done!)
* Add conditional jumps based on value comparisons (Would this make LPHKscript Turing complete? :D) 
* Add script status icons (bound, playing, queued)
* Add syntax highlighting
* Add GUI scaling
* Full support for Launchpad Pro
  * The lack of tactile feedback, inability to utilize the pressure sensitive inputs (launchpad.py limitation), and inconvenient function keys where the hand rests makes support for the LP Pro a lower priority.
* Add generalized macro recorder wizard
* Make `Add Command...` menu that acts as a guided helper for making commands
* Add mouse event capture prompts to `Add Command...` menu boxes
* Add keyboard event capture (incl. unknown keycodes) to `Add Commands...` menu boxes
* Add `CMD` command to run OS commands
  * Make multi-level scary warning dialog boxes when binding to a button (incl during load layout)
  * Give option (and strongly recommend its use) for users to run command once and verify it does what they want before binding to button (incl during load layout)
* MIDI output command? (Low priority)
* Load layout header?

## What have you done so far? [[Table of Contents]](https://github.com/nimaid/LPHK#table-of-contents)
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
* ~~Make script being edited highlighted~~
* ~~Fix weird bug where GOTO and DELAY didn't obey a kill command (caught on video)~~
* ~~Add `OPEN` command to open folders and files~~
* ~~Add `RELEASE_ALL` command~~
* ~~Add `RESET_REPEATS` command to reset the counter on all repeats~~
* ~~Basic support for Launchpad Classic/S/Mini~~
  * Thanks to Patreon patron Korbinian Maag for fully funding the purchase of a LP Mini for developing this feature!
  * Includes Behringer CMD Touch TC64 in Novation compatibility mode
* ~~Add partial Pro support (left and bottom rows not enabled)~~
  * A huge shoutout to MiniStumpy Bloopers in the Discord, who was able to find out that adding this feature was actually fairly simple! I really need a Pro to develop with.
* ~~Make a special color picker for Classic/Mini/S that only has the 16 possible colors~~
* ~~Re-write `files.py` to use a JSON format for layouts.~~