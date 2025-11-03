@echo off
:: Change to script directory
cd /d "%~dp0"

echo Starting Host Sender...
echo.

python host_sender.py

if %errorLevel% neq 0 (
    echo.
    echo Script exited with error code %errorLevel%
    pause
) else (
    pause >nul
)

