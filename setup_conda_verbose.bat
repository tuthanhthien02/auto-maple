@echo off
REM ============================================================
REM AUTO MAPLE - CONDA SETUP (Verbose version - Debug mode)
REM ============================================================
echo.
echo ============================================================
echo AUTO MAPLE - CONDA ENVIRONMENT SETUP (DEBUG MODE)
echo ============================================================
echo.
echo Script nay se:
echo 1. Tao conda environment "automaple"
echo 2. Cai dat Python 3.10
echo 3. Cai dat tat ca dependencies
echo 4. Kiem tra installation
echo.
echo DEBUG MODE: Script se hien thi tat ca output
echo.
echo Bat dau sau 5 giay...
timeout /t 5 /nobreak
echo.

REM Bat debug mode
@echo on

REM Kiem tra conda da duoc cai chua
echo [1/5] Kiem tra Conda...
echo ============================================================
conda --version
if errorlevel 1 (
    @echo off
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
    echo Nhan phim bat ky de thoat...
    pause
    exit /b 1
)
@echo off
echo OK - Conda da duoc cai dat
echo.

REM Xoa environment cu neu ton tai
echo [2/5] Xoa environment cu (neu co)...
echo ============================================================
@echo on
conda env remove -n automaple -y
@echo off
echo OK - Da xoa environment cu (neu co)
echo.

REM Tao environment moi
echo [3/5] Tao conda environment "automaple" (Python 3.10)...
echo ============================================================
echo Dang tai Python 3.10... (co the mat vai phut)
@echo on
conda create -n automaple python=3.10 -y
@echo off
if errorlevel 1 (
    echo.
    echo ERROR: Khong tao duoc conda environment!
    echo Nhan phim bat ky de thoat...
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
@echo on
call conda activate automaple
@echo off
if errorlevel 1 (
    echo.
    echo ERROR: Khong kich hoat duoc environment!
    echo Nhan phim bat ky de thoat...
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
@echo on
call conda install numpy opencv pillow -y
@echo off
if errorlevel 1 (
    echo WARNING: Co loi khi cai tu conda, thu dung pip...
    @echo on
    pip install numpy opencv-python-headless Pillow
    @echo off
)
echo.

echo ------------------------------------------------------------
echo [4b/5] Cai cac packages con lai tu pip...
echo ------------------------------------------------------------
echo.
@echo on
pip install keyboard pywin32 pygame GitPython mss
@echo off
echo.

REM Kiem tra installation
echo [5/5] Kiem tra installation...
echo ============================================================
echo.

echo Test import packages...
@echo on
python -c "import sys; print('Python version:', sys.version)"
@echo off
echo.

echo Testing packages...
python -c "import numpy; print('OK numpy:', numpy.__version__)"
python -c "import cv2; print('OK OpenCV:', cv2.__version__)"
python -c "from PIL import Image; print('OK Pillow')"
python -c "import win32api; print('OK pywin32')"
python -c "import mss; print('OK mss')"
python -c "import keyboard; print('OK keyboard')"
python -c "import pygame; print('OK pygame')"
python -c "import git; print('OK GitPython')"

echo.
echo ============================================================
echo HOAN THANH!
echo ============================================================
echo.
echo De chay bot:
echo 1. Mo Anaconda Prompt
echo 2. Chay: conda activate automaple
echo 3. Chay: python main.py
echo.
echo Hoac double-click file: run_bot_conda.bat
echo.
echo ============================================================
echo Nhan phim bat ky de dong cua so nay...
echo ============================================================
pause

