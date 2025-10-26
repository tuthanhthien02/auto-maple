@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo   COMPILE AUTO PAUSE - SIMPLE
echo ========================================
echo.

REM Check if AHK script exists
if not exist "auto_pause_only.ahk" (
    echo ERROR: auto_pause_only.ahk not found!
    echo Please make sure the file is in the same folder as this batch file.
    pause
    exit /b 1
)

REM Check if Ahk2Exe exists
set "AHK_COMPILER=C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe"
if not exist "%AHK_COMPILER%" (
    set "AHK_COMPILER=C:\Program Files (x86)\AutoHotkey\Compiler\Ahk2Exe.exe"
)

if not exist "%AHK_COMPILER%" (
    echo ERROR: Ahk2Exe.exe not found!
    echo Please install AutoHotkey v1.1 from https://www.autohotkey.com/download/ahk-install.exe
    pause
    exit /b 1
)

echo Compiling auto_pause_only.ahk...
echo.

REM Compile WITHOUT icon parameter to avoid format errors
"%AHK_COMPILER%" /in "auto_pause_only.ahk" /out "auto_pause_only.exe"

if exist "auto_pause_only.exe" (
    echo.
    echo ========================================
    echo   COMPILATION SUCCESS!
    echo ========================================
    echo.
    echo Output: auto_pause_only.exe
    echo.
    echo Next steps:
    echo 1. Test the .exe file
    echo 2. Run setup_autostart_auto_pause.bat to enable auto-start
    echo 3. Use remove_autostart_auto_pause.bat to disable if needed
    echo.
) else (
    echo.
    echo ========================================
    echo   COMPILATION FAILED!
    echo ========================================
    echo.
    echo Please check the error messages above.
    echo.
)

pause

