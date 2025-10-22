@echo off
echo ============================================================
echo CAI OPENCV THU CONG (Neu pip install loi)
echo ============================================================
echo.

echo [1/5] Kich hoat conda environment...
call conda activate automaple
if errorlevel 1 (
    echo ERROR: Khong kich hoat duoc environment!
    echo Vui long chay setup_conda.bat truoc
    pause
    exit /b 1
)
echo OK
echo.

echo [2/5] Xoa pip cache...
pip cache purge
echo.

echo [3/5] Thu cai tu conda (co pre-built binary)...
conda install opencv -y
if errorlevel 1 (
    echo Conda khong co opencv, thu pip...
    goto :pip_install
)
echo.
echo Kiem tra...
python -c "import cv2; print('OK - OpenCV tu conda:', cv2.__version__)" 2>nul
if not errorlevel 1 (
    echo.
    echo ============================================================
    echo THANH CONG! Da cai opencv tu conda
    echo ============================================================
    pause
    exit /b 0
)

:pip_install
echo.
echo [4/5] Cai tu pip voi cac option khac nhau...
echo.

echo Thu cach 1: opencv-python-headless (headless version)...
pip install --timeout=300 --retries=5 opencv-python-headless --no-cache-dir
python -c "import cv2; print('OK')" 2>nul
if not errorlevel 1 goto :success
echo.

echo Thu cach 2: opencv-python (full version)...
pip install --timeout=300 --retries=5 opencv-python --no-cache-dir
python -c "import cv2; print('OK')" 2>nul
if not errorlevel 1 goto :success
echo.

echo Thu cach 3: Version cu hon (stable)...
pip install --timeout=300 opencv-python-headless==4.8.0.76 --no-cache-dir
python -c "import cv2; print('OK')" 2>nul
if not errorlevel 1 goto :success
echo.

echo Thu cach 4: Dung --user flag...
pip install --user --timeout=300 opencv-python-headless --no-cache-dir
python -c "import cv2; print('OK')" 2>nul
if not errorlevel 1 goto :success
echo.

echo [5/5] Tat ca deu that bai! Vui long thu:
echo 1. Kiem tra internet
echo 2. Tat antivirus tam thoi
echo 3. Chay lai voi quyen Administrator
echo 4. Download wheel thu cong tu: https://pypi.org/project/opencv-python-headless/#files
pause
exit /b 1

:success
echo.
echo ============================================================
echo [5/5] THANH CONG!
echo ============================================================
python -c "import cv2; print('OpenCV version:', cv2.__version__)"
echo.
pause

