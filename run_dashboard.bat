@echo off
echo ================================================
echo        Iniciando PCBBR Dashboard
echo ================================================
echo.
cd /d "%~dp0"
call .venv\Scripts\activate.bat
python dashboard/app.py
pause
