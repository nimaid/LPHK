REM This is a beta installer script that is the first step
REM in making the installation process painless. All you have
REM to do is install MiniConda 3 (or Anaconda 3).
REM See https://docs.conda.io/en/latest/miniconda.html
REM After installing that, run this. A shortcut should be
REM created for LPHK in the main LPHK folder! Just copy that
REM wherever you want, but don't move the LPHK folder, or it
REM will break the shortcut.

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

if not errorlevel 1 call conda activate LPHK
if not errorlevel 1 FOR /F "tokens=*" %%g IN ('where python ^| findstr /R /C:"LPHK"') do (set LPHKPYTHON=%%g)
if not errorlevel 1 call conda deactivate

if not errorlevel 1 set STARTPATH=%CD%
if not errorlevel 1 cd %~dp0\..
if not errorlevel 1 set MAINDIR=%CD%
if not errorlevel 1 cd %STARTPATH%

if not errorlevel 1 set LPHKSCRIPT=%MAINDIR%\LPHK.py

if not errorlevel 1 set LINKPATH=%MAINDIR%\LPHK.lnk
if not errorlevel 1 set LPHKICON=%MAINDIR%\resources\LPHK.ico

if not errorlevel 1 set SHORTCUTSCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
if not errorlevel 1 echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SHORTCUTSCRIPT%
if not errorlevel 1 echo sLinkFile = "%LINKPATH%" >> %SHORTCUTSCRIPT%
if not errorlevel 1 echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SHORTCUTSCRIPT%
if not errorlevel 1 echo oLink.TargetPath = "%LPHKPYTHON%" >> %SHORTCUTSCRIPT%
if not errorlevel 1 echo oLink.Arguments = "%LPHKSCRIPT%" >> %SHORTCUTSCRIPT%
if not errorlevel 1 echo oLink.IconLocation = "%LPHKICON%" >> %SHORTCUTSCRIPT%
if not errorlevel 1 echo oLink.Save >> %SHORTCUTSCRIPT%
if not errorlevel 1 call cscript /nologo %SHORTCUTSCRIPT%
if not errorlevel 1 del %SHORTCUTSCRIPT%

echo Installation done! Shortcut created at %LINKPATH%
goto END

:NOCONDA
echo Please install either Anaconda or MiniConda before attempting to install LPHK.
goto END

:ALREADYINSTALLED
echo LPHK is already installed!
goto END

:END
pause