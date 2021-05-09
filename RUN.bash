#!/bin/bash -i
conda activate LPHK
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
python $DIR/LPHK.py
conda deactivate
