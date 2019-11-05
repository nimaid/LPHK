REM @echo off

REM This is a beta installer script that is the first step
REM in making the installation process painless. All you have
REM to do is install MiniConda 3 (or Anaconda 3).
REM After installing that, run this. A shortcut should be
REM created for LPHK in the main LPHK folder! Just copy that
REM wherever you want, but don't move the LPHK folder, or it
REM will break the shortcut.

REM Please let me know if this does or does not work in the Discord!

set "LPHKENV="
set "LPHKPYTHON="
set "STARTPATH="
set "MAINDIR="
set "LPHKSCRIPT="
set "LINKPATH="
set "LPHKICON="
set "SHORTCUTSCRIPT="

where conda >nul 2>nul
if %ERRORLEVEL% EQU 0 goto CONDADONE

:NOCONDA
set "AREYOUSURE="
set /P AREYOUSURE=No conda found. Install Miniconda3? (Y/[N]) 
if /I "%AREYOUSURE%" EQU "Y" goto INSTALLCONDA
goto NOINSTALLCONDA

:INSTALLCONDA
reg Query "HKLM\Hardware\Description\System\CentralProcessor\0" | find /i "x86" > NUL && set OS=32BIT || set OS=64BIT
if %OS%==32BIT set MCLINK=https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86.exe
if %OS%==64BIT set MCLINK=https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe

set CONDAEXE="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%-condainstall.exe"

echo Downloading Miniconda3...
powershell -Command "(New-Object Net.WebClient).DownloadFile('%MCLINK%', '%CONDAEXE%')"

if not errorlevel 1 echo Installing Miniconda3...
if not errorlevel 1 start /wait %CONDAEXE% /InstallationType=JustMe /S /D=%USERPROFILE%\Miniconda3

if not errorlevel 1 echo Miniconda3 has been installed...
if not errorlevel 1 echo Please re-run this installer in order to install LPHK!
del %CONDAEXE%
goto END

:CONDADONE
FOR /F "tokens=*" %%g IN ('conda env list ^| findstr /R /C:"LPHK"') do (set LPHKENV=%%g)
if defined LPHKENV goto ALREADYINSTALLED

set "AREYOUSURE="
set /P AREYOUSURE=Install LPHK? (Y/[N]) 
if /I "%AREYOUSURE%" EQU "Y" goto INSTALLLPHK
goto NOINSTALLLPHK

:INSTALLLPHK
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

if not errorlevel 1 goto DESKTOPLINKMAKE
goto END

:ALREADYINSTALLED
echo LPHK is already installed!
set "AREYOUSURE="
set /P AREYOUSURE=Uninstall LPHK? (Y/[N]) 
if /I "%AREYOUSURE%" EQU "Y" goto UNINSTALLLPHK
goto NOUNINSTALLLPHK

:UNINSTALLLPHK
echo Uninstalling LPHK...
call conda env remove -n LPHK

if not errorlevel 1 echo LPHK conda environment unistalled.
if not errorlevel 1 echo Please manually delete shortcuts, program files, and if desired, uninstall Miniconda3.
if not errorlevel 1 echo Run this installer again ro re-install.
goto END

:NOUNINSTALLLPHK
echo Not uninstalling LPHK, exiting...
goto END

:NOINSTALLLPHK
echo Not installing LPHK, exiting...
goto END

:NOINSTALLCONDA
echo Not installing MiniConda3, exiting...
goto END

:NOINSTALLCONDA
echo Not installing LPHK, exiting...
goto END

:DESKTOPLINKMAKE
echo Installation done! Shortcut created at %LINKPATH%

set "AREYOUSURE="
set /P AREYOUSURE=Install desktop shortcut? (Y/[N]) 
if /I "%AREYOUSURE%" EQU "Y" goto INSTALLSHORTCUT
goto END

:INSTALLSHORTCUT
set DESKTOPLINK=%USERPROFILE%\Desktop\
copy "%LINKPATH%" "%DESKTOPLINK%"
if not errorlevel 1 echo Copied shortcut to Desktop.
goto END

:END
echo LPHK installer is done running.
pause