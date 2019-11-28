@echo off

REM DO NOT USE THIS SCRIPT. It is for the new Inno Setup installer.

set "LPHKENV="
set "STARTPATH="

where conda >nul 2>nul
if %ERRORLEVEL% NEQ 0 goto CONDAMISSING

:INSTALLENV
REM TODO: Use environments.txt
FOR /F "tokens=*" %%g IN ('conda env list ^| findstr /R /C:"LPHK"') do (set LPHKENV="%%g")
if defined LPHKENV goto ALREADYINSTALLED

echo Installing LPHK...
set STARTPATH="%CD%"
cd "%~dp0"
call conda env create -f environment.yml
if errorlevel 1 goto INSTALLENVFAIL

cd %STARTPATH%
goto END

:CONDAMISSING
echo "Conda is not installed!"
goto ERROREND

:INSTALLENVFAIL
call conda env remove -n LPHK
REM TODO: Use environments.txt
rmdir %USERPROFILE%\Miniconda3\envs\LPHK /s /q 2> nul
goto ERROREND

:ALREADYINSTALLED
echo LPHK is already installed!
goto END

:ERROREND
echo The LPHK environment could not be installed!
exit /B 1

:END
exit /B 0
