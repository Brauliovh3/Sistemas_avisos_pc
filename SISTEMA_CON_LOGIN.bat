@echo off
title Sistema de Avisos con Login
color 0b
echo.
echo ========================================
echo    SISTEMA DE AVISOS CON LOGIN
echo ========================================
echo.
echo Iniciando sistema con autenticacion...
echo.

cd /d "%~dp0"

if exist "src\sistema_con_login.py" (
    python "src\sistema_con_login.py"
) else (
    echo ERROR: No se encuentra el archivo sistema_con_login.py
    echo Verifica que el archivo este en la carpeta src\
    pause
)

echo.
echo Sistema finalizado.
pause