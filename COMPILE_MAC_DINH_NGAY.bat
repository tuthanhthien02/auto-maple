@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo   COMPILE SETTING MẶC ĐỊNH - NHANH!
echo ========================================
echo.
echo ⚡ SỬ DỤNG SETTING MẶC ĐỊNH TỐI ƯU:
echo.
echo   🎚️ Training: MỨC TRUNG BÌNH (4-6 giờ/ngày)
echo       Desync: 0-500ms
echo.
echo   ⏸️ Pause: VỪA PHẢI (mỗi 3-5 phút, 0.8-2.5 giây)
echo.
echo   🎮 Key: MAPLESTORY (Q→A, W→S, E→D, R→F)
echo       Arrow keys + Space (có desync+jitter)
echo.
echo   ✅ Phù hợp: 95%% người dùng!
echo.
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
"%AHK_COMPILER%" /in "multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk" /out "multiplicity_jitter_DESYNC_EASY_CUSTOM.exe"

if not exist "multiplicity_jitter_DESYNC_EASY_CUSTOM.exe" (
    echo.
    echo ERROR: Compilation failed!
    pause
    exit /b 1
)

echo.
echo Obfuscating filename...
echo.

REM Rename to look like Windows system service
set "OBFUSCATED_NAME=SystemAudioService.exe"
if exist "%OBFUSCATED_NAME%" (
    del "%OBFUSCATED_NAME%"
)
ren "multiplicity_jitter_DESYNC_EASY_CUSTOM.exe" "%OBFUSCATED_NAME%"

if exist "%OBFUSCATED_NAME%" (
    echo.
    echo ========================================
    echo   THANH CONG! ✅
    echo ========================================
    echo.
    echo Output: %OBFUSCATED_NAME%
    echo.
    echo TIEP THEO:
    echo   1. Test file .exe tren Notepad
    echo   2. An Q W E R → Kiem tra delay va remap
    echo   3. Neu OK, chay: setup_autostart_EASY_CUSTOM.bat
    echo.
    echo ========================================
    echo.
) else (
    echo.
    echo ERROR: Obfuscation failed!
    echo.
)

pause

