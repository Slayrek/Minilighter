@echo off
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "Minilighter" /f
echo.
echo Minilighter removed from startup!
pause
