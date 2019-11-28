@echo off

start "LPHK Log (Do Not Close)" /min /D "%~dp0" cmd /c "conda activate LPHK & python -u LPHK.py & conda deactivate & exit"