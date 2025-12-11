@echo off
echo ========================================
echo   cZr Catering - Inicio del Backend
echo ========================================
echo.

REM Verificar si el entorno virtual existe
if not exist "venv\" (
    echo Creando entorno virtual...
    py -m venv venv
)

echo Activando entorno virtual...
call venv\Scripts\activate

echo.
echo Instalando dependencias...
pip install --quiet --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo   Inicializando base de datos...
echo ========================================
py init_db.py

echo.
echo ========================================
echo   Iniciando servidor FastAPI...
echo ========================================
echo.
echo Backend corriendo en: http://localhost:8020
echo Documentacion API: http://localhost:8020/docs
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8020
