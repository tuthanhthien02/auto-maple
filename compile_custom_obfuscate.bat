@echo off
REM ═══════════════════════════════════════════════════════════
REM COMPILE + OBFUSCATE MULTIPLICITY JITTER CUSTOM
REM ═══════════════════════════════════════════════════════════
REM This compiles AND renames to a legitimate-sounding name
REM to avoid anti-cheat detection!
REM ═══════════════════════════════════════════════════════════

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                                                        ║
echo ║   🔧 COMPILE + OBFUSCATE 🔧                           ║
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
    pause
    exit /b 1
)

echo ✅ Compiler found
echo ✅ Source found
echo.

REM ═══════════════════════════════════════════════════════════
REM Choose obfuscated name
REM ═══════════════════════════════════════════════════════════

echo 🎭 Choose obfuscated name:
echo.
echo 1. WindowsUpdateHelper.exe    (Most believable!)
echo 2. SystemAudioService.exe     (Good)
echo 3. DisplayManager.exe          (Good)
echo 4. NetworkHelper.exe           (Good)
echo 5. SecurityHelper.exe          (Good)
echo 6. Custom name (you type it)
echo.

set /p CHOICE="Enter choice (1-6): "

if "%CHOICE%"=="1" set OBFNAME=WindowsUpdateHelper.exe
if "%CHOICE%"=="2" set OBFNAME=SystemAudioService.exe
if "%CHOICE%"=="3" set OBFNAME=DisplayManager.exe
if "%CHOICE%"=="4" set OBFNAME=NetworkHelper.exe
if "%CHOICE%"=="5" set OBFNAME=SecurityHelper.exe
if "%CHOICE%"=="6" (
    set /p OBFNAME="Enter custom name (with .exe): "
)

if "%OBFNAME%"=="" (
    echo ❌ Invalid choice!
    pause
    exit /b 1
)

echo.
echo 🔨 Compiling as: %OBFNAME%
echo.

REM Compile the script with obfuscated name + Windows system icon
REM Using shell32.dll (more compatible) for legitimate-looking Windows icon
"%COMPILER%" /in "multiplicity_jitter_CUSTOM.ahk" /out "%OBFNAME%" /icon "%SystemRoot%\System32\shell32.dll,3"

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
echo ║   ✅ COMPILATION + OBFUSCATION SUCCESSFUL! ✅         ║
echo ║                                                        ║
echo ║   Output: %OBFNAME%
echo ║                                                        ║
echo ║   ⚠️ ANTI-DETECTION TIPS:                            ║
echo ║   - File looks like legitimate Windows utility        ║
echo ║   - Harder for anti-cheat to detect                   ║
echo ║   - Use this instead of original .ahk                 ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo 📦 File created: %OBFNAME%
echo.
echo 🚀 Next steps:
echo    1. Test: Double-click %OBFNAME%
echo    2. If works: Use this for farming
echo    3. Setup autostart: Run setup_autostart_custom.bat
echo.
pause

