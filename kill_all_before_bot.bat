@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo ========================================
echo    NGS PRE-BOT KILLER
echo    Kill ALL processes TRƯỚC KHI start bot
echo ========================================
echo.
echo [!] WARNING: This will kill ALL sensitive processes
echo [!] Run this BEFORE starting bot to avoid NGS detection
echo.
echo This script kills:
echo   - VM processes (VMware, VirtualBox, etc.)
echo   - Keyboard hooks (Python scripts with hooks)
echo   - Automation tools (AutoHotkey, etc.)
echo   - Debugging tools
echo   - Bot processes (ExplorerSettings.exe, python.exe)
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

echo [~] Step 1: Killing ALL sensitive processes...
echo.

REM Run Python script (preferred method)
python kill_ngs_processes.py 2>nul

if errorlevel 1 (
    echo [X] Python script failed, using fallback method...
    echo.
    
    REM Fallback: Kill common processes manually
    echo [Fallback] Killing common processes...
    
    REM Kill Python processes (keyboard hooks, bot scripts)
    echo [1/6] Killing Python processes...
    taskkill /F /IM python.exe >nul 2>&1
    taskkill /F /IM pythonw.exe >nul 2>&1
    if errorlevel 1 (
        echo     No Python processes found
    ) else (
        echo     [✓] Python processes killed
    )
    timeout /t 1 >nul
    
    REM Kill bot executable
    echo [2/6] Killing bot executable...
    taskkill /F /IM ExplorerSettings.exe >nul 2>&1
    if errorlevel 1 (
        echo     No bot process found
    ) else (
        echo     [✓] Bot process killed
    )
    timeout /t 1 >nul
    
    REM Kill VMware processes
    echo [3/6] Killing VMware processes...
    taskkill /F /IM vmware.exe >nul 2>&1
    taskkill /F /IM vmwaretray.exe >nul 2>&1
    taskkill /F /IM vmwareuser.exe >nul 2>&1
    taskkill /F /IM vmwaretools.exe >nul 2>&1
    taskkill /F /IM vmtoolsd.exe >nul 2>&1
    if errorlevel 1 (
        echo     No VMware processes found
    ) else (
        echo     [✓] VMware processes killed
    )
    timeout /t 1 >nul
    
    REM Kill AutoHotkey processes
    echo [4/6] Killing AutoHotkey processes...
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
    echo [5/6] Killing debugging tools...
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
    timeout /t 1 >nul
    
    REM Kill VirtualBox processes
    echo [6/6] Killing VirtualBox processes...
    taskkill /F /IM virtualbox.exe >nul 2>&1
    taskkill /F /IM vboxsvc.exe >nul 2>&1
    taskkill /F /IM vboxmanage.exe >nul 2>&1
    if errorlevel 1 (
        echo     No VirtualBox processes found
    ) else (
        echo     [✓] VirtualBox processes killed
    )
    
    echo.
    echo [Fallback] Done.
    echo.
)

echo.
echo [~] Step 2: Verifying no sensitive processes remain...
echo.

REM Verify using check script
python check_ngs_processes.py --brief 2>nul

if errorlevel 1 (
    echo [X] Check script failed, using manual verification...
    echo.
    
    REM Manual verification
    set FOUND=0
    tasklist | findstr /I "python pythonw ExplorerSettings autohotkey vmware" >nul
    if errorlevel 1 (
        echo [✓] No sensitive processes found - SAFE TO START BOT
        set FOUND=0
    ) else (
        echo [!] WARNING: Some processes still running!
        echo.
        echo Remaining processes:
        tasklist | findstr /I "python pythonw ExplorerSettings autohotkey vmware"
        echo.
        echo Please kill them manually or restart the script
        set FOUND=1
    )
) else (
    set FOUND=0
)

echo.
echo ========================================
if !FOUND!==0 (
    echo    ✅ READY TO START BOT
    echo ========================================
    echo.
    echo [✓] All sensitive processes killed
    echo [✓] Safe to start bot now
    echo.
    echo Workflow:
    echo 1. ✅ Processes killed (done)
    echo 2. → Start game NOW
    echo 3. → Wait for game fully loaded
    echo 4. → Start bot AFTER game loaded
    echo.
    echo IMPORTANT:
    echo   - If bot is NOT compiled: Use compiled version to reduce detection risk
    echo   - If bot is compiled: Use ExplorerSettings.exe (not python main.py)
    echo.
) else (
    echo    ⚠️  PROCESSES STILL RUNNING
    echo ========================================
    echo.
    echo [!] Please kill remaining processes before starting bot
    echo     Try running as Administrator
    echo.
)

pause

