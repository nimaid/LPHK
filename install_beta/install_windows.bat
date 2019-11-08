@echo off

REM This is a beta installer script that is the first step
REM in making the installation process painless. All you have
REM to do is run this. It will install Miniconda3 if you don't
REM have a conda installation, and will ask if you want to install LPHK.
REM A shortcut will be created for LPHK in the main LPHK folder.
REM It will also offer to create a desktop shortcut. Just don't move
REM the LPHK folder, or it will break the shortcut. If you wish to
REM uninstall, run this after LPHK is installed. You will have to
REM remove the shortcuts, and manually delete the files.

REM Please let me know if this does or does not work in the Discord!

set "LPHKENV="
set "LPHKPYTHON="
set "STARTPATH="
set "MAINDIR="
set "LPHKSCRIPT="
set "LINKPATH="
set "LPHKICON="
set "SHORTCUTSCRIPT="
set "MINICONDAPATH="
set "CONDAEXE="
set "OS="
set "MCLINK="
set "DESKTOPLINK="

set "CONDAWASINSTALLEDFLAG=\CONDAWASJUSTINSTALLED"

where conda >nul 2>nul
if %ERRORLEVEL% EQU 0 goto CONDADONE

:NOCONDA
set "AREYOUSURE="
set /P AREYOUSURE=No conda found. Install Miniconda3 and LPHK? (Y/[N]): 
if /I "%AREYOUSURE%" EQU "Y" goto INSTALLCONDA
goto NOINSTALLCONDA

:INSTALLCONDA
reg Query "HKLM\Hardware\Description\System\CentralProcessor\0" | find /i "x86" > NUL && set OS=32BIT || set OS=64BIT
if %OS%==32BIT set MCLINK=https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86.exe
if %OS%==64BIT set MCLINK=https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe

set CONDAEXE=%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%-condainstall.exe

echo Downloading Miniconda3 (This will take while, please wait)...
powershell -Command "(New-Object Net.WebClient).DownloadFile('%MCLINK%', '%CONDAEXE%')" > nul
if errorlevel 1 goto ERROREND

echo Installing Miniconda3...
set MINICONDAPATH=%USERPROFILE%\Miniconda3
start /wait /min %CONDAEXE% /InstallationType=JustMe /S /D=%MINICONDAPATH%
del %CONDAEXE%
if errorlevel 1 goto CONDAERROR
if not exist %MINICONDAPATH%\ (goto CONDAERROR)

%MINICONDAPATH%\Scripts\conda.exe init
if errorlevel 1 goto CONDAERROR

echo Miniconda3 has been installed...
timeout 5
start cmd /c "%0 %CONDAWASINSTALLEDFLAG%"
goto HARDEND

:CONDAERROR
echo Miniconda3 install failed!
goto ERROREND

:CONDADONE
REM TODO: Use environments.txt
FOR /F "tokens=*" %%g IN ('conda env list ^| findstr /R /C:"LPHK"') do (set LPHKENV=%%g)
if defined LPHKENV goto ALREADYINSTALLED

if "%1"=="%CONDAWASINSTALLEDFLAG%" goto CONDAWASINSTALLED
set "AREYOUSURE="
set /P AREYOUSURE=Install LPHK? (Y/[N]): 
if /I "%AREYOUSURE%" EQU "Y" goto INSTALLLPHK
goto NOINSTALLLPHK

:CONDAWASINSTALLED
echo Miniconda was previously installed successfully!
goto INSTALLLPHK

:INSTALLLPHK
echo Installing LPHK...
set STARTPATH=%CD%
cd %~dp0
call conda env create -f environment.yml
if errorlevel 1 goto INSTALLLPHKFAIL

REM TODO: Use environments.txt
call conda activate LPHK
FOR /F "tokens=*" %%g IN ('where python ^| findstr /R /C:"LPHK"') do (set LPHKPYTHON=%%g)
call conda deactivate
if errorlevel 1 goto INSTALLLPHKFAIL

cd ..
set MAINDIR=%CD%
cd %STARTPATH%

set LPHKSCRIPT=%MAINDIR%\LPHK.py

set LINKPATH=%MAINDIR%\LPHK.lnk
set LPHKICON=%MAINDIR%\resources\LPHK.ico

del %LINKPATH% 2> nul

set SHORTCUTSCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SHORTCUTSCRIPT%
echo sLinkFile = "%LINKPATH%" >> %SHORTCUTSCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SHORTCUTSCRIPT%
echo oLink.TargetPath = """%LPHKPYTHON%""" >> %SHORTCUTSCRIPT%
echo oLink.Arguments = """%LPHKSCRIPT%""" >> %SHORTCUTSCRIPT%
echo oLink.IconLocation = "%LPHKICON%" >> %SHORTCUTSCRIPT%
echo oLink.Save >> %SHORTCUTSCRIPT%
call cscript /nologo %SHORTCUTSCRIPT%
del %SHORTCUTSCRIPT%
if not exist %LINKPATH% goto INSTALLSHORTCUTFAILED
if errorlevel 1 goto INSTALLSHORTCUTFAILED
goto DESKTOPLINKMAKE

:INSTALLLPHKFAIL
call conda env remove -n LPHK
REM TODO: Use environments.txt
rmdir %USERPROFILE%\Miniconda3\envs\LPHK /s /q 2> nul
goto ERROREND

:INSTALLSHORTCUTFAILED
echo LPHK conda environment was installed, but a link could not be created!
echo Please run "%LPHKPYTHON%" "%LPHKSCRIPT%" to use LPHK!
echo Also, please report this bug via the Discord or GitHub issues.
goto ERROREND

:ALREADYINSTALLED
echo LPHK is already installed!
set "AREYOUSURE="
set /P AREYOUSURE=Uninstall LPHK? (Y/[N]): 
if /I "%AREYOUSURE%" EQU "Y" goto UNINSTALLLPHK
goto NOUNINSTALLLPHK

:UNINSTALLLPHK
echo Uninstalling LPHK...
call conda env remove -n LPHK
REM TODO: Use environments.txt
rmdir %USERPROFILE%\Miniconda3\envs\LPHK /s /q 2> nul
if errorlevel 1 goto ERROREND

echo LPHK conda environment unistalled.
echo Please manually delete shortcuts, program files, and if desired, uninstall Miniconda3.
echo Run this installer again ro re-install.
goto END

:NOUNINSTALLLPHK
echo Not uninstalling LPHK, exiting...
goto END

:NOINSTALLLPHK
echo Not installing LPHK, exiting...
goto END

:NOINSTALLCONDA
echo Not installing MiniConda3 or LPHK, exiting...
goto END

:NOINSTALLCONDA
echo Not installing LPHK, exiting...
goto END

:DESKTOPLINKMAKE
echo Installation done! Shortcut created at %LINKPATH%

set "AREYOUSURE="
set /P AREYOUSURE=Install desktop shortcut? (Y/[N])
if /I "%AREYOUSURE%" EQU "Y" goto INSTALLSHORTCUT

echo Run this installer again to uninstall LPHK.
goto END

:INSTALLSHORTCUT
set DESKTOPLINK=%USERPROFILE%\Desktop\
copy "%LINKPATH%" "%DESKTOPLINK%"
if errorlevel 1 goto ERROREND

echo Copied shortcut to desktop.
echo Run this installer again to uninstall LPHK.
goto END

:ERROREND
echo The installer has failed!
echo Please try running again, or seek help in the Discord.
goto END

:END
pause

:HARDEND
