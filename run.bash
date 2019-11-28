#!/bin/bash -i
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
conda activate LPHK
python $DIR/LPHK.py
conda deactivate
