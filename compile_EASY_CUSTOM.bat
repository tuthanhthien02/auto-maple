@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo   COMPILE EASY CUSTOM SCRIPT - SIMPLE
echo ========================================
echo.

REM Check if AHK script exists
if not exist "multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk" (
    echo ERROR: multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk not found!
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

echo Compiling multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk...
echo.

REM Compile WITHOUT icon parameter to avoid format errors
"%AHK_COMPILER%" /in "multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk" /out "multiplicity_jitter_DESYNC_EASY_CUSTOM.exe"

if exist "multiplicity_jitter_DESYNC_EASY_CUSTOM.exe" (
    echo.
    echo ========================================
    echo   COMPILATION SUCCESS!
    echo ========================================
    echo.
    echo Output: multiplicity_jitter_DESYNC_EASY_CUSTOM.exe
    echo.
    echo Next steps:
    echo 1. Test the .exe file
    echo 2. If OK, run setup_autostart_EASY_CUSTOM.bat
    echo 3. Use remove_autostart_EASY_CUSTOM.bat to disable if needed
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

