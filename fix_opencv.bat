@echo off
echo ============================================================
echo FIX OPENCV INSTALLATION
echo ============================================================
echo.

echo Dang xoa cache cu...
pip cache purge
echo.

echo Doi 5 giay de file unlock...
timeout /t 5 /nobreak
echo.

echo Cai OpenCV voi timeout dai hon...
pip install --timeout=300 opencv-python-headless --no-cache-dir
echo.

echo Kiem tra...
python -c "import cv2; print('OK - OpenCV version:', cv2.__version__)"
echo.

pause

