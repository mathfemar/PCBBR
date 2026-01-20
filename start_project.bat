@echo off
echo ================================================
echo        PCBBR - Iniciando Projeto Completo
echo ================================================
echo.

REM Inicia o Backend (FastAPI) em uma nova janela
echo [1/2] Iniciando Backend (FastAPI)...
start "PCBBR - Backend API" cmd /k "cd /d "%~dp0backend" && python main.py"

REM Aguarda 3 segundos para o backend inicializar
timeout /t 3 /nobreak >nul

REM Inicia o Frontend (Flutter) em uma nova janela via PowerShell (para ter acesso às variáveis de ambiente atualizadas)
echo [2/2] Iniciando Frontend (Flutter)...
start "PCBBR - Frontend Flutter" powershell -NoExit -Command "cd '%~dp0frontend'; $env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User'); flutter run"

echo.
echo ================================================
echo   Projeto iniciado com sucesso!
echo   - Backend: http://localhost:8000/docs
echo   - Frontend: Rodando no dispositivo selecionado
echo ================================================
echo.
pause
