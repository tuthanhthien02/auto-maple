@echo off
setlocal
cd /d "%~dp0"

REM Run keyboard_to_arduino.py as Administrator (UAC prompt)
REM Pass through any CLI args: run_keyboard_admin.bat COM13 115200 true 10.0 false
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_PATH=%SCRIPT_DIR%keyboard_to_arduino.py"
powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process python -ArgumentList '%SCRIPT_PATH% %*' -WorkingDirectory '%SCRIPT_DIR%' -Verb RunAs -Wait"

REM Check exit code and pause on error
if %errorLevel% neq 0 (
    echo.
    echo ========================================
    echo Script exited with error code %errorLevel%
    echo ========================================
    pause
) else (
    echo.
    echo ========================================
    echo Script finished. Press any key to close...
    pause >nul
)

endlocal

