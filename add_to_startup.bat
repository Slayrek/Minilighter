@echo off
set "EXE_PATH=%~dp0Minilighter.exe"
if not exist "%EXE_PATH%" (
    echo Error: Minilighter.exe not found in this folder!
    pause
    exit /b 1
)
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "Minilighter" /t REG_SZ /d "\"%EXE_PATH%\"" /f
echo.
echo Minilighter added to startup!
pause
