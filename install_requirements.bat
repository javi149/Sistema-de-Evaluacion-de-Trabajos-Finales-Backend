@echo off
echo ==========================================
echo    Instalador de Requerimientos del Proyecto
echo ==========================================
echo.

:: Verificar si Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no se encuentra instalado o no esta en el PATH.
    echo Por favor instala Python antes de continuar.
    pause
    exit /b
)

:: Crear entorno virtual si no existe
if not exist "venv" (
    echo [INFO] Creando entorno virtual 'venv'...
    python -m venv venv
) else (
    echo [INFO] Entorno virtual 'venv' ya existe.
)

:: Activar entorno virtual
echo [INFO] Activando entorno virtual...
call venv\Scripts\activate

:: Actualizar pip
echo [INFO] Actualizando pip...
python -m pip install --upgrade pip

:: Instalar dependencias
if exist "requirements.txt" (
    echo [INFO] Instalando dependencias desde requirements.txt...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Hubo un problema instalando las dependencias.
        pause
        exit /b
    )
) else (
    echo [WARN] No se encontro el archivo requirements.txt.
)

echo.
echo ==========================================
echo    Instalacion completada exitosamente
echo ==========================================
pause
