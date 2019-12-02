@echo off

REM DO NOT USE THIS SCRIPT. It is for creating new releases.

set ORIGDIR="%CD%"

set "LPHKENV="
set "STARTPATH="

set "ENVNAME=LPHK-build"

where conda >nul 2>nul
if %ERRORLEVEL% NEQ 0 goto CONDAMISSING

:INSTALLENV
REM TODO: Use environments.txt
FOR /F "tokens=*" %%g IN ('conda env list ^| findstr /R /C:"%ENVNAME%"') do (set LPHKENV="%%g")
if defined LPHKENV goto ALREADYINSTALLED

echo Installing LPHK build environment...
set STARTPATH="%CD%"
cd "%~dp0"
call conda env create -f ../environment-build.yml
cd %ORIGDIR%
if errorlevel 1 goto INSTALLENVFAIL

cd %STARTPATH%
echo LPHK build environment installed!
goto END

:CONDAMISSING
echo Conda is not installed!
goto ERROREND

:INSTALLENVFAIL
REM TODO: Use environments.txt
rmdir %USERPROFILE%\Miniconda3\envs\%ENVNAME% /s /q 2> nul
goto ERROREND

:ALREADYINSTALLED
echo LPHK build environment is already installed!
goto END

:ERROREND
echo The LPHK build environment could not be installed!
exit /B 1

:END
exit /B 0
