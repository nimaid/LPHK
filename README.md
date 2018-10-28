# LPHK
A hotkey mapper for the Novation Launchpad

## What does it do?
The goal of this project is to implement a keyboard and mouse macro binding system for the Novation Launchpad.
It uses "LPScript", a very simple scripting language similar to DuckyScript, and will have a GUI to enter scripts, set colors, and to save/load your setup.

## Why would you do that?
Because it could be very useful for editing, gaming, programming, and even program launchers.

## Does it work yet?
Sort of! You can bind simple script strings to buttons, with colors, and the scheduling/events system is all done. Now the GUI and extention on the scripting language are the primary concerns. See below for a todo list. I have a life (a crazy one at that), so no promises on a delivery date. Feel free to offer your help!

## How do I use it?
Plug your Launchpad MkII (for now, Pro and others are coming) in, then run LPHK.py with Python 3, either through IDLE or "python3 LPHK.py".
Open a web browser and click on the web bar. Press a button and text will be eneterd. See scripts.py and LPHK.py for details on using LPScript and binding to a button. Still in development, so no real docs yet.

## What still needs to be written?
### Global
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
