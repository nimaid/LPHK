@echo off

REM DO NOT USE THIS SCRIPT. It is for the new Inno Setup installer.

set "MINICONDAPATH="
set "CONDAEXE="
set "OS="
set "MCLINK="

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
powershell -Command "(New-Object Net.WebClient).DownloadFile('%MCLINK%', '%CONDAEXE%')" 
if errorlevel 1 goto END

echo Installing Miniconda3... (This will also take a while, please wait...)
set MINICONDAPATH=%USERPROFILE%\Miniconda3
start /wait /min "Installing Miniconda3..." "%CONDAEXE%" /InstallationType=JustMe /S /D="%MINICONDAPATH%"
del "%CONDAEXE%"
if errorlevel 1 goto CONDAERROR
if not exist "%MINICONDAPATH%\" (goto CONDAERROR)

"%MINICONDAPATH%\Scripts\conda.exe" init
if errorlevel 1 goto CONDAERROR

echo Miniconda3 has been installed...
timeout 5
start cmd /c "%0 %CONDAWASINSTALLEDFLAG%"
goto END

:CONDAERROR
echo Miniconda3 install failed!
goto END

:CONDADONE
echo Conda is already installed!
goto HARDEND

:NOINSTALLCONDA
echo Not installing MiniConda3, exiting...
goto END

:END
pause

:HARDEND
