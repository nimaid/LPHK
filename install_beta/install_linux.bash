#!/bin/bash

CONDAEXE=
CONDAPATH=
CONDA=
DOINSTALLCONDA=
DOINSTALLLPHK=
DOUNINSTALLLPHK=

SCRIPTDIR=$(dirname $0)
CONDAENVDIR=~/.conda/envs

function pause () {
	read -rsp $'Press any key to continue...\n' -n1 key
}

function prompt_yn () {
	read -p "Do you wish to continue? (Y/[N])" -n 1 -r
    echo 
	if [[ $REPLY =~ ^[Yy]$ ]]; then
		return 1
	else
		return 0
	fi
}



function install_conda () {
	CONDAEXE=/tmp/$RANDOM-$RANDOM-$RANDOM-$RANDOM-condainstall.sh
	CONDAPATH=~/miniconda3

	if [ $(uname -m) == 'x86_64' ]; then wget 'https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh' -O $CONDAEXE; else wget 'https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86.sh' -O $CONDAEXE; fi
	sudo chmod +x $CONDAEXE
	sudo $CONDAEXE -b -p $CONDAPATH
	sudo rm $CONDAEXE

	CONDA=$CONDAPATH/bin/conda

	$CONDA init
	source ~/.bashrc

	conda config --set auto_activate_base False
}

function uninstall_conda () {
	sed -i '/^# >>> conda initialize >>>/,/^# <<< conda initialize <<</d;' ~/.bashrc
	sudo rm -rf ~/.conda*/ ~/miniconda3/
	sudo rm -f ~/.conda* 
	source ~/.bashrc
}

function install_LPHK () {
	conda env create -f $SCRIPTDIR/environment.yml
}

function uninstall_LPHK () {
	conda env remove -n LPHK
	sudo rm -rf $CONDAENVDIR/LPHK/
}



conda > /dev/null 2>1 && CONDAGOOD=1 || CONDAGOOD=0

if [ $CONDAGOOD = 0 ]; then
	echo "No conda found. Install Miniconda3?"
	prompt_yn
	DOINSTALLCONDA=$?
	if [ $DOINSTALLCONDA = 1 ]; then
		echo "Installing Miniconda3..."
		install_conda
		echo "Miniconda3 has been installed!"
	else
		echo "Not installing Miniconda3, exiting..."
		pause
		exit	
	fi
fi


if [ -d "$CONDAENVDIR/LPHK" ]; then
	echo "LPHK already installed! Uninstall LPHK?"
	prompt_yn
	DOUNINSTALLLPHK=$?
	if [ $DOUNINSTALLLPHK = 1 ]; then
		echo "Uninstalling LPHK..."
		uninstall_LPHK
		echo "LPHK uninstalled!"
	else
		echo "Not uninstalling LPHK, exiting..."
		exit
	fi

else
	echo "Install LPHK?"
	prompt_yn
	DOINSTALLLPHK=$?
	if [ $DOINSTALLLPHK = 1 ]; then
		echo "Installing LPHK..."
		install_LPHK
		echo "LPHK environment set up. Run 'conda activate LPHK', then 'python LPHK.py'"
	else
		echo "Not installing LPHK, exiting..."
		exit
	fi
fi

