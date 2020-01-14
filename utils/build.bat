@echo off

set ORIGDIR="%CD%"
set SCRIPTDIR=%~dp0
set LPHKDIR=%SCRIPTDIR%\..
set ICONDIR=%LPHKDIR%\resources
set ICON=%ICONDIR%\LPHK.ico

echo Building LIST_PADS...
call conda run -n LPHK-build pyinstaller ^
    --noconfirm ^
    --onefile ^
    --icon=%ICON% ^
    LIST_PADS.py
echo Built LIST_PADS!

echo Building RAW_CONNECT...
call conda run -n LPHK-build pyinstaller ^
    --noconfirm ^
    --onefile ^
    --icon=%ICON% ^
    RAW_CONNECT.py
echo Built RAW_CONNECT!

echo Building GET_KEYCODES...
call conda run -n LPHK-build pyinstaller ^
    --noconfirm ^
    --onefile ^
    --icon=%ICON% ^
    GET_KEYCODES.py
echo Built GET_KEYCODES!

pause