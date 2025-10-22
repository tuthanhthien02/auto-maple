@echo off
REM ============================================================
REM AUTO MAPLE - CONDA SETUP (Chạy sau khi cài Miniconda)
REM ============================================================
echo.
echo ============================================================
echo AUTO MAPLE - CONDA ENVIRONMENT SETUP
echo ============================================================
echo.
echo Script nay se:
echo 1. Tao conda environment "automaple"
echo 2. Cai dat Python 3.10
echo 3. Cai dat tat ca dependencies
echo 4. Kiem tra installation
echo.
echo Thoi gian du kien: 5-10 phut
echo.
pause
echo.

REM Kiem tra conda da duoc cai chua
echo [1/5] Kiem tra Conda...
echo ============================================================
conda --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Conda chua duoc cai dat!
    echo.
    echo Vui long cai Miniconda tu:
    echo https://docs.conda.io/en/latest/miniconda.html
    echo.
    echo Sau khi cai:
    echo 1. Restart terminal
    echo 2. Chay lai script nay
    echo.
    pause
    exit /b 1
)
echo OK - Conda da duoc cai dat
conda --version
echo.

REM Xoa environment cu neu ton tai
echo [2/5] Xoa environment cu (neu co)...
echo ============================================================
conda env remove -n automaple -y >nul 2>&1
echo OK - Da xoa environment cu (neu co)
echo.

REM Tao environment moi
echo [3/5] Tao conda environment "automaple" (Python 3.10)...
echo ============================================================
echo Dang tai Python 3.10... (co the mat vai phut)
conda create -n automaple python=3.10 -y
if errorlevel 1 (
    echo.
    echo ERROR: Khong tao duoc conda environment!
    pause
    exit /b 1
)
echo OK - Da tao environment "automaple"
echo.

REM Kich hoat environment va cai packages
echo [4/5] Cai dat packages...
echo ============================================================
echo.
echo Kich hoat environment "automaple"...
call conda activate automaple
if errorlevel 1 (
    echo.
    echo ERROR: Khong kich hoat duoc environment!
    pause
    exit /b 1
)
echo OK - Da kich hoat environment
echo.

echo ------------------------------------------------------------
echo [4a/5] Cai numpy, opencv, pillow tu conda...
echo ------------------------------------------------------------
echo (Co the mat 3-5 phut, vui long doi...)
echo.
call conda install numpy opencv pillow -y
if errorlevel 1 (
    echo WARNING: Co loi khi cai tu conda, thu dung pip...
    pip install numpy opencv-python-headless Pillow
)
echo.

echo ------------------------------------------------------------
echo [4b/5] Cai cac packages con lai tu pip...
echo ------------------------------------------------------------
echo.
pip install keyboard pywin32 pygame GitPython mss
echo.

REM Kiem tra installation
echo [5/5] Kiem tra installation...
echo ============================================================
echo.

echo Test import packages...
python -c "import sys; print('Python version:', sys.version)"
echo.

python -c "import numpy; print('✓ numpy:', numpy.__version__)" 2>nul
if errorlevel 1 (
    echo ✗ numpy - FAILED
    set ERROR_COUNT=1
) else (
    echo.
)

python -c "import cv2; print('✓ OpenCV:', cv2.__version__)" 2>nul
if errorlevel 1 (
    echo ✗ OpenCV - FAILED
    set ERROR_COUNT=1
) else (
    echo.
)

python -c "from PIL import Image; print('✓ Pillow: OK')" 2>nul
if errorlevel 1 (
    echo ✗ Pillow - FAILED
    set ERROR_COUNT=1
) else (
    echo.
)

python -c "import win32api; print('✓ pywin32: OK')" 2>nul
if errorlevel 1 (
    echo ✗ pywin32 - FAILED
    set ERROR_COUNT=1
) else (
    echo.
)

python -c "import mss; print('✓ mss: OK')" 2>nul
if errorlevel 1 (
    echo ✗ mss - FAILED
    set ERROR_COUNT=1
) else (
    echo.
)

python -c "import keyboard; print('✓ keyboard: OK')" 2>nul
if errorlevel 1 (
    echo ✗ keyboard - FAILED
    set ERROR_COUNT=1
) else (
    echo.
)

python -c "import pygame; print('✓ pygame: OK')" 2>nul
if errorlevel 1 (
    echo ✗ pygame - FAILED
    set ERROR_COUNT=1
) else (
    echo.
)

python -c "import git; print('✓ GitPython: OK')" 2>nul
if errorlevel 1 (
    echo ✗ GitPython - FAILED
    set ERROR_COUNT=1
) else (
    echo.
)

echo.
echo ============================================================
echo HOAN THANH!
echo ============================================================

if defined ERROR_COUNT (
    echo.
    echo WARNING: Mot so packages khong cai duoc
    echo Bot van co the chay nhung mot so tinh nang bi thieu
    echo.
) else (
    echo.
    echo ✓✓✓ TAT CA PACKAGES DA DUOC CAI DAT THANH CONG! ✓✓✓
    echo.
    echo De chay bot:
    echo 1. Mo Anaconda Prompt
    echo 2. Chay: conda activate automaple
    echo 3. Chay: cd "%~dp0"
    echo 4. Chay: python main.py
    echo.
    echo Hoac double-click file: run_bot_conda.bat
    echo.
)

echo Nhan phim bat ky de thoat...
pause >nul

