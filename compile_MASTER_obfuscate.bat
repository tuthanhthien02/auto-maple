@echo off
cd /d "%~dp0"

echo ========================================
echo   COMPILING MASTER VERSION (Obfuscated)
echo ========================================
echo.
echo Script: Master_Multi_VM_EASY_CUSTOM.ahk
echo Output: WindowsTaskScheduler.exe
echo.

REM Check if compiler exists
if not exist "C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe" (
    echo ERROR: AHK Compiler not found!
    echo Please install AutoHotkey from https://www.autohotkey.com/
    pause
    exit /b 1
)

REM Delete old exe if exists
if exist "WindowsTaskScheduler.exe" (
    echo Deleting old WindowsTaskScheduler.exe...
    del /F /Q "WindowsTaskScheduler.exe"
)

REM Compile script (without icon parameter to avoid errors)
echo Compiling...
"C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe" /in "Master_Multi_VM_EASY_CUSTOM.ahk" /out "temp_master.exe"

if errorlevel 1 (
    echo.
    echo ERROR: Compilation failed!
    pause
    exit /b 1
)

REM Rename to obfuscated name
echo Renaming to WindowsTaskScheduler.exe...
move /Y "temp_master.exe" "WindowsTaskScheduler.exe"

echo.
echo ========================================
echo   COMPILATION SUCCESSFUL!
echo ========================================
echo.
echo File created: WindowsTaskScheduler.exe
echo.
echo NEXT STEPS:
echo 1. Run WindowsTaskScheduler.exe on HOST
echo 2. Make sure all VMs are running
echo 3. Press Ctrl+Alt+L to list VMs
echo 4. Test broadcasting!
echo.
pause

