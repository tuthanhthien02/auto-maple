@echo off
echo ============================================================
echo FORCE FIX OPENCV - Kill processes va cai lai
echo ============================================================
echo CANH BAO: Script nay se:
echo 1. Tat tat ca Python/pip processes
echo 2. Xoa pip cache
echo 3. Cai lai OpenCV
echo.
echo Nhan phim bat ky de tiep tuc, hoac dong cua so de huy...
pause
echo.

echo [1/6] Tat tat ca Python va pip processes...
echo ============================================================
taskkill /F /IM python.exe 2>nul
taskkill /F /IM pip.exe 2>nul
taskkill /F /IM pip3.exe 2>nul
echo OK - Da tat processes (neu co)
echo.

echo [2/6] Doi 10 giay de Windows unlock files...
echo ============================================================
timeout /t 10 /nobreak
echo.

echo [3/6] Xoa pip cache...
echo ============================================================
pip cache purge 2>nul
echo.

echo [4/6] Xoa temp files...
echo ============================================================
del /F /Q "%TEMP%\pip-*" 2>nul
echo.

echo [5/6] Kich hoat conda environment...
echo ============================================================
call conda activate automaple
if errorlevel 1 (
    echo WARNING: Khong kich hoat duoc environment
    echo Thu cai trong base environment...
)
echo.

echo [6/6] Cai OpenCV...
echo ============================================================
echo.

echo Thu cach 1: Conda install (co pre-built binary)...
conda install opencv -y 2>nul
python -c "import cv2; print('SUCCESS - OpenCV version:', cv2.__version__)" 2>nul
if not errorlevel 1 goto :success

echo Thu cach 2: Pip install headless version...
pip install --timeout=300 --retries=10 opencv-python-headless --no-cache-dir --force-reinstall 2>nul
python -c "import cv2; print('SUCCESS - OpenCV version:', cv2.__version__)" 2>nul
if not errorlevel 1 goto :success

echo Thu cach 3: Pip install full version...
pip install --timeout=300 --retries=10 opencv-python --no-cache-dir 2>nul
python -c "import cv2; print('SUCCESS - OpenCV version:', cv2.__version__)" 2>nul
if not errorlevel 1 goto :success

echo Thu cach 4: Cai version cu hon (4.8.0.76)...
pip install --timeout=300 opencv-python-headless==4.8.0.76 --no-cache-dir 2>nul
python -c "import cv2; print('SUCCESS - OpenCV version:', cv2.__version__)" 2>nul
if not errorlevel 1 goto :success

echo Thu cach 5: Dung --user flag...
pip install --user --timeout=300 opencv-python-headless --no-cache-dir 2>nul
python -c "import cv2; print('SUCCESS - OpenCV version:', cv2.__version__)" 2>nul
if not errorlevel 1 goto :success

echo.
echo ============================================================
echo TAT CA CACH DEU THAT BAI!
echo ============================================================
echo.
echo Vui long thu:
echo 1. Kiem tra internet: ping pypi.org
echo 2. Tat antivirus/firewall tam thoi
echo 3. Chay script voi quyen Administrator
echo 4. Xem file FIX_OPENCV_ERROR.md de biet them chi tiet
echo.
echo Hoac download wheel thu cong tu:
echo https://pypi.org/project/opencv-python-headless/#files
echo.
pause
exit /b 1

:success
echo.
echo ============================================================
echo THANH CONG! Da cai OpenCV
echo ============================================================
echo.
python -c "import cv2; print('OpenCV version:', cv2.__version__); print('Module path:', cv2.__file__)"
echo.
echo Kiem tra tat ca packages...
python -c "import numpy; print('numpy:', numpy.__version__)"
python -c "from PIL import Image; print('Pillow: OK')"
python -c "import mss; print('mss: OK')"
echo.
echo Neu tat ca deu OK, co the chay bot: run_bot_conda.bat
echo.
pause

