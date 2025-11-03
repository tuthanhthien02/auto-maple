@echo off
:: Change to script directory
cd /d "%~dp0"

echo Starting Host Sender (admin mode)...
echo.

:: Check if running as admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs -Wait"
    exit /b
)

:: Run Python script with admin privileges
python host_sender.py

if %errorLevel% neq 0 (
    echo.
    echo Script exited with error code %errorLevel%
    pause
) else (
    pause >nul
)

