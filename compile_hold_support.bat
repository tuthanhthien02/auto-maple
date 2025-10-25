@echo off
setlocal enabledelayedexpansion
color 0A
title Compile Hold Support Script

echo.
echo ════════════════════════════════════════════════════════════
echo  COMPILE HOLD SUPPORT SCRIPT TO EXE
echo ════════════════════════════════════════════════════════════
echo.
echo  This will compile the .ahk script to standalone .exe
echo  The .exe can run WITHOUT AutoHotkey installed!
echo.
echo ════════════════════════════════════════════════════════════
echo.

REM Check if AutoHotkey is installed
set "AHK_COMPILER="

REM Common installation paths
set "PATHS="
set "PATHS=!PATHS! C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe"
set "PATHS=!PATHS! C:\Program Files (x86)\AutoHotkey\Compiler\Ahk2Exe.exe"
set "PATHS=!PATHS! %LOCALAPPDATA%\Programs\AutoHotkey\Compiler\Ahk2Exe.exe"
set "PATHS=!PATHS! %ProgramFiles%\AutoHotkey\Compiler\Ahk2Exe.exe"

for %%p in (!PATHS!) do (
    if exist "%%~p" (
        set "AHK_COMPILER=%%~p"
        goto :found_compiler
    )
)

echo [ERROR] AutoHotkey compiler not found!
echo.
echo Please install AutoHotkey from: https://www.autohotkey.com/
echo.
pause
exit /b 1

:found_compiler
echo [OK] Found AutoHotkey compiler: !AHK_COMPILER!
echo.

REM Check if script exists
if not exist "multiplicity_jitter_hold_support.ahk" (
    echo [ERROR] multiplicity_jitter_hold_support.ahk not found!
    echo.
    pause
    exit /b 1
)

echo [OK] Script found!
echo.
echo ════════════════════════════════════════════════════════════
echo  COMPILING...
echo ════════════════════════════════════════════════════════════
echo.

REM Compile script
"!AHK_COMPILER!" /in "multiplicity_jitter_hold_support.ahk" /out "multiplicity_jitter_hold_support.exe" /silent

if !errorlevel! equ 0 (
    echo [OK] Compilation successful!
    echo.
    
    REM Rename to obfuscated name
    if exist "InputTimingService.exe" del "InputTimingService.exe"
    ren "multiplicity_jitter_hold_support.exe" "InputTimingService.exe"
    echo [OK] Renamed to: InputTimingService.exe
    echo.
) else (
    echo [ERROR] Compilation failed!
    echo.
    pause
    exit /b 1
)

echo ════════════════════════════════════════════════════════════
echo  SUCCESS!
echo ════════════════════════════════════════════════════════════
echo.
echo  Created: InputTimingService.exe
echo.
echo  This .exe can run on ANY Windows PC/VM
echo  WITHOUT AutoHotkey installed!
echo.
echo ════════════════════════════════════════════════════════════
echo  DEPLOYMENT TO VM:
echo ════════════════════════════════════════════════════════════
echo.
echo  1. Copy InputTimingService.exe to VM
echo  2. Double-click to run (no install needed!)
echo  3. Check system tray for green H icon
echo  4. Done! ✅
echo.
echo ════════════════════════════════════════════════════════════
echo.
pause

