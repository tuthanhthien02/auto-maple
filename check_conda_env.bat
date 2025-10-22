@echo off
REM ============================================================
REM Kiem tra Conda environment "automaple"
REM ============================================================

echo.
echo ============================================================
echo CONDA ENVIRONMENT CHECK
echo ============================================================
echo.

REM Kiem tra conda
echo [1/3] Kiem tra Conda installation...
conda --version 2>nul
if errorlevel 1 (
    echo ERROR: Conda chua duoc cai dat!
    pause
    exit /b 1
)
echo.

REM List environments
echo [2/3] Danh sach conda environments:
echo ------------------------------------------------------------
conda env list
echo.

REM Kiem tra environment "automaple"
echo [3/3] Kiem tra environment "automaple"...
echo ------------------------------------------------------------
conda env list | find "automaple" >nul
if errorlevel 1 (
    echo.
    echo WARNING: Environment "automaple" chua ton tai!
    echo Vui long chay setup_conda.bat de tao environment
    echo.
) else (
    echo.
    echo OK - Environment "automaple" da ton tai
    echo.
    echo Kich hoat environment...
    call conda activate automaple
    echo.
    echo Python version:
    python --version
    echo.
    echo Installed packages:
    echo ------------------------------------------------------------
    conda list | find "numpy"
    conda list | find "opencv"
    conda list | find "pillow"
    pip list | find "keyboard"
    pip list | find "pywin32"
    pip list | find "mss"
    pip list | find "pygame"
    pip list | find "GitPython"
    echo.
)

echo ============================================================
echo.
pause

