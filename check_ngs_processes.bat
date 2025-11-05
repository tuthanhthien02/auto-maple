@echo off
setlocal
REM Change to script directory
cd /d "%~dp0"

echo ========================================
echo NGS Sensitive Processes Checker
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Python not found. Please install Python first.
    pause
    exit /b 1
)

REM Check if psutil is installed
python -c "import psutil" >nul 2>&1
if %errorLevel% neq 0 (
    echo [WARNING] psutil not found. Installing...
    pip install psutil
    if %errorLevel% neq 0 (
        echo [ERROR] Failed to install psutil. Please run: pip install psutil
        pause
        exit /b 1
    )
)

REM Run the Python script
python check_ngs_processes.py %*

if %errorLevel% neq 0 (
    echo.
    echo [ERROR] Script failed with error code %errorLevel%
    pause
    exit /b %errorLevel%
)

pause
