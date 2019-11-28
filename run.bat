@echo off
set STARTPATH="%CD%"
cd "%~dp0"
conda activate LPHK & python LPHK.py & conda deactivate
cd %STARTPATH%