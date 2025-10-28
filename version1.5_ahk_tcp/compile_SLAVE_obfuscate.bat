@echo off
cd /d "%~dp0"

echo ========================================
echo   COMPILING SLAVE VERSION (Obfuscated)
echo ========================================
echo.
echo Script: multiplicity_jitter_DESYNC_SLAVE.ahk
echo Output: SystemAudioService.exe
echo.

REM Check if compiler exists
if not exist "C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe" (
    echo ERROR: AHK Compiler not found!
    echo Please install AutoHotkey from https://www.autohotkey.com/
    pause
    exit /b 1
)

REM Delete old exe if exists
if exist "SystemAudioService.exe" (
    echo Deleting old SystemAudioService.exe...
    del /F /Q "SystemAudioService.exe"
)

REM Compile script (without icon parameter to avoid errors)
echo Compiling...
"C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe" /in "multiplicity_jitter_DESYNC_SLAVE.ahk" /out "temp_slave.exe"

if errorlevel 1 (
    echo.
    echo ERROR: Compilation failed!
    pause
    exit /b 1
)

REM Rename to obfuscated name
echo Renaming to SystemAudioService.exe...
move /Y "temp_slave.exe" "SystemAudioService.exe"

echo.
echo ========================================
echo   COMPILATION SUCCESSFUL!
echo ========================================
echo.
echo File created: SystemAudioService.exe
echo.
echo NEXT STEPS:
echo 1. Copy SystemAudioService.exe to your VM
echo 2. Run it in the VM
echo 3. Run Master_Multi_VM.ahk on HOST
echo 4. Test!
echo.
pause

