#!/bin/bash -i

SCRIPTPATH=$(readlink -f "$0")
SCRIPTDIR=$(dirname "$SCRIPTPATH")
INSTALLDIR=$SCRIPTDIR/..
MAINDIR=$INSTALLDIR/..

ORIGDIR=$(pwd)

cd $MAINDIR

conda activate LPHK-build
pyinstaller --onedir --windowed --hidden-import='PIL._tkinter_finder' --add-data VERSION:. --add-data resources/:resources/ --icon=resources/LPHK.ico LPHK.py
conda deactivate 

cd $ORIGDIR
