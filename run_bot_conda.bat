@echo off
REM ============================================================
REM AUTO MAPLE - START BOT (Conda Environment)
REM ============================================================

echo.
echo ============================================================
echo AUTO MAPLE BOT - STARTING
echo ============================================================
echo.

REM Kiem tra conda
conda --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Conda chua duoc cai dat!
    echo Vui long cai Miniconda va chay setup_conda.bat truoc
    pause
    exit /b 1
)

REM Kiem tra environment
conda env list | find "automaple" >nul
if errorlevel 1 (
    echo ERROR: Environment "automaple" chua duoc tao!
    echo Vui long chay setup_conda.bat truoc
    pause
    exit /b 1
)

echo Kich hoat conda environment "automaple"...
call conda activate automaple
echo.

echo Di chuyen den thu muc bot...
cd /d "%~dp0"
echo Thu muc hien tai: %CD%
echo.

echo ============================================================
echo Starting Auto Maple Bot...
echo ============================================================
echo Nhan Ctrl+C de dung bot
echo.

REM Chay bot
python main.py

REM Neu bot tat, hoi nguoi dung
echo.
echo ============================================================
echo Bot da dung
echo ============================================================
pause

