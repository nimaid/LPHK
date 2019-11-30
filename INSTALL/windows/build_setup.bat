@echo off

REM DO NOT USE THIS SCRIPT. It is for creating new releases.

set ORIGDIR="%CD%"

set ISCC="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if exist %ISCC% goto BUILD
echo Inno Setup Studio 6 not found! (%ISCC%)
echo Download the latest installer at http://files.jrsoftware.org/is/6/
goto ERROR

:BUILD
echo Building Installer...
%ISCC% "%~dp0\windows.iss"
if errorlevel 1 goto ERROR

goto DONE


:ERROR
echo Installer build failed!
exit /B 1

:DONE
echo Installer build done!
exit /B 0