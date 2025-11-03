@echo off
setlocal
cd /d "%~dp0"

REM Run keyboard_to_arduino.py as Administrator (UAC prompt)
REM Pass through any CLI args: run_keyboard_admin.bat COM13 115200 true 10.0 false
powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process python -ArgumentList 'keyboard_to_arduino.py %*' -Verb RunAs -Wait"

REM Pause to keep console open so user can see errors
echo.
echo ========================================
echo Script finished. Press any key to close...
pause >nul

endlocal

