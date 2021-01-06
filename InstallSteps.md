1. Pyinstaller
   
Generates the executable

```shell
python -OO -m PyInstaller --add-data resources;resources --noconfirm --noconsole --icon resources/LPHK.ico LPH
K.py

```

2. Inno Setup

Generates the installer for the executatble.
See the existing .iss file. 
That needs to be run from Inno setup, 
which will generate the setup executable.

3. Run Setup

Run the generated .exe installer file
