@echo off
setlocal enabledelayedexpansion
color 0A
title Compile All Jitter-Only Scripts (Hybrid Mode)

echo.
echo ════════════════════════════════════════════════════════════
echo  COMPILE JITTER-ONLY SCRIPTS (For use with PowerToys)
echo ════════════════════════════════════════════════════════════
echo.
echo  HYBRID SETUP:
echo  - PowerToys: Key Remapping (driver-level, safest)
echo  - AHK: Jitter/Delays only (no remapping)
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

if not exist "multiplicity_jitter_only_CLIENT1.ahk" (
    echo [ERROR] multiplicity_jitter_only_CLIENT1.ahk not found!
    set "MISSING_FILES=1"
)

if not exist "multiplicity_jitter_only_CLIENT2.ahk" (
    echo [ERROR] multiplicity_jitter_only_CLIENT2.ahk not found!
    set "MISSING_FILES=1"
)

if not exist "multiplicity_jitter_only_CLIENT3.ahk" (
    echo [ERROR] multiplicity_jitter_only_CLIENT3.ahk not found!
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
echo [1/3] Compiling CLIENT 1 (Jitter-Only)...
"!AHK_COMPILER!" /in "multiplicity_jitter_only_CLIENT1.ahk" /out "multiplicity_jitter_only_CLIENT1.exe" /silent
if !errorlevel! equ 0 (
    echo [OK] CLIENT 1 compiled successfully!
    
    REM Rename to obfuscated name
    if exist "InputTimingService_C1.exe" del "InputTimingService_C1.exe"
    ren "multiplicity_jitter_only_CLIENT1.exe" "InputTimingService_C1.exe"
    echo [OK] Renamed to: InputTimingService_C1.exe
) else (
    echo [ERROR] Failed to compile CLIENT 1!
)
echo.

REM Compile CLIENT 2
echo [2/3] Compiling CLIENT 2 (Jitter-Only)...
"!AHK_COMPILER!" /in "multiplicity_jitter_only_CLIENT2.ahk" /out "multiplicity_jitter_only_CLIENT2.exe" /silent
if !errorlevel! equ 0 (
    echo [OK] CLIENT 2 compiled successfully!
    
    REM Rename to obfuscated name
    if exist "InputTimingService_C2.exe" del "InputTimingService_C2.exe"
    ren "multiplicity_jitter_only_CLIENT2.exe" "InputTimingService_C2.exe"
    echo [OK] Renamed to: InputTimingService_C2.exe
) else (
    echo [ERROR] Failed to compile CLIENT 2!
)
echo.

REM Compile CLIENT 3
echo [3/3] Compiling CLIENT 3 (Jitter-Only)...
"!AHK_COMPILER!" /in "multiplicity_jitter_only_CLIENT3.ahk" /out "multiplicity_jitter_only_CLIENT3.exe" /silent
if !errorlevel! equ 0 (
    echo [OK] CLIENT 3 compiled successfully!
    
    REM Rename to obfuscated name
    if exist "InputTimingService_C3.exe" del "InputTimingService_C3.exe"
    ren "multiplicity_jitter_only_CLIENT3.exe" "InputTimingService_C3.exe"
    echo [OK] Renamed to: InputTimingService_C3.exe
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
if exist "InputTimingService_C1.exe" echo  [OK] InputTimingService_C1.exe
if exist "InputTimingService_C2.exe" echo  [OK] InputTimingService_C2.exe
if exist "InputTimingService_C3.exe" echo  [OK] InputTimingService_C3.exe
echo.
echo ════════════════════════════════════════════════════════════
echo  HYBRID SETUP DEPLOYMENT
echo ════════════════════════════════════════════════════════════
echo.
echo  STEP 1: Configure PowerToys on each client
echo  ───────────────────────────────────────────────────────────
echo  CLIENT 1: PowerToys - No remap (default keys)
echo  CLIENT 2: PowerToys - Remap Q -^> O, O -^> Q
echo  CLIENT 3: PowerToys - Remap Q -^> L, W -^> ;
echo.
echo  STEP 2: Deploy AHK Jitter Scripts
echo  ───────────────────────────────────────────────────────────
echo  Copy InputTimingService_C1.exe to CLIENT 1 PC
echo  Copy InputTimingService_C2.exe to CLIENT 2 PC
echo  Copy InputTimingService_C3.exe to CLIENT 3 PC
echo.
echo  STEP 3: Run Order (IMPORTANT!)
echo  ───────────────────────────────────────────────────────────
echo  1. PowerToys must be running (starts with Windows)
echo  2. Run InputTimingService_CX.exe
echo  3. Start MapleStory
echo.
echo  STEP 4: Configure In-Game Keybindings
echo  ───────────────────────────────────────────────────────────
echo  CLIENT 1: Bind skills to original keys (Q, W, E, etc.)
echo  CLIENT 2: Bind skills to remapped keys (O, W, E, etc.)
echo  CLIENT 3: Bind skills to remapped keys (L, ;, E, etc.)
echo.
echo ════════════════════════════════════════════════════════════
echo.
echo  NEXT: Read HYBRID_SETUP_GUIDE.md for detailed instructions
echo.
echo ════════════════════════════════════════════════════════════
echo.
pause

