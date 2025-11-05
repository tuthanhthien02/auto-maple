@echo off
setlocal
REM Change to script directory
cd /d "%~dp0"

echo ========================================
echo VMware Stealth Checker
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Python not found. Please install Python first.
    pause
    exit /b 1
)

REM Run the Python script
python check_vmware_stealth.py %*

pause

