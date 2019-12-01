#!/bin/bash

cd ../../

conda run -n LPHK-build pyinstaller --onedir --windowed --hidden-import='PIL._tkinter_finder' --add-data VERSION:. --add-data resources/:resources/ --icon=resources/LPHK.ico LPHK.py

