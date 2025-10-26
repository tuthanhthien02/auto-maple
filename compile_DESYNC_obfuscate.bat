@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo   COMPILE DESYNC - OBFUSCATED
echo ========================================
echo.

REM Check if AHK script exists
if not exist "multiplicity_jitter_WITH_DESYNC.ahk" (
    echo ERROR: multiplicity_jitter_WITH_DESYNC.ahk not found!
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

echo Step 1: Compiling AHK script...
echo.

REM Compile WITHOUT icon parameter to avoid format errors
"%AHK_COMPILER%" /in "multiplicity_jitter_WITH_DESYNC.ahk" /out "multiplicity_jitter_WITH_DESYNC.exe"

if not exist "multiplicity_jitter_WITH_DESYNC.exe" (
    echo.
    echo ERROR: Compilation failed!
    pause
    exit /b 1
)

echo.
echo Step 2: Obfuscating filename...
echo.

REM Rename to look like Windows system service
set "OBFUSCATED_NAME=WindowsUpdateService.exe"
if exist "%OBFUSCATED_NAME%" (
    del "%OBFUSCATED_NAME%"
)
ren "multiplicity_jitter_WITH_DESYNC.exe" "%OBFUSCATED_NAME%"

if exist "%OBFUSCATED_NAME%" (
    echo.
    echo ========================================
    echo   COMPILATION SUCCESS!
    echo ========================================
    echo.
    echo Output: %OBFUSCATED_NAME%
    echo.
    echo ANTI-DETECTION FEATURES:
    echo - Obfuscated filename (looks like Windows service)
    echo - Compiled to .exe (harder to detect than .ahk)
    echo - Desync delay breaks Multiplicity synchronization
    echo - Jitter makes timing unpredictable
    echo - Behavioral pauses mimic human breaks
    echo.
    echo Next steps:
    echo 1. Test %OBFUSCATED_NAME%
    echo 2. Run setup_autostart_DESYNC.bat to enable auto-start
    echo 3. Use remove_autostart_DESYNC.bat to disable if needed
    echo.
) else (
    echo.
    echo ERROR: Obfuscation failed!
    echo.
)

pause

