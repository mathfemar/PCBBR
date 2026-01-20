@echo off
echo ================================================
echo        Iniciando PCBBR Backend (API)
echo ================================================
echo.
cd /d "%~dp0"
call .venv\Scripts\activate.bat
echo Rodando como modulo para garantir imports corretos...
python -m backend.main
pause
