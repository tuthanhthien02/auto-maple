@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM Arduino Phase 2 Implementation - Upload Firmware to COM13
REM Modify device name và upload firmware

echo ========================================
echo    ARDUINO PHASE 2 IMPLEMENTATION
echo    Upload Firmware to COM13
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"

echo [~] Current directory: %CD%
echo.

REM Step 1: Modify Arduino core files
echo [1/3] Modifying Arduino core files...
echo.

python modify_arduino_device_name.py

set MODIFY_EXITCODE=%ERRORLEVEL%

if %MODIFY_EXITCODE% NEQ 0 (
    echo.
    echo [X] ERROR: Failed to modify Arduino core files!
    echo.
    echo Please check the output above for details.
    echo.
    pause
    exit /b %MODIFY_EXITCODE%
)

echo.
echo [✓] Arduino core files modified successfully!
echo.

REM Step 2: Instructions for Arduino IDE
echo [2/3] Instructions for Arduino IDE:
echo.
echo Please follow these steps:
echo.
echo 1. Open Arduino IDE
echo 2. File → Open: arduino_hid_keyboard\arduino_hid_keyboard.ino
echo 3. Tools → Board: Arduino Leonardo
echo 4. Tools → Port: COM13
echo 5. Sketch → Upload
echo.
echo Press any key when ready to continue...
pause >nul
echo.

REM Step 3: Verify device name (optional)
echo [3/3] Verify device name (optional):
echo.
echo After uploading firmware, verify device name:
echo.
echo 1. Open Device Manager (Windows + X → Device Manager)
echo 2. Keyboards → Find your device
echo 3. Right-click → Properties → Details
echo 4. Property: Device description
echo 5. Value: Should be "USB Keyboard" (not "Arduino Micro")
echo.
echo Press any key to continue...
pause >nul
echo.

echo ========================================
echo    PHASE 2 SETUP COMPLETE
echo ========================================
echo.
echo [✓] Arduino core files modified
echo [✓] Ready to upload firmware to COM13
echo.
echo Next steps:
echo 1. Open Arduino IDE
echo 2. Upload firmware to COM13
echo 3. Verify device name in Device Manager
echo.
pause

