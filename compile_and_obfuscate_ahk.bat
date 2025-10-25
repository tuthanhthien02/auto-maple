@echo off
echo ========================================
echo COMPILE + OBFUSCATE AHK SCRIPTS
echo ========================================
echo.
echo This script will:
echo 1. Compile .ahk scripts to .exe
echo 2. Rename to innocent names
echo 3. Hide from game detection
echo.

REM Check if Ahk2Exe exists
set AHK_COMPILER=
if exist "C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe" (
    set AHK_COMPILER=C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe
) else if exist "C:\Program Files (x86)\AutoHotkey\Compiler\Ahk2Exe.exe" (
    set AHK_COMPILER=C:\Program Files ^(x86^)\AutoHotkey\Compiler\Ahk2Exe.exe
) else (
    echo ERROR: AutoHotkey compiler not found!
    echo Please install AutoHotkey first: https://www.autohotkey.com/
    pause
    exit /b 1
)

echo Found compiler: %AHK_COMPILER%
echo.

echo ========================================
echo COMPILING SCRIPTS
echo ========================================
echo.

REM Compile Input Jitter script
if exist "multiplicity_input_jitter.ahk" (
    echo Compiling: multiplicity_input_jitter.ahk
    "%AHK_COMPILER%" /in "multiplicity_input_jitter.ahk" /out "WindowsAudioDriver.exe"
    if %errorlevel%==0 (
        echo SUCCESS: WindowsAudioDriver.exe created! ✅
    ) else (
        echo ERROR: Failed to compile multiplicity_input_jitter.ahk
    )
    echo.
)

REM Compile Anti-Detection script
if exist "multiplicity_anti_detection_complete.ahk" (
    echo Compiling: multiplicity_anti_detection_complete.ahk
    "%AHK_COMPILER%" /in "multiplicity_anti_detection_complete.ahk" /out "SystemInputService.exe"
    if %errorlevel%==0 (
        echo SUCCESS: SystemInputService.exe created! ✅
    ) else (
        echo ERROR: Failed to compile multiplicity_anti_detection_complete.ahk
    )
    echo.
)

REM Compile Test script
if exist "test_multiplicity_broadcast.ahk" (
    echo Compiling: test_multiplicity_broadcast.ahk
    "%AHK_COMPILER%" /in "test_multiplicity_broadcast.ahk" /out "NetworkTestUtility.exe"
    if %errorlevel%==0 (
        echo SUCCESS: NetworkTestUtility.exe created! ✅
    ) else (
        echo ERROR: Failed to compile test_multiplicity_broadcast.ahk
    )
    echo.
)

echo.
echo ========================================
echo COMPILATION COMPLETE!
echo ========================================
echo.
echo Original scripts → Compiled + Renamed:
echo.
if exist "WindowsAudioDriver.exe" (
    echo ✅ multiplicity_input_jitter.ahk → WindowsAudioDriver.exe
)
if exist "SystemInputService.exe" (
    echo ✅ multiplicity_anti_detection_complete.ahk → SystemInputService.exe
)
if exist "NetworkTestUtility.exe" (
    echo ✅ test_multiplicity_broadcast.ahk → NetworkTestUtility.exe
)
echo.
echo IMPORTANT:
echo 1. Copy compiled .exe files to Client PCs
echo 2. Run .exe files (NOT .ahk files!)
echo 3. Delete or hide original .ahk files
echo.
echo Task Manager will show:
echo   WindowsAudioDriver.exe (looks like Windows service)
echo   SystemInputService.exe (looks like Windows service)
echo.
echo Much harder to detect! ✅
echo.

pause



