@echo off
chcp 65001 > nul
title PCBBR - Catalog Bot

echo.
echo ========================================
echo    PCBBR - Catalog Bot
echo ========================================
echo.

REM Ir para o diretório do script
cd /d "%~dp0"

REM Verificar se ambiente virtual existe
if not exist ".venv" (
    echo [ERRO] Ambiente virtual não encontrado!
    echo Execute setup.bat primeiro para configurar o projeto.
    pause
    exit /b 1
)

REM Ativar ambiente virtual
call .venv\Scripts\activate.bat

echo [*] Iniciando catalogação...
echo.
echo Exemplos de uso:
echo   python catalog_bot.py --category "CPU"
echo   python catalog_bot.py --category "CPU" --store kabum
echo   python catalog_bot.py --category "Placa de Vídeo"
echo.

REM Se argumentos foram passados, usar eles
if "%~1"=="" (
    REM Sem argumentos, catalogar CPUs de todas as lojas
    echo [*] Executando: python catalog_bot.py --category "CPU"
    python catalog_bot.py --category "CPU"
) else (
    REM Com argumentos, passar todos
    python catalog_bot.py %*
)

echo.
echo ========================================
echo    Catalogação Concluída
echo ========================================
echo.
pause
