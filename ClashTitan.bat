@echo off
chcp 65001 >nul
title Clash Titan 2.0 - Created by Zodi4c

:: Set Working Directory to Script Location
cd /d "%~dp0"

:: Smart Universal Python Discovery (Skips Windows Store dummy alias)
set "PY_CMD="

:: 1. Search official Python install directories (AppData, ProgramFiles, Root)
for %%P in (
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    "%ProgramFiles%\Python311\python.exe"
    "%ProgramFiles%\Python312\python.exe"
    "%ProgramFiles%\Python310\python.exe"
    "%ProgramFiles(x86)%\Python311\python.exe"
    "C:\Python311\python.exe"
    "C:\Python312\python.exe"
    "C:\Python310\python.exe"
) do (
    if "%PY_CMD%"=="" if exist "%%~fP" set "PY_CMD="%%~fP""
)

:: 2. If not found in standard paths, test real execution via py launcher
if "%PY_CMD%"=="" (
    py -3 -c "import sys" >nul 2>nul
    if %ERRORLEVEL% equ 0 set "PY_CMD=py -3"
)

:: 3. Test real execution via PATH python (verifies it's not the broken Microsoft Store stub)
if "%PY_CMD%"=="" (
    python -c "import sys" >nul 2>nul
    if %ERRORLEVEL% equ 0 set "PY_CMD=python"
)

:: If Python is still not found, alert user
if "%PY_CMD%"=="" (
    color 0c
    echo ============================================================
    echo  [HATA / ERROR] Python bulunamadi! / Python not found!
    echo ============================================================
    echo  Lutfen Python 3.11 veya daha yeni bir surum yukleyin.
    echo  Please install Python 3.11 or newer and add to PATH.
    echo  https://www.python.org/downloads/
    echo ============================================================
    pause
    exit /b 1
)

:: Otomatik Paket Kontrolu / Auto Dependency Check
%PY_CMD% -c "import customtkinter, pyautogui, keyboard, cv2" >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ============================================================
    echo  [i] Ilk Kurulum: Paketler yukleniyor...
    echo  [i] First Run: Installing required dependencies...
    echo ============================================================
    %PY_CMD% -m pip install -r requirements.txt
    echo.
)

:: Start Clash Titan 2.0
%PY_CMD% main.py %*
if %ERRORLEVEL% neq 0 (
    echo.
    echo ============================================================
    echo  [!] Program bir hatayla kapandi. / Program exited with error.
    echo ============================================================
    pause
)

