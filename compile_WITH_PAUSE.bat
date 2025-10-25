@echo off
REM ═══════════════════════════════════════════════════════════
REM COMPILE MULTIPLICITY JITTER WITH PAUSE
REM ═══════════════════════════════════════════════════════════

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                                                        ║
echo ║   🔧 COMPILING JITTER + BEHAVIORAL PAUSE 🔧           ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Check if AHK compiler exists
set COMPILER=C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe

if not exist "%COMPILER%" (
    echo ❌ ERROR: AHK Compiler not found!
    echo.
    echo Expected location: %COMPILER%
    echo.
    echo Please install AutoHotkey v1.1 from:
    echo https://www.autohotkey.com/download/ahk-install.exe
    echo.
    pause
    exit /b 1
)

REM Check if source script exists
if not exist "multiplicity_jitter_WITH_PAUSE.ahk" (
    echo ❌ ERROR: multiplicity_jitter_WITH_PAUSE.ahk not found!
    echo.
    pause
    exit /b 1
)

echo ✅ Compiler found
echo ✅ Source found: multiplicity_jitter_WITH_PAUSE.ahk
echo.
echo 🔨 Compiling...
echo.

REM Compile the script
"%COMPILER%" /in "multiplicity_jitter_WITH_PAUSE.ahk" /out "multiplicity_jitter_WITH_PAUSE.exe" /icon "C:\Program Files\AutoHotkey\AutoHotkey.exe,2"

if errorlevel 1 (
    echo.
    echo ❌ COMPILATION FAILED!
    echo.
    pause
    exit /b 1
)

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                                                        ║
echo ║   ✅ COMPILATION SUCCESSFUL! ✅                       ║
echo ║                                                        ║
echo ║   Output: multiplicity_jitter_WITH_PAUSE.exe          ║
echo ║                                                        ║
echo ║   Features:                                           ║
echo ║   ✅ Jitter (30-80ms Gaussian)                        ║
echo ║   ✅ Remap (Q→A, W→S, etc.)                           ║
echo ║   ✅ Behavioral pause (5-10 min intervals)            ║
echo ║   ✅ Arrow keys jitter (Up→Up with delay)             ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo 📦 File created: multiplicity_jitter_WITH_PAUSE.exe
echo.
echo 🚀 Next:
echo    1. Test: Double-click .exe
echo    2. Or: Run compile_WITH_PAUSE_obfuscate.bat to rename
echo.
pause

