@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo   COMPILE AUTO PAUSE - OBFUSCATED
echo ========================================
echo.
echo ⚡ SỬ DỤNG SETTING MẶC ĐỊNH:
echo.
echo   ⏸️ Pause: VỪA PHẢI (mỗi 3-5 phút, 0.8-2.5 giây)
echo.
echo   ✅ Phù hợp: Hầu hết người dùng!
echo.
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
    echo.
    echo Vui long cai AutoHotkey v1.1:
    echo https://www.autohotkey.com/download/ahk-install.exe
    echo.
    pause
    exit /b 1
)

echo Compiling...
echo.

REM Compile WITHOUT icon parameter to avoid format errors
"%AHK_COMPILER%" /in "auto_pause_only.ahk" /out "auto_pause_only.exe"

if not exist "auto_pause_only.exe" (
    echo.
    echo ERROR: Compilation failed!
    pause
    exit /b 1
)

echo.
echo Obfuscating filename...
echo.

REM Rename to look like Windows system service
set "OBFUSCATED_NAME=WindowsUpdateHelper.exe"

REM Delete old file if exists
if exist "%OBFUSCATED_NAME%" (
    del "%OBFUSCATED_NAME%" 2>nul
)

REM Use MOVE instead of REN for more reliable operation
move /Y "auto_pause_only.exe" "%OBFUSCATED_NAME%" >nul 2>&1

REM Wait a moment for file system
timeout /t 1 /nobreak >nul 2>&1

REM Check if move was successful
if not exist "%OBFUSCATED_NAME%" (
    echo.
    echo ERROR: Obfuscation failed!
    echo File auto_pause_only.exe may be locked or in use.
    echo.
    echo TRY THIS:
    echo 1. Close any running auto_pause_only.exe or WindowsUpdateHelper.exe
    echo 2. Run this batch file again
    echo.
    pause
    exit /b 1
)

REM Double check old file is gone
if exist "auto_pause_only.exe" (
    del "auto_pause_only.exe" /F /Q >nul 2>&1
)

REM Success!
echo.
echo ========================================
echo   THANH CONG! ✅
echo ========================================
echo.
echo Output: %OBFUSCATED_NAME%
echo.
echo TINH NANG:
echo - Ten file gia mao he thong
echo - Chi co auto pause (khong remap/jitter)
echo - Pause ngau nhien giong nguoi that
echo.
echo TIEP THEO:
echo   1. Test file .exe (se thay tooltip khi pause)
echo   2. Neu OK, chay: setup_autostart_auto_pause.bat
echo.
echo ========================================
echo.

pause

