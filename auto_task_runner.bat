@echo off
setlocal enabledelayedexpansion

REM === CONFIGURACION ===
REM Ajustado al path real del usuario d:\code\...
set PROJECT_ROOT=d:\code\cZr_CosteoCatering
set BACKEND=%PROJECT_ROOT%\backend
set VENV=%BACKEND%\venv
set PYTHON=%VENV%\Scripts\python.exe
set GIT_BIN=D:\code\git\bin\git.exe

REM === LOG ===
set LOGFILE=%PROJECT_ROOT%\auto_run_logistics.log
echo START %DATE% %TIME% > "%LOGFILE%"

echo [INFO] Iniciando script de finalizacion de Logistica...
echo [INFO] Logs detallados en: %LOGFILE%

REM === DEPENDENCIAS (Asegurar entorno) ===
echo [STEP 1/4] Verificando dependencias...
"%PYTHON%" -m pip install python-dotenv >> "%LOGFILE%" 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Fallo instalando dependencias. Ver log.
    exit /b 1
)

REM === TESTS ===
echo [STEP 2/4] Ejecutando Tests de Logistica...
"%PYTHON%" "%BACKEND%\tests\manual_test_logistics.py" >> "%LOGFILE%" 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Test de Logistica FALLO. Ver log para detalles.
    echo [DEBUG] Ultimas lineas del log:
    type "%LOGFILE%"
    exit /b 1
) else (
    echo [SUCCESS] Test de Logistica PASO correctamente.
)

REM === GIT COMMIT & PUSH ===
echo [STEP 3/4] Guardando cambios en Git (All-in-one)...
cd /d "%PROJECT_ROOT%"
"%GIT_BIN%" add . >> "%LOGFILE%" 2>&1
"%GIT_BIN%" commit -m "Feat: Completed Logistics Module (Assets, EventAssets, API, Tests)" >> "%LOGFILE%" 2>&1
"%GIT_BIN%" push >> "%LOGFILE%" 2>&1

if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Git push pudo haber fallado o no habia cambios. Revisa el log.
) else (
    echo [SUCCESS] Cambios subidos al repositorio.
)

REM === CLEANUP / STATUS ===
echo [STEP 4/4] Finalizando...
echo END %DATE% %TIME% >> "%LOGFILE%"
echo.
echo [DONE] Proceso completado exitosamente.
exit /b 0
