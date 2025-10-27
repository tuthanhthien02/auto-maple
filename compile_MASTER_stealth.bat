@echo off
cd /d "%~dp0"

set AHK_SCRIPT=Master_Multi_VM_STEALTH.ahk
set COMPILED_NAME=WindowsTaskScheduler.exe
set ICON_PATH=

echo Compiling STEALTH Master script...
echo Script: %AHK_SCRIPT%
echo Output: %COMPILED_NAME%

; Check if Ahk2Exe.exe exists
if not exist "C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe" (
    echo Error: Ahk2Exe.exe not found at "C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe"
    echo Please install AutoHotkey or update the path to Ahk2Exe.exe in this script.
    pause
    exit /b 1
)

; Delete old compiled executable if it exists
if exist "%COMPILED_NAME%" (
    del "%COMPILED_NAME%"
)

; Compile the stealth script
"C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe" /in "%AHK_SCRIPT%" /out "%COMPILED_NAME%" %ICON_PATH%

if exist "%COMPILED_NAME%" (
    echo.
    echo ✅ SUCCESS: Stealth Master script compiled!
    echo 📁 Output: %COMPILED_NAME%
    echo 🥷 Features: No tray icon, silent operation, minimal footprint
    echo.
    echo ⚠️  WARNING: This version is designed to be undetectable!
    echo 💡 Use Master_Multi_VM_EASY_CUSTOM.ahk for normal use!
) else (
    echo ❌ ERROR: Failed to compile stealth Master script!
)

pause
