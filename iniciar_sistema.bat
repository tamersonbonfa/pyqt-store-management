@echo off
title Iniciando Sistema - %CD%
cls

echo ======================================================
echo           INICIALIZADOR DO SISTEMA
echo ======================================================

:: 1. Verifica se a pasta do ambiente virtual existe
if not exist .venv (
    echo [AVISO] Ambiente virtual nao encontrado. Criando...
    python -m venv .venv
)

:: 2. Ativa o ambiente virtual e garante que as dependencias estao ok
echo [INFO] Ativando ambiente e verificando dependencias...
call .venv\Scripts\activate

:: 3. Instala/Atualiza dependencias (opcional, remova 'rem' se quiser automatizar sempre)
rem pip install -r requirements.txt

:: 4. Executa o sistema
echo [OK] Iniciando aplicacao...
python main.py

:: 5. Mantem o prompt aberto caso ocorra algum erro no Python
if %errorlevel% neq 0 (
    echo.
    echo [ERRO] O sistema fechou inesperadamente. Verifique as mensagens acima.
    pause
)