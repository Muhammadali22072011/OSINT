@echo off
title OSINT Toolkit - Social Engineering Framework
color 0A

echo.
echo  ===================================================
echo   🕵️ OSINT Toolkit - Social Engineering Framework
echo  ===================================================
echo.

REM Проверка наличия Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден!
    echo Пожалуйста, установите Python 3.7+ с https://python.org
    pause
    exit /b 1
)

echo ✅ Python найден

REM Запуск программы
echo 🚀 Запуск OSINT Toolkit...
echo.

python run.py

echo.
echo 👋 Программа завершена
pause
