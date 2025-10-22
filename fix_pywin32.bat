@echo off
echo ============================================================
echo FIX PYWIN32 - Register win32com module
echo ============================================================
echo.

echo Kich hoat conda environment...
call conda activate automaple
if errorlevel 1 (
    echo ERROR: Khong kich hoat duoc environment!
    echo Vui long chay setup_conda.bat truoc
    pause
    exit /b 1
)
echo.

echo [1/4] Xoa pywin32 cu...
pip uninstall pywin32 -y
echo.

echo [2/4] Cai lai pywin32...
pip install --upgrade pywin32
echo.

echo [3/4] Chay post-install script (register COM)...
python "%CONDA_PREFIX%\Scripts\pywin32_postinstall.py" -install
echo.

echo [4/4] Test win32com...
python -c "import win32com.client; print('OK - win32com da hoat dong')"
if errorlevel 1 (
    echo.
    echo WARNING: Van chua hoat dong, thu cach khac...
    echo.
    echo Thu chay voi quyen Administrator...
    python "%CONDA_PREFIX%\Lib\site-packages\pywin32_postinstall.py" -install
    echo.
    echo Test lai lan nua...
    python -c "import win32com.client; print('OK - win32com da hoat dong')"
    if errorlevel 1 (
        echo.
        echo ERROR: Van khong duoc! Vui long:
        echo 1. Right-click script nay
        echo 2. Chon "Run as Administrator"
        echo 3. Chay lai
        pause
        exit /b 1
    )
)
echo.

echo ============================================================
echo HOAN THANH!
echo ============================================================
echo.
echo Bay gio co the chay: python setup.py
echo.
pause

