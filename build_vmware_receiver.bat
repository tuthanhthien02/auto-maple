@echo off
REM Build script for vmware_receiver.py (Windows Batch)
REM Compiles to standalone executable using PyInstaller

echo ============================================================
echo Building vmware_receiver.py
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python first.
    pause
    exit /b 1
)

echo [INFO] Python found
echo.

REM Install PyInstaller if not available
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing PyInstaller...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] Failed to install PyInstaller
        pause
        exit /b 1
    )
)

REM Install dependencies
echo [INFO] Checking dependencies...
python -c "import serial" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing pyserial...
    python -m pip install pyserial
)

echo.
echo [INFO] Starting build...
echo.

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build with PyInstaller
python -m PyInstaller ^
    --onefile ^
    --noconsole ^
    --clean ^
    --noupx ^
    --name=system_service ^
    --add-data="src;src" ^
    --hidden-import=serial ^
    --hidden-import=serial.tools.list_ports ^
    --hidden-import=ctypes ^
    --hidden-import=ctypes.wintypes ^
    --hidden-import=winsound ^
    --hidden-import=src.common.serial_obfuscation ^
    --hidden-import=src.common.logger ^
    --collect-all=serial ^
    vmware_receiver.py

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

REM Check if exe was created
if exist "dist\system_service.exe" (
    echo.
    echo ============================================================
    echo Build successful!
    echo ============================================================
    echo.
    echo Executable: dist\system_service.exe
    echo.
    echo Next steps:
    echo 1. Test the executable
    echo 2. Copy to VMware machine
    echo 3. Run with: system_service.exe [COM_PORT] [BAUDRATE] [SERVER_PORT] [ENABLE_LOGGING]
    echo.
) else (
    echo.
    echo [ERROR] Build completed but executable not found!
    pause
    exit /b 1
)

pause

