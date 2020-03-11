#!/bin/bash -i
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
conda activate LPHK
# https://ubuntuforums.org/showthread.php?t=2290602
xhost +
python $DIR/LPHK.py
conda deactivate
