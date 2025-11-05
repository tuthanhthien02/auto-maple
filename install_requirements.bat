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

REM Upgrade pip (optional, but recommended)
echo [~] Upgrading pip to latest version...
echo     This may take a moment, please wait...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo [!] Warning: Failed to upgrade pip, continuing anyway...
    echo     This won't affect package installation.
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
echo     This may take several minutes, please be patient...
echo.

REM Try installing all packages together first
python -m pip install -r requirements.txt --upgrade
if errorlevel 1 (
    echo.
    echo [!] Some packages failed to install. Trying to install packages individually...
    echo.
    
    REM Install packages one by one for better error handling
    set FAILED_PACKAGES=
    set INSTALLED_COUNT=0
    set TOTAL_COUNT=0
    
    for /f "tokens=*" %%p in (requirements.txt) do (
        set PACKAGE=%%p
        set PACKAGE=!PACKAGE: =!
        if not "!PACKAGE!"=="" if not "!PACKAGE:~0,1!"=="#" (
            set /a TOTAL_COUNT+=1
            echo [~] Installing !PACKAGE! (!TOTAL_COUNT! of ~11)...
            python -m pip install !PACKAGE! --upgrade --no-cache-dir
            if errorlevel 1 (
                echo [X] Failed to install !PACKAGE!
                set FAILED_PACKAGES=!FAILED_PACKAGES! !PACKAGE!
            ) else (
                echo [✓] Successfully installed !PACKAGE!
                set /a INSTALLED_COUNT+=1
            )
            echo.
        )
    )
    
    if not "!FAILED_PACKAGES!"=="" (
        echo.
        echo [!] WARNING: Some packages failed to install:
        echo     !FAILED_PACKAGES!
        echo.
        echo [!] If you see build errors, you may need to install Visual Studio Build Tools:
        echo     Download from: https://visualstudio.microsoft.com/downloads/
        echo     Install "Desktop development with C++" workload
        echo.
        echo [!] Or try installing pre-built wheels by upgrading pip and setuptools:
        echo     python -m pip install --upgrade pip setuptools wheel
        echo.
        echo [!] Continuing with verification...
        echo.
    ) else (
        echo [✓] All packages installed successfully!
    )
) else (
    echo [✓] Main requirements installed successfully
)
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
echo.
set VERIFY_FAILED=0

python -c "import cv2" >nul 2>&1
if errorlevel 1 (echo [X] cv2 not found) else (echo [✓] cv2 (OpenCV) OK)

python -c "import numpy" >nul 2>&1
if errorlevel 1 (
    echo [X] numpy not found
    set VERIFY_FAILED=1
) else (
    echo [✓] numpy OK
)

python -c "import keyboard" >nul 2>&1
if errorlevel 1 (
    echo [X] keyboard not found
    set VERIFY_FAILED=1
) else (
    echo [✓] keyboard OK
)

python -c "import mss" >nul 2>&1
if errorlevel 1 (
    echo [X] mss not found
    set VERIFY_FAILED=1
) else (
    echo [✓] mss OK
)

python -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo [X] pygame not found
    set VERIFY_FAILED=1
) else (
    echo [✓] pygame OK
)

python -c "import psutil" >nul 2>&1
if errorlevel 1 (
    echo [X] psutil not found
    set VERIFY_FAILED=1
) else (
    echo [✓] psutil OK
)

python -c "import serial" >nul 2>&1
if errorlevel 1 (
    echo [X] pyserial not found
    set VERIFY_FAILED=1
) else (
    echo [✓] pyserial OK
)

python -c "import git" >nul 2>&1
if errorlevel 1 (
    echo [X] GitPython not found
    set VERIFY_FAILED=1
) else (
    echo [✓] GitPython OK
)

python -c "import tensorflow" >nul 2>&1
if errorlevel 1 (
    echo [X] tensorflow not found
    set VERIFY_FAILED=1
) else (
    echo [✓] tensorflow OK
)

echo.

if !VERIFY_FAILED!==1 (
    echo [!] Some packages failed verification
    echo     Please check the error messages above
    echo.
    echo [!] Common solutions:
    echo     1. Install Visual Studio Build Tools (for packages that need compilation):
    echo        https://visualstudio.microsoft.com/downloads/
    echo        Select "Desktop development with C++" workload
    echo.
    echo     2. Try upgrading pip and installing again:
    echo        python -m pip install --upgrade pip setuptools wheel
    echo        python -m pip install -r requirements.txt --upgrade
    echo.
    echo     3. For TensorFlow, try installing specific version:
    echo        python -m pip install tensorflow
    echo.
) else (
    echo [✓] All core packages verified successfully!
)
echo.

echo ========================================
if !VERIFY_FAILED!==1 (
    echo    INSTALLATION COMPLETE WITH WARNINGS
) else (
    echo    INSTALLATION COMPLETE!
)
echo ========================================
echo.
echo [!] You can now try running the program with: python main.py
echo.
pause

