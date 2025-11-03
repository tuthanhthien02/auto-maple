@echo off
echo Starting keyboard block Arduino (admin mode)...
echo.

:: Check if running as admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs -Wait"
    exit /b
)

:: Run Python script with admin privileges
python keyboard_block_arduino.py

pause >nul

