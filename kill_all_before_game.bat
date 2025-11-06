@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo ========================================
echo    NGS CRITICAL PROCESS KILLER
echo    (Kill ALL processes TRƯỚC KHI start game)
echo ========================================
echo.
echo [!] WARNING: This will kill ALL sensitive processes
echo [!] Run this BEFORE starting MapleStory to avoid NGS detection
echo.

REM Check admin
net session >nul 2>&1
if errorlevel 1 (
    echo [X] ERROR: Please run as Administrator!
    echo.
    echo Right-click and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo [~] Killing ALL sensitive processes...
echo.

REM Kill Python processes (keyboard hooks)
echo [1/5] Killing Python processes...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM pythonw.exe >nul 2>&1
if errorlevel 1 (
    echo     No Python processes found
) else (
    echo     [✓] Python processes killed
)
timeout /t 1 >nul

REM Kill bot executable
echo [2/5] Killing bot executable...
taskkill /F /IM ExplorerSettings.exe >nul 2>&1
if errorlevel 1 (
    echo     No bot process found
) else (
    echo     [✓] Bot process killed
)
timeout /t 1 >nul

REM Kill keyboard hook scripts (by name)
echo [3/5] Killing keyboard hook scripts...
set KILLED_HOOKS=0
for /f "tokens=2" %%p in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV 2^>nul ^| findstr /I "python"') do (
    set PID=%%~p
    set PID=!PID:"=!
    wmic process where "ProcessId=!PID!" get CommandLine /format:value 2>nul | findstr /I "keyboard_to_arduino keyboard_block_arduino host_sender vmware_receiver" >nul
    if !errorlevel!==0 (
        taskkill /F /PID !PID! >nul 2>&1
        if !errorlevel!==0 (
            echo     [✓] Killed keyboard hook PID !PID!
            set /a KILLED_HOOKS+=1
        )
    )
)
if !KILLED_HOOKS!==0 (
    echo     No keyboard hook scripts found
)

REM Kill AutoHotkey processes
echo [4/5] Killing AutoHotkey processes...
taskkill /F /IM autohotkey.exe >nul 2>&1
taskkill /F /IM autohotkeyu64.exe >nul 2>&1
taskkill /F /IM autohotkeyu32.exe >nul 2>&1
taskkill /F /IM ahk.exe >nul 2>&1
if errorlevel 1 (
    echo     No AutoHotkey processes found
) else (
    echo     [✓] AutoHotkey processes killed
)
timeout /t 1 >nul

REM Kill debugging tools
echo [5/5] Killing debugging tools...
taskkill /F /IM cheatengine.exe >nul 2>&1
taskkill /F /IM x64dbg.exe >nul 2>&1
taskkill /F /IM x32dbg.exe >nul 2>&1
taskkill /F /IM ollydbg.exe >nul 2>&1
taskkill /F /IM ida.exe >nul 2>&1
taskkill /F /IM ida64.exe >nul 2>&1
if errorlevel 1 (
    echo     No debugging tools found
) else (
    echo     [✓] Debugging tools killed
)

echo.
echo [~] Verifying no sensitive processes...
timeout /t 2 >nul

REM Final check
set FOUND=0
tasklist | findstr /I "python pythonw ExplorerSettings autohotkey" >nul
if errorlevel 1 (
    echo [✓] No sensitive processes found - SAFE TO START GAME
    set FOUND=0
) else (
    echo [!] WARNING: Some processes still running!
    echo.
    echo Remaining processes:
    tasklist | findstr /I "python pythonw ExplorerSettings autohotkey"
    echo.
    echo Please kill them manually or restart the script
    set FOUND=1
)

echo.
echo ========================================
if !FOUND!==0 (
    echo    ✅ READY TO START GAME
    echo ========================================
    echo.
    echo [✓] All sensitive processes killed
    echo [✓] Safe to start MapleStory now
    echo.
    echo Workflow:
    echo 1. ✅ Processes killed (done)
    echo 2. → Start MapleStory NOW
    echo 3. → Wait for game fully loaded
    echo 4. → Start bot AFTER game loaded
    echo.
) else (
    echo    ⚠️  PROCESSES STILL RUNNING
    echo ========================================
    echo.
    echo [!] Please kill remaining processes before starting game
    echo.
)

pause

