REM This is a beta installer script that is the first step
REM in making the installation process painless. All you have
REM to do is install MiniConda 3 (or Anaconda 3).
REM See https://docs.conda.io/en/latest/miniconda.html
REM After installing that, run this. A shortcut should be
REM created for LPHK in the main folder!

REM Please let me know if this does or does not work in the Discord!

@echo off

set "LPHKENV="
set "LPHKPYTHON="
set "STARTPATH="
set "MAINDIR="
set "LPHKSCRIPT="
set "LINKPATH="
set "LPHKICON="
set "SHORTCUTSCRIPT="

where conda >nul 2>nul
if %ERRORLEVEL% NEQ 0 goto NOCONDA


FOR /F "tokens=*" %%g IN ('conda env list ^| findstr /R /C:"LPHK"') do (set LPHKENV=%%g)
if defined LPHKENV goto ALREADYINSTALLED

echo Installing LPHK...
call conda env create -f %~dp0\environment.yml

call conda activate LPHK
FOR /F "tokens=*" %%g IN ('where python ^| findstr /R /C:"LPHK"') do (set LPHKPYTHON=%%g)
call conda deactivate

set STARTPATH=%CD%
cd %~dp0\..
set MAINDIR=%CD%
cd %STARTPATH%

set LPHKSCRIPT=%MAINDIR%\LPHK.py

set LINKPATH=%MAINDIR%\LPHK.lnk
set LPHKICON=%MAINDIR%\resources\LPHK.ico

set SHORTCUTSCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SHORTCUTSCRIPT%
echo sLinkFile = "%LINKPATH%" >> %SHORTCUTSCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SHORTCUTSCRIPT%
echo oLink.TargetPath = "%LPHKPYTHON%" >> %SHORTCUTSCRIPT%
echo oLink.Arguments = "%LPHKSCRIPT%" >> %SHORTCUTSCRIPT%
echo oLink.IconLocation = "%LPHKICON%" >> %SHORTCUTSCRIPT%
echo oLink.Save >> %SHORTCUTSCRIPT%
call cscript /nologo %SHORTCUTSCRIPT%
del %SHORTCUTSCRIPT%

echo Installation done! Shortcut created at %LINKPATH%
goto END

:NOCONDA
echo Please install either Anaconda or MiniConda before attempting to install LPHK.
goto END

:ALREADYINSTALLED
echo LPHK is already installed!
goto END

:END