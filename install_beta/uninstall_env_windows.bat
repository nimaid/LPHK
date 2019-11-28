@echo off

REM DO NOT USE THIS SCRIPT. It is for the new Inno Setup installer.

set "LPHKENV="

REM TODO: Use environments.txt
FOR /F "tokens=*" %%g IN ('conda env list ^| findstr /R /C:"LPHK"') do (set LPHKENV="%%g")
if defined LPHKENV goto UNINSTALLENV
goto NOTINSTALLED

:UNINSTALLENV
echo Uninstalling LPHK Conda environment...
call conda env remove -n LPHK
REM TODO: Use environments.txt
rmdir %USERPROFILE%\Miniconda3\envs\LPHK /s /q 2> nul
if errorlevel 1 goto ERROREND

echo LPHK conda environment unistalled!
goto END

:NOTINSTALLED
echo The LPHK environment is not installed!
goto END

:ERROREND
echo The LPHK environment could not be uninstalled!
exit /B 1

:END
exit /B 0