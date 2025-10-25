@echo off
setlocal enabledelayedexpansion
color 0A
title Compile All Remap+Jitter Scripts (Layer 4+5)

echo.
echo ════════════════════════════════════════════════════════════
echo  COMPILE ALL REMAP + JITTER SCRIPTS (LAYER 4+5)
echo ════════════════════════════════════════════════════════════
echo.
echo  This will compile all 3 CLIENT scripts to EXE and rename them
echo  for obfuscation (makes them look like system services).
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

REM Check if CLIENT scripts exist
set "MISSING_FILES=0"

if not exist "multiplicity_remap_jitter_CLIENT1.ahk" (
    echo [ERROR] multiplicity_remap_jitter_CLIENT1.ahk not found!
    set "MISSING_FILES=1"
)

if not exist "multiplicity_remap_jitter_CLIENT2.ahk" (
    echo [ERROR] multiplicity_remap_jitter_CLIENT2.ahk not found!
    set "MISSING_FILES=1"
)

if not exist "multiplicity_remap_jitter_CLIENT3.ahk" (
    echo [ERROR] multiplicity_remap_jitter_CLIENT3.ahk not found!
    set "MISSING_FILES=1"
)

if !MISSING_FILES! equ 1 (
    echo.
    echo [ERROR] Missing required files!
    pause
    exit /b 1
)

echo [OK] All CLIENT scripts found!
echo.
echo ════════════════════════════════════════════════════════════
echo  COMPILING SCRIPTS...
echo ════════════════════════════════════════════════════════════
echo.

REM Compile CLIENT 1
echo [1/3] Compiling CLIENT 1...
"!AHK_COMPILER!" /in "multiplicity_remap_jitter_CLIENT1.ahk" /out "multiplicity_remap_jitter_CLIENT1.exe" /silent
if !errorlevel! equ 0 (
    echo [OK] CLIENT 1 compiled successfully!
    
    REM Rename to obfuscated name
    if exist "SystemInputService_C1.exe" del "SystemInputService_C1.exe"
    ren "multiplicity_remap_jitter_CLIENT1.exe" "SystemInputService_C1.exe"
    echo [OK] Renamed to: SystemInputService_C1.exe
) else (
    echo [ERROR] Failed to compile CLIENT 1!
)
echo.

REM Compile CLIENT 2
echo [2/3] Compiling CLIENT 2...
"!AHK_COMPILER!" /in "multiplicity_remap_jitter_CLIENT2.ahk" /out "multiplicity_remap_jitter_CLIENT2.exe" /silent
if !errorlevel! equ 0 (
    echo [OK] CLIENT 2 compiled successfully!
    
    REM Rename to obfuscated name
    if exist "SystemInputService_C2.exe" del "SystemInputService_C2.exe"
    ren "multiplicity_remap_jitter_CLIENT2.exe" "SystemInputService_C2.exe"
    echo [OK] Renamed to: SystemInputService_C2.exe
) else (
    echo [ERROR] Failed to compile CLIENT 2!
)
echo.

REM Compile CLIENT 3
echo [3/3] Compiling CLIENT 3...
"!AHK_COMPILER!" /in "multiplicity_remap_jitter_CLIENT3.ahk" /out "multiplicity_remap_jitter_CLIENT3.exe" /silent
if !errorlevel! equ 0 (
    echo [OK] CLIENT 3 compiled successfully!
    
    REM Rename to obfuscated name
    if exist "SystemInputService_C3.exe" del "SystemInputService_C3.exe"
    ren "multiplicity_remap_jitter_CLIENT3.exe" "SystemInputService_C3.exe"
    echo [OK] Renamed to: SystemInputService_C3.exe
) else (
    echo [ERROR] Failed to compile CLIENT 3!
)
echo.

echo ════════════════════════════════════════════════════════════
echo  COMPILATION COMPLETE!
echo ════════════════════════════════════════════════════════════
echo.
echo  Obfuscated executables created:
echo.
if exist "SystemInputService_C1.exe" echo  [OK] SystemInputService_C1.exe
if exist "SystemInputService_C2.exe" echo  [OK] SystemInputService_C2.exe
if exist "SystemInputService_C3.exe" echo  [OK] SystemInputService_C3.exe
echo.
echo ════════════════════════════════════════════════════════════
echo  DEPLOYMENT INSTRUCTIONS
echo ════════════════════════════════════════════════════════════
echo.
echo  1. Copy SystemInputService_C1.exe to CLIENT 1 PC
echo  2. Copy SystemInputService_C2.exe to CLIENT 2 PC
echo  3. Copy SystemInputService_C3.exe to CLIENT 3 PC
echo.
echo  4. Run each .exe BEFORE starting MapleStory
echo  5. Check system tray for AHK icon (green H)
echo.
echo  6. Configure in-game keybindings:
echo     - CLIENT 1: Keep original keys
echo     - CLIENT 2: Bind skills to remapped keys (e.g., Q -^> O)
echo     - CLIENT 3: Bind skills to remapped keys (e.g., Q -^> L)
echo.
echo ════════════════════════════════════════════════════════════
echo.
echo  NEXT: Move to Layer 6 (Behavioral Variation)
echo  File: multiplicity_anti_detection_complete.ahk
echo.
echo ════════════════════════════════════════════════════════════
echo.
pause

