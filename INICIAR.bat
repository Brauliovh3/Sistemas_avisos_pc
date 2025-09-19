@echo off
REM ===================================================
REM    🚀 INICIADOR UNIVERSAL DEL SISTEMA DE AVISOS
REM ===================================================

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
echo [1]   SISTEMA UNIFICADO (Sin Login) ⭐
echo [2]   SISTEMA CON LOGIN (Admin/Cliente) 🔐
echo [3] ❌  Salir
echo.
echo OPCIONES DISPONIBLES:
echo [1] Sistema completo sin restricciones
echo [2] Sistema con roles: Admin (completo) / Cliente (limitado)
echo.

set /p opcion="Ingresa tu opcion (1-3): "

if "%opcion%"=="1" goto unificado
if "%opcion%"=="2" goto login
if "%opcion%"=="3" goto salir

echo Opcion invalida. Presiona cualquier tecla para intentar de nuevo.
pause >nul
cls
goto menu

:unificado
cls
echo ===================================================
echo    🚀 INICIANDO SISTEMA UNIFICADO
echo ===================================================
echo.
echo TODO EN UNA SOLA VENTANA (SIN LOGIN):
echo - Servidor integrado
echo - Panel de envio completo
echo - Administrador de PCs
echo - Centro de control
echo - Configuracion avanzada
echo.
python "src\sistema_unificado.py"
goto fin

:login
cls
echo ===================================================
echo    🔐 INICIANDO SISTEMA CON LOGIN
echo ===================================================
echo.
echo SISTEMA CON ROLES Y PERMISOS:
echo - Login requerido
echo - Admin: Acceso completo
echo - Cliente: Solo 3 mensajes (salida, comer, problema)
echo - Gestion de usuarios e IPs con nombres
echo.
echo USUARIOS POR DEFECTO:
echo Admin: usuario='admin' / pass='admin123'
echo Cliente: usuario='cliente' / pass='cliente123'
echo.
python "src\sistema_con_login.py"
goto fin

:salir
cls
echo ===================================================
echo    👋 GRACIAS POR USAR EL SISTEMA DE AVISOS
echo ===================================================
echo.
pause
exit

:fin
echo.
echo ===================================================
echo    ✅ SISTEMA FINALIZADO
echo ===================================================
echo.
echo Presiona cualquier tecla para volver al menu...
pause >nul
cls
goto menu

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