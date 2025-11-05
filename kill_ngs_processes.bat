@echo off
setlocal
REM Change to script directory
cd /d "%~dp0"

echo ========================================
echo Kill NGS Sensitive Processes
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Python not found. Please install Python first.
    pause
    exit /b 1
)

REM Run with --kill flag (with confirmation)
python check_ngs_processes.py --kill

pause
