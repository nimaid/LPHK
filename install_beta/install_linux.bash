#!/bin/bash

CONDAEXE=
CONDAPATH=
CONDA=
DOINSTALLCONDA=0
DOINSTALLLPHK=0
DOUNINSTALLLPHK=0
DOUNINSTALLCONDA=0

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

function exit_if_error () {
	if [ ! $? = 0 ]; then
		echo "An error has occured! Exiting..."
		pause
		exit 1
	fi
}



function install_conda () {
	CONDAEXE=/tmp/$RANDOM-$RANDOM-$RANDOM-$RANDOM-condainstall.sh
	CONDAPATH=~/miniconda3

	if [ $(uname -m) == 'x86_64' ]; then
		wget 'https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh' -O $CONDAEXE
    else
        wget 'https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86.sh' -O $CONDAEXE
    fi; exit_if_error

	sudo chmod +x $CONDAEXE; exit_if_error
	sudo $CONDAEXE -b -p $CONDAPATH; exit_if_error
	sudo rm $CONDAEXE

	CONDA=$CONDAPATH/bin/conda

	$CONDA init; exit_if_error
	source ~/.bashrc; exit_if_error

	conda config --set auto_activate_base False
}

function uninstall_conda () {
	sed -i '/^# >>> conda initialize >>>/,/^# <<< conda initialize <<</d;' ~/.bashrc
	sudo rm -rf ~/.conda*/ ~/miniconda3/
	sudo rm -f ~/.conda* 
	source ~/.bashrc
}

function install_LPHK () {
	conda env create -f $SCRIPTDIR/environment.yml; exit_if_error
}

function uninstall_LPHK () {
	conda env remove -n LPHK; exit_if_error
	sudo rm -rf $CONDAENVDIR/LPHK/
}


function help_message () {
	echo "Usage: install_linux.bash [-t]"
	echo "-t | Total uninstall (Miniconda3 + LPHK)"
}



# If conda isn't found, prompt to install it as well
conda > /dev/null 2>1 && CONDAGOOD=1 || CONDAGOOD=0
if [ $CONDAGOOD = 0 ]; then
	echo "No conda found. Install Miniconda3 and LPHK?"
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

# If LPHK is already installed, offer to uninstall
if [ -d "$CONDAENVDIR/LPHK" ]; then
	echo "LPHK already installed! Uninstall LPHK?"
	prompt_yn
	DOUNINSTALLLPHK=$?
	if [ $DOUNINSTALLLPHK = 1 ]; then
		echo "Uninstall Miniconda3 as well? (THIS WILL DELETE YOUR ENVIRONMENTS)"
		prompt_yn
		DOUNINSTALLCONDA=$?
		
		echo "Uninstalling LPHK..."
		uninstall_LPHK
		echo "LPHK uninstalled!"

		if [ $DOUNINSTALLCONDA = 1 ]; then
			echo "Uninstalling Miniconda3..."
			uninstall_conda
			echo "Miniconda3 uninstalled!"
		fi

		pause
		exit
	else
		echo "Not uninstalling LPHK, exiting..."
		pause
		exit
	fi
# If LPHK is not installed, offer to install
else
	if [ $DOINSTALLCONDA = 1 ]; then
		DOINSTALLLPHK=1
	else
		echo "Install LPHK?"
		prompt_yn
		DOINSTALLLPHK=$?
	fi
	if [ $DOINSTALLLPHK = 1 ]; then
		echo "Installing LPHK..."
		install_LPHK
		echo "LPHK environment set up. Run 'conda activate LPHK', then 'python LPHK.py'"
	else
		echo "Not installing LPHK, exiting..."
		pause
		exit
	fi
fi

