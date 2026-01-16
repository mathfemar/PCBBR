@echo off
chcp 65001 > nul
title PCBBR - API Server

echo.
echo ========================================
echo    PCBBR - Iniciando API
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python não encontrado!
    echo Execute setup.bat primeiro para configurar o projeto.
    pause
    exit /b 1
)

REM Verificar se ambiente virtual existe
if not exist ".venv" (
    echo [AVISO] Ambiente virtual não encontrado
    echo Execute setup.bat primeiro para configurar o projeto.
    pause
    exit /b 1
)

REM Ativar ambiente virtual
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao ativar ambiente virtual
    echo Execute setup.bat primeiro para configurar o projeto.
    pause
    exit /b 1
)

echo [OK] Ambiente virtual ativado
echo.

REM Verificar se dependências estão instaladas
python -c "import fastapi" >nul 2>&1
if %errorlevel% neq 0 (
    echo [AVISO] Dependências não encontradas. Instalando...
    pip install -r backend\requirements.txt --quiet
    echo [OK] Dependências instaladas
    echo.
)

REM Criar diretórios necessários
if not exist "database" mkdir database
if not exist "logs" mkdir logs

echo [*] Iniciando servidor FastAPI...
echo [*] API estará disponível em: http://localhost:8000
echo [*] Documentação: http://localhost:8000/docs
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

cd backend
python main.py
