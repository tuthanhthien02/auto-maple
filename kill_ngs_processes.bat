@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo ========================================
echo    NGS PROCESS KILLER
echo    Kill ALL processes TRƯỚC KHI start bot
echo ========================================
echo.
echo [!] WARNING: This will kill ALL sensitive processes
echo [!] Run this BEFORE starting bot to avoid NGS detection
echo.

REM Check admin
net session >nul 2>&1
if errorlevel 1 (
    echo [X] WARNING: Not running as Administrator
    echo     Some processes may fail to kill.
    echo     For best results, run as Administrator.
    echo.
    echo Press any key to continue anyway...
    pause >nul
)

echo [~] Running Python script to kill processes...
echo.

REM Run Python script
python kill_ngs_processes.py

if errorlevel 1 (
    echo.
    echo [X] ERROR: Python script failed!
    echo.
    echo Trying fallback method...
    echo.
    
    REM Fallback: Kill common processes manually
    echo [Fallback] Killing common processes...
    
    REM Kill Python processes
    taskkill /F /IM python.exe >nul 2>&1
    taskkill /F /IM pythonw.exe >nul 2>&1
    
    REM Kill bot executable
    taskkill /F /IM ExplorerSettings.exe >nul 2>&1
    
    REM Kill AutoHotkey
    taskkill /F /IM autohotkey.exe >nul 2>&1
    taskkill /F /IM autohotkeyu64.exe >nul 2>&1
    taskkill /F /IM autohotkeyu32.exe >nul 2>&1
    
    REM Kill VMware processes
    taskkill /F /IM vmware.exe >nul 2>&1
    taskkill /F /IM vmwaretray.exe >nul 2>&1
    taskkill /F /IM vmwareuser.exe >nul 2>&1
    taskkill /F /IM vmwaretools.exe >nul 2>&1
    taskkill /F /IM vmtoolsd.exe >nul 2>&1
    
    echo [Fallback] Done.
    echo.
)

echo.
echo ========================================
echo    VERIFICATION
echo ========================================
echo.

REM Verify no sensitive processes
echo Checking for remaining processes...
python check_ngs_processes.py --brief

echo.
echo ========================================
echo    DONE
echo ========================================
echo.
pause
