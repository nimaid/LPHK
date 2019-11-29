@echo off

REM DO NOT USE THIS SCRIPT. It is for creating new releases.

set ORIGDIR="%CD%"

echo Cleaning up before starting...
del /f /s /q "%~dp0\..\..\__release__" 1>nul 2>&1
rmdir /s /q "%~dp0\..\..\__release__" 1>nul 2>&1

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

echo Moving setup to release...
rename "%~dp0\..\..\__setup__" "__release__" 1>nul 2>&1
if errorlevel 1 goto ERROR

echo Moving needed portable files to dist...
mkdir "%~dp0\..\..\dist\user_layouts" 1>nul 2>&1
xcopy /s "%~dp0\..\..\user_layouts" "%~dp0\..\..\dist\user_layouts" 1>nul 2>&1

mkdir "%~dp0\..\..\dist\user_scripts" 1>nul 2>&1
xcopy /s "%~dp0\..\..\user_scripts" "%~dp0\..\..\dist\user_scripts" 1>nul 2>&1

mkdir "%~dp0\..\..\dist\user_sounds" 1>nul 2>&1
xcopy /s "%~dp0\..\..\user_sounds" "%~dp0\..\..\dist\user_sounds" 1>nul 2>&1
if errorlevel 1 goto ERROR

echo Zipping portable version...
powershell -Command Compress-Archive "%~dp0\..\..\dist" "%~dp0\..\..\__release__\NAME.zip" 1>nul 2>&1
if errorlevel 1 goto ERROR

echo Cleaning up...
del /f /s /q "%~dp0\..\..\dist" 1>nul 2>&1
rmdir /s /q "%~dp0\..\..\dist" 1>nul 2>&1

del /f /s /q "%~dp0\..\..\build" 1>nul 2>&1
rmdir /s /q "%~dp0\..\..\build" 1>nul 2>&1
if errorlevel 1 goto ERROR

goto DONE


:ERROR
echo Create release failed!
exit /B 1

:DONE
echo Create release done!
exit /B 0