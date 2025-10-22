@echo off
echo ============================================================
echo AUTO MAPLE - INSTALLER FOR WINDOWS VM
echo ============================================================
echo.

echo Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.10 from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo.

echo ============================================================
echo Running safe installer...
echo ============================================================
python install_safe.py

echo.
echo ============================================================
echo DONE! Press any key to exit...
echo ============================================================
pause

