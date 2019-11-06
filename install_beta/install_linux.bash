#!/bin/bash

CONDAEXE=/tmp/condainstall.sh
CONDAPATH=$HOME/miniconda3

if [ $(uname -m) == 'x86_64' ]; then wget 'https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh' -O $CONDAEXE; else wget 'https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86.sh' -O $CONDAEXE; fi
sudo chmod +x $CONDAEXE
sudo $CONDAEXE -b -p $CONDAPATH
sudo rm $CONDAEXE
CONDA=$CONDAPATH/bin/conda

$CONDA init
$CONDA config --set auto_activate_base False


