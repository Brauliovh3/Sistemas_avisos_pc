@echo off
REM ===================================================
REM    🚀 INICIADOR UNIVERSAL DEL SISTEMA DE AVISOS
REM ===================================================

echo ===================================================
echo    🚀 SISTEMA DE AVISOS - MENU PRINCIPAL
echo ===================================================
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

echo Directorio actual: %CD%
echo.
echo Selecciona una opcion:
echo.
echo [1]   SISTEMA COMPLETO UNIFICADO (TODO EN UNO) ⭐
echo [2] ❌  Salir
echo.
echo RECOMENDADO: Opcion [1] incluye TODAS las funcionalidades
echo (Servidor, Panel de Envio, Administrador, Centro de Control)
echo.

set /p opcion="Ingresa tu opcion (1-2): "

if "%opcion%"=="1" goto unificado
if "%opcion%"=="2" goto salir

echo Opcion invalida. Presiona cualquier tecla para intentar de nuevo.
pause >nul
cls
goto menu

:unificado
cls
echo ===================================================
echo    🚀 INICIANDO SISTEMA COMPLETO UNIFICADO
echo ===================================================
echo.
echo TODO EN UNA SOLA VENTANA:
echo - Servidor integrado
echo - Panel de envio
echo - Administrador de PCs
echo - Centro de control
echo - Configuracion
echo.
python "src\sistema_unificado.py"
goto fin

:salir
echo.
echo Gracias por usar el Sistema de Avisos!
echo.
timeout /t 2 >nul
exit

:fin
echo.
echo ===================================================
echo    Aplicacion cerrada
echo ===================================================
echo.
set /p continuar="¿Volver al menu principal? (s/n): "
if /i "%continuar%"=="s" (
    cls
    goto menu
) else (
    goto salir
)

:inicio
cls

:menu
echo ===================================================
echo    🚀 SISTEMA DE AVISOS - MENU PRINCIPAL
echo ===================================================
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

echo Directorio actual: %CD%
echo.
echo Selecciona una opcion:
echo.
echo [1] 🖥️  Iniciar SERVIDOR (recibir avisos)
echo [2] 📱  Iniciar PANEL DE CONTROL (enviar avisos) 
echo [3] 🏢  Iniciar ADMINISTRADOR (multiple PCs)
echo [4] 📞  Iniciar CLIENTE SIMPLE
echo [5] ❌  Salir
echo.

set /p opcion="Ingresa tu opcion (1-5): "