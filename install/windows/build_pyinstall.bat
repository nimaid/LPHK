@echo off
set "ORIGDIR=%~dp0"
cd %~dp0\..\..

echo Building EXE...
call conda run -n LPHK-build pyinstaller --add-data VERSION;. --add-data resources\;resources\ --onefile --windowed --icon=resources\LPHK.ico LPHK.py
if errorlevel 1 goto ERROR

goto DONE

:ERROR
cd %ORIGDIR%
echo Build failed!
exit /B 1

:DONE
cd %ORIGDIR%
echo Build done!
exit /B 0