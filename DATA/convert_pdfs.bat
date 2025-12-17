@echo off
echo ============================================================
echo PDF to Markdown Converter - Batch Script
echo ============================================================
echo.

REM Usar Python del contenedor Docker
echo Instalando pdfplumber en el contenedor...
docker-compose exec backend pip install -q pdfplumber

echo.
echo Copiando script al contenedor...
docker cp DATA\pdf_to_md_plumber.py czr_catering_backend:/tmp/converter.py

echo.
echo Creando carpeta de salida...
if not exist "DATA\md" mkdir "DATA\md"

echo.
echo Convirtiendo PDFs...
echo.

REM Copiar PDFs al contenedor
docker cp DATA\Modelo czr_catering_backend:/tmp/

REM Ejecutar conversión
docker-compose exec backend python /tmp/converter.py /tmp/Modelo /tmp/md

REM Copiar resultados de vuelta
docker cp czr_catering_backend:/tmp/md DATA\

echo.
echo ============================================================
echo Conversion completada! 
echo Archivos MD guardados en: DATA\md\
echo ============================================================
pause
