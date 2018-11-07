First, download the lastest release of Python 3.x from https://www.python.org/. Run it, make a note of the default install location.

I suggest checking the option "Add Python 3.x to PATH", as it lets you easily use Python from the command line.

If performing a "Custom Installation" of Python 3, ensure "pip" and "tcl/tk and IDLE" are selected for install, at minimum.

Run "install_dependencies.bat" to install required libraries via pip.

After installing all dependencies, right click on LPHK.py and select "Open with", then "Look for another app on this PC". Browse to that install location you noted earlier and select "python.exe". At this point, you should be able to use whatever functionality the program currently has.

If you have errors, run the script in the command line by running "python3 LPHK.py" in the LPHK directory. (If this fails, use "python LPHK.py".) Please open an issue on GitHub and copy the output when trying and failing to run via command prompt.