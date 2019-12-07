@echo off

REM DO NOT USE THIS SCRIPT. It is for creating new releases.

set RELEASEDIRNAME=__release__

set ORIGDIR="%CD%"

set INSTALLWINDIR=%~dp0
set INSTALLDIR=%INSTALLWINDIR%\..
set LPHKDIR=%INSTALLDIR%\..

set RELEASEDIR=%LPHKDIR%\%RELEASEDIRNAME%
set SETUPDIR=%LPHKDIR%\__setup__
set DISTDIR=%LPHKDIR%\dist
set BUILDDIR=%LPHKDIR%\build

set /p VERSION=<"%LPHKDIR%\VERSION"
if [%VERSION%] == [] goto ERROR

set PORTABLENAME=LPHK_portable_win_%VERSION%
set PORTABLEDIR=%RELEASEDIR%\LPHK

set EXENAME=LPHK.exe


call cmd /c "%INSTALLWINDIR%\install_conda_windows.bat"
if errorlevel 1 goto ERROR


:CONDAFOUND
call cmd /c "%INSTALLWINDIR%\install_build_env.bat"
if errorlevel 1 goto ERROR

echo Cleaning up before making release...
del /f /s /q "%RELEASEDIR%" 1>nul 2>&1
rmdir /s /q "%RELEASEDIR%" 1>nul 2>&1

del /f /s /q "%SETUPDIR%" 1>nul 2>&1
rmdir /s /q "%SETUPDIR%" 1>nul 2>&1

del /f /s /q "%DISTDIR%" 1>nul 2>&1
rmdir /s /q "%DISTDIR%" 1>nul 2>&1

del /f /s /q "%BUILDDIR%" 1>nul 2>&1
rmdir /s /q "%BUILDDIR%" 1>nul 2>&1

echo Making release version %VERSION% now...
call cmd /c "%INSTALLWINDIR%\build_pyinstall_installed.bat"
if errorlevel 1 goto ERROR

call cmd /c "%INSTALLWINDIR%\build_setup.bat"
if errorlevel 1 goto ERROR

echo Moving setup to release...
rename "%SETUPDIR%" "%RELEASEDIRNAME%" 1>nul 2>&1
if errorlevel 1 goto ERROR

call cmd /c "%INSTALLWINDIR%\build_pyinstall_portable.bat"
if errorlevel 1 goto ERROR

echo Moving needed portable files to folder...
mkdir "%PORTABLEDIR%" 1>nul 2>&1
xcopy "%DISTDIR%\%EXENAME%" "%PORTABLEDIR%" 1>nul 2>&1
if not exist "%PORTABLEDIR%\%EXENAME%" goto ERROR

mkdir "%PORTABLEDIR%\user_layouts\examples" 1>nul 2>&1
xcopy /s "%LPHKDIR%\user_layouts\examples" "%PORTABLEDIR%\user_layouts\examples" 1>nul 2>&1
if not exist "%PORTABLEDIR%\user_layouts\examples" goto ERROR

mkdir "%PORTABLEDIR%\user_scripts\examples" 1>nul 2>&1
xcopy /s "%LPHKDIR%\user_scripts\examples" "%PORTABLEDIR%\user_scripts\examples" 1>nul 2>&1
if not exist "%PORTABLEDIR%\user_scripts\examples" goto ERROR

mkdir "%PORTABLEDIR%\user_sounds\examples" 1>nul 2>&1
xcopy /s "%LPHKDIR%\user_sounds\examples" "%PORTABLEDIR%\user_sounds\examples" 1>nul 2>&1
if not exist "%PORTABLEDIR%\user_sounds\examples" goto ERROR

if errorlevel 1 goto ERROR

echo Zipping portable version...
powershell -Command Compress-Archive "%PORTABLEDIR%" "%RELEASEDIR%\%PORTABLENAME%.zip"
if errorlevel 1 goto ERROR

echo Cleaning up...
del /f /s /q "%PORTABLEDIR%" 1>nul 2>&1
rmdir /s /q "%PORTABLEDIR%" 1>nul 2>&1

del /f /s /q "%DISTDIR%" 1>nul 2>&1
rmdir /s /q "%DISTDIR%" 1>nul 2>&1

del /f /s /q "%BUILDDIR%" 1>nul 2>&1
rmdir /s /q "%BUILDDIR%" 1>nul 2>&1
if errorlevel 1 goto ERROR

goto DONE


:ERROR
echo Create release failed!
exit /B 1

:DONE
echo Create release done!
exit /B 0