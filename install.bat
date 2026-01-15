@echo off
:: ========================================
::   PS2 Launcher v2.0 - Instalador
:: ========================================

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
echo   PS2 Launcher v2.0 - Instalador
echo ========================================
echo.

:: Verificar Python
echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python no esta instalado.
    echo Descarga Python desde: https://python.org
    echo Marca "Add Python to PATH" durante la instalacion.
    pause
    exit /b 1
)
echo       OK

:: Actualizar pip
echo [2/5] Actualizando pip...
python -m pip install --upgrade pip >nul 2>&1
echo       OK

:: Instalar dependencias
echo [3/5] Instalando dependencias...
pip install customtkinter pygame-ce pillow >nul 2>&1
echo       OK

:: Crear carpetas
echo [4/5] Creando carpetas...
if not exist "roms" mkdir roms
if not exist "logs" mkdir logs
if not exist "config" mkdir config
if not exist "bios" mkdir bios
echo       OK

:: Extraer BIOS
echo [5/5] Extrayendo BIOS...
if exist "bios.rar" (
    :: Intentar con PowerShell (Windows 10+)
    powershell -Command "try { Add-Type -AssemblyName System.IO.Compression.FileSystem } catch {}; if (Test-Path 'bios.zip') { Expand-Archive -Path 'bios.zip' -DestinationPath 'bios' -Force }" >nul 2>&1
    
    :: Si hay bios.rar, necesita WinRAR o 7-Zip
    if exist "C:\Program Files\WinRAR\WinRAR.exe" (
        "C:\Program Files\WinRAR\WinRAR.exe" x -y "bios.rar" "bios\" >nul 2>&1
        echo       BIOS extraida con WinRAR
    ) else if exist "C:\Program Files\7-Zip\7z.exe" (
        "C:\Program Files\7-Zip\7z.exe" x -y "bios.rar" -o"bios" >nul 2>&1
        echo       BIOS extraida con 7-Zip
    ) else (
        echo       AVISO: Instala WinRAR o 7-Zip para extraer bios.rar
        echo       O extrae manualmente bios.rar a la carpeta "bios"
    )
) else if exist "bios.zip" (
    powershell -Command "Expand-Archive -Path 'bios.zip' -DestinationPath 'bios' -Force" >nul 2>&1
    echo       BIOS extraida
) else (
    echo       No se encontro bios.rar ni bios.zip
)

echo.
echo ========================================
echo   Instalacion completada!
echo ========================================
echo.
echo   Siguiente paso: Configura la BIOS en PCSX2
echo   (ver README.md para instrucciones)
echo.

set /p respuesta="Iniciar PS2 Launcher ahora? (s/n): "
if /i "%respuesta%"=="s" (
    start "" pythonw launcher/main.py
)

pause
