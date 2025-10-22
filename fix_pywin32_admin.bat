@echo off
REM ============================================================
REM FIX PYWIN32 - ADMIN VERSION (Tu dong xin quyen admin)
REM ============================================================

REM Kiem tra admin rights
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :run_fix
) else (
    echo.
    echo ============================================================
    echo CAN QUYEN ADMINISTRATOR
    echo ============================================================
    echo.
    echo Script se tu dong xin quyen Administrator...
    echo Nhan YES khi Windows hoi...
    echo.
    timeout /t 3 /nobreak >nul
    
    REM Chay lai voi admin rights
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:run_fix
echo ============================================================
echo FIX PYWIN32 - Register win32com (ADMIN MODE)
echo ============================================================
echo.

echo Kich hoat conda environment...
call conda activate automaple
if errorlevel 1 (
    echo ERROR: Khong kich hoat duoc environment!
    echo.
    echo Vui long mo Anaconda Prompt va chay:
    echo   conda activate automaple
    echo   python "%CONDA_PREFIX%\Scripts\pywin32_postinstall.py" -install
    echo.
    pause
    exit /b 1
)
echo OK
echo.

echo [1/5] Hien thi thong tin environment...
echo Python path: 
python -c "import sys; print(sys.executable)"
echo Conda prefix: %CONDA_PREFIX%
echo.

echo [2/5] Xoa pywin32 cu...
pip uninstall pywin32 -y
echo.

echo [3/5] Cai lai pywin32moi nhat...
pip install --upgrade pywin32
echo.

echo [4/5] Chay post-install script (register COM DLL)...
echo Dang register pythoncomXX.dll va pywintypesXX.dll...
python "%CONDA_PREFIX%\Scripts\pywin32_postinstall.py" -install
if errorlevel 1 (
    echo.
    echo WARNING: Scripts folder khong co file, thu site-packages...
    python "%CONDA_PREFIX%\Lib\site-packages\pywin32_postinstall.py" -install
)
echo.

echo [5/5] Test win32com...
python -c "import win32com.client; print('✓ win32com.client - OK')" 2>nul
if errorlevel 1 (
    echo ✗ win32com.client - FAILED
    echo.
    echo ERROR: Van khong hoat dong!
    echo.
    echo Thu cach khac:
    echo 1. Mo Anaconda Prompt AS ADMINISTRATOR
    echo 2. Chay: conda activate automaple
    echo 3. Chay: python -m pip install --upgrade --force-reinstall pywin32
    echo 4. Chay: python "%CONDA_PREFIX%\Scripts\pywin32_postinstall.py" -install
    echo.
    pause
    exit /b 1
)

python -c "import win32api; print('✓ win32api - OK')"
python -c "import win32con; print('✓ win32con - OK')"
echo.

echo ============================================================
echo THANH CONG!
echo ============================================================
echo.
echo win32com da duoc register thanh cong!
echo.
echo Bay gio co the chay:
echo   python setup.py
echo.
echo Hoac:
echo   python setup.py --stay
echo   (Giu cmd prompt mo sau khi bot tat)
echo.
pause

