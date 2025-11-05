@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo ========================================
echo    AUTO MAPLE - INSTALL REQUIREMENTS
echo ========================================
echo.
echo [~] Working directory: %CD%
echo.

REM Check if Python is installed
echo [~] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [✓] Python !PYTHON_VERSION! found
echo.

REM Upgrade pip
echo [~] Upgrading pip...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo [X] Warning: Failed to upgrade pip, continuing anyway...
) else (
    echo [✓] Pip upgraded successfully
)
echo.

REM Install main requirements
if not exist "requirements.txt" (
    echo [X] ERROR: requirements.txt not found in current directory
    echo     Current directory: %CD%
    echo     Please make sure you're running this script from the project root folder.
    echo.
    pause
    exit /b 1
)

echo [~] Installing main requirements from requirements.txt...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [X] ERROR: Failed to install main requirements
    echo.
    echo Please check the error messages above and try again.
    echo.
    pause
    exit /b 1
)
echo [✓] Main requirements installed successfully
echo.

REM Install multiplicity requirements (optional)
if exist "version2_python\requirements_multiplicity.txt" (
    echo [~] Installing multiplicity requirements...
    python -m pip install -r version2_python\requirements_multiplicity.txt
    if errorlevel 1 (
        echo [!] Warning: Failed to install multiplicity requirements
        echo     This is optional and won't affect the main program
    ) else (
        echo [✓] Multiplicity requirements installed successfully
    )
    echo.
)

REM Verify installation
echo [~] Verifying installation...
python -c "import cv2, numpy, keyboard, mss, pygame, psutil, serial" >nul 2>&1
if errorlevel 1 (
    echo [!] Warning: Some packages may not be installed correctly
    echo     Please check the error messages above
) else (
    echo [✓] Core packages verified successfully
)
echo.

echo ========================================
echo    INSTALLATION COMPLETE!
echo ========================================
echo.
echo [✓] All requirements have been installed successfully
echo.
echo You can now run the program with: python main.py
echo.
pause

