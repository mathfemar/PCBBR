@echo off
chcp 65001 > nul
title PCBBR - Setup Inicial

echo.
echo ========================================
echo    PCBBR - Configuração Inicial
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python não encontrado!
    echo.
    echo Por favor, instale o Python 3.10+ de: https://www.python.org/downloads/
    echo Certifique-se de marcar "Add Python to PATH" durante a instalação.
    echo.
    pause
    exit /b 1
)

echo [OK] Python encontrado
python --version
echo.

REM Verificar versão do Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Versão detectada: %PYTHON_VERSION%
echo.

REM Criar ambiente virtual se não existir
if not exist ".venv" (
    echo [*] Criando ambiente virtual...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERRO] Falha ao criar ambiente virtual
        pause
        exit /b 1
    )
    echo [OK] Ambiente virtual criado
) else (
    echo [OK] Ambiente virtual já existe
)
echo.

REM Ativar ambiente virtual
echo [*] Ativando ambiente virtual...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao ativar ambiente virtual
    pause
    exit /b 1
)
echo [OK] Ambiente virtual ativado
echo.

REM Atualizar pip
echo [*] Atualizando pip...
python -m pip install --upgrade pip --quiet
echo [OK] pip atualizado
echo.

REM Instalar dependências do backend
echo [*] Instalando dependências do backend...
pip install -r backend\requirements.txt
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao instalar dependências do backend
    pause
    exit /b 1
)
echo [OK] Dependências do backend instaladas
echo.

REM Instalar dependências da raiz (catalog_bot)
echo [*] Instalando dependências da raiz...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao instalar dependências da raiz
    pause
    exit /b 1
)
echo [OK] Dependências da raiz instaladas
echo.

REM Verificar se banco de dados existe
if not exist "database" (
    echo [*] Criando diretório do banco de dados...
    mkdir database
)

REM Criar diretório de logs se não existir
if not exist "logs" (
    echo [*] Criando diretório de logs...
    mkdir logs
)

echo.
echo ========================================
echo    Configuração Concluída!
echo ========================================
echo.
echo O projeto está pronto para uso.
echo.
echo Comandos disponíveis:
echo   - start_api.bat       : Inicia apenas a API
echo   - catalog_bot.py      : Cataloga produtos das lojas
echo   - run_catalog.bat     : Atalho para catalogar
echo.
echo Para iniciar a API agora, execute: start_api.bat
echo.
pause
