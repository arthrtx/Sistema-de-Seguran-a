@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"

title Integrated Security System

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

echo ============================================
echo    Integrated Security System
echo ============================================
echo.

"%PY%" main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start the application.
    echo Make sure Python with tkinter is installed.
    echo.
    pause
)

endlocal
