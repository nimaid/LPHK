@echo off

REM DO NOT USE THIS SCRIPT. It is for creating new releases.

set ORIGDIR="%CD%"

del /f /s /q "%~dp0\..\..\__setup__" 1>nul 2>&1
rmdir /s /q "%~dp0\..\..\__setup__" 1>nul 2>&1

del /f /s /q "%~dp0\..\..\dist" 1>nul 2>&1
rmdir /s /q "%~dp0\..\..\dist" 1>nul 2>&1

del /f /s /q "%~dp0\..\..\build" 1>nul 2>&1
rmdir /s /q "%~dp0\..\..\build" 1>nul 2>&1

call "%~dp0\install_conda_windows.bat"
if errorlevel 1 goto ERROR

call "%~dp0\install_build_env.bat"
if errorlevel 1 goto ERROR

call "%~dp0\build_pyinstall.bat"
if errorlevel 1 goto ERROR

call "%~dp0\build_setup.bat"
if errorlevel 1 goto ERROR

goto DONE


:ERROR
echo Create release failed!
exit /B 1

:DONE
echo Create release done!
exit /B 0