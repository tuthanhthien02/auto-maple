@echo off
REM ═══════════════════════════════════════════════════════════
REM COMPILE MULTIPLICITY JITTER CUSTOM
REM ═══════════════════════════════════════════════════════════
REM This compiles the .ahk script to .exe for anti-detection
REM ═══════════════════════════════════════════════════════════

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                                                        ║
echo ║   🔧 COMPILING MULTIPLICITY JITTER CUSTOM 🔧          ║
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
if not exist "multiplicity_jitter_CUSTOM.ahk" (
    echo ❌ ERROR: multiplicity_jitter_CUSTOM.ahk not found!
    echo.
    echo Please make sure the script is in the same folder as this batch file.
    echo.
    pause
    exit /b 1
)

echo ✅ Compiler found: %COMPILER%
echo ✅ Source found: multiplicity_jitter_CUSTOM.ahk
echo.
echo 🔨 Compiling...
echo.

REM Compile the script with Windows system icon
REM Using shell32.dll (more compatible) for legitimate-looking Windows icon
"%COMPILER%" /in "multiplicity_jitter_CUSTOM.ahk" /out "multiplicity_jitter_CUSTOM.exe" /icon "%SystemRoot%\System32\shell32.dll,3"

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
echo ║   Output: multiplicity_jitter_CUSTOM.exe              ║
echo ║                                                        ║
echo ║   ⚠️ IMPORTANT:                                       ║
echo ║   - Use .exe instead of .ahk                          ║
echo ║   - Harder to detect by anti-cheat                    ║
echo ║   - Can rename .exe for extra obfuscation             ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo 📦 File created: multiplicity_jitter_CUSTOM.exe
echo.
echo 🚀 Next steps:
echo    1. Test: Double-click multiplicity_jitter_CUSTOM.exe
echo    2. If works: Use .exe instead of .ahk
echo    3. Optional: Run compile_custom_obfuscate.bat to rename
echo.
pause

