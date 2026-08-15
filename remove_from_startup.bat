@echo off
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "Minilighter" /f
echo.
echo Minilighter successfully removed from startup!
pause
