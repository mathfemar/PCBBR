@echo off
chcp 65001 > nul
title PCBBR - Verificação do Sistema

echo.
echo ========================================
echo    PCBBR - Verificação do Sistema
echo ========================================
echo.

set ERROR_COUNT=0

REM Verificar Python
echo [*] Verificando Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python instalado
    python --version
) else (
    echo [ERRO] Python não encontrado
    echo        Instale de: https://www.python.org/downloads/
    set /a ERROR_COUNT+=1
)
echo.

REM Verificar pip
echo [*] Verificando pip...
python -m pip --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] pip instalado
    python -m pip --version
) else (
    echo [ERRO] pip não encontrado
    set /a ERROR_COUNT+=1
)
echo.

REM Verificar ambiente virtual
echo [*] Verificando ambiente virtual...
if exist ".venv" (
    echo [OK] Ambiente virtual existe
) else (
    echo [AVISO] Ambiente virtual não encontrado
    echo          Execute setup.bat para criar
)
echo.

REM Verificar estrutura de diretórios
echo [*] Verificando estrutura de diretórios...
if exist "backend" (
    echo [OK] Pasta backend/ existe
) else (
    echo [ERRO] Pasta backend/ não encontrada
    set /a ERROR_COUNT+=1
)

if exist "backend\main.py" (
    echo [OK] backend/main.py existe
) else (
    echo [ERRO] backend/main.py não encontrado
    set /a ERROR_COUNT+=1
)

if exist "catalog_bot.py" (
    echo [OK] catalog_bot.py existe
) else (
    echo [ERRO] catalog_bot.py não encontrado
    set /a ERROR_COUNT+=1
)
echo.

REM Verificar dependências (se ambiente virtual existe)
if exist ".venv" (
    echo [*] Verificando dependências instaladas...
    call .venv\Scripts\activate.bat
    
    python -c "import fastapi" >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] fastapi instalado
    ) else (
        echo [AVISO] fastapi não instalado
        echo          Execute setup.bat para instalar
    )
    
    python -c "import sqlmodel" >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] sqlmodel instalado
    ) else (
        echo [AVISO] sqlmodel não instalado
        echo          Execute setup.bat para instalar
    )
    
    python -c "import curl_cffi" >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] curl_cffi instalado
    ) else (
        echo [AVISO] curl_cffi não instalado
        echo          Execute setup.bat para instalar
    )
    echo.
)

REM Verificar portas
echo [*] Verificando porta 8000...
netstat -ano | findstr ":8000" >nul 2>&1
if %errorlevel% equ 0 (
    echo [AVISO] Porta 8000 já está em uso
    echo          A API pode não conseguir iniciar
) else (
    echo [OK] Porta 8000 disponível
)
echo.

REM Verificar espaço em disco
echo [*] Verificando espaço em disco...
for /f "tokens=3" %%a in ('dir /-c ^| findstr "bytes free"') do set FREE_SPACE=%%a
echo [OK] Espaço livre: %FREE_SPACE% bytes
echo.

REM Resumo
echo ========================================
echo    Resumo da Verificação
echo ========================================
if %ERROR_COUNT% equ 0 (
    echo [OK] Sistema pronto para uso!
    echo.
    echo Próximos passos:
    echo   1. Se ambiente virtual não existe: setup.bat
    echo   2. Para iniciar API: start_api.bat
    echo   3. Para catalogar produtos: run_catalog.bat
) else (
    echo [ERRO] %ERROR_COUNT% erro(s) encontrado(s)
    echo.
    echo Execute setup.bat para configurar o projeto
    echo Consulte TROUBLESHOOTING.md para ajuda
)
echo.
pause
