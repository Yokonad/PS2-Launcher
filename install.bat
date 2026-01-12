@echo off
:: Solicitar permisos de administrador
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo Solicitando permisos de administrador...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"

echo.
echo ========================================
echo   PS2 Launcher - Instalador
echo ========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado.
    echo Descarga Python desde: https://python.org
    pause
    exit /b 1
)

echo Python encontrado.
echo.
echo Instalando dependencias...
echo.

pip install customtkinter pygame-ce

echo.
echo ========================================
echo   Instalacion completada!
echo ========================================
echo.

set /p respuesta="Deseas iniciar el launcher ahora? (s/n): "
if /i "%respuesta%"=="s" (
    echo Iniciando PS2 Launcher...
    start "" pythonw launcher/main.py
)

echo.
echo Listo! Puedes cerrar esta ventana.
pause
