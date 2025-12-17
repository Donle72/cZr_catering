# 📄 Conversor de PDF a Markdown

## 🚀 Instalación

1. Instalar la dependencia:

```bash
pip install pypdf
```

O usando el archivo de requirements:

```bash
pip install -r requirements_converter.txt
```

## 📖 Uso

### Opción 1: Modo Interactivo (Recomendado)

Ejecuta el script:

```bash
python pdf_to_md_converter.py
```

El programa te pedirá:

1. **Carpeta de entrada**: Donde están los PDFs
2. **Carpeta de salida**: Donde guardar los MD (opcional, usa la misma si no especificas)

### Opción 2: Desde Código

```python
from pdf_to_md_converter import convert_pdfs_to_markdown

convert_pdfs_to_markdown(
    input_folder="D:/code/cZr_CosteoCatering/DATA/Modelo",
    output_folder="D:/code/cZr_CosteoCatering/DATA/md"
)
```

## 📋 Ejemplo

```
📄 CONVERSOR DE PDF A MARKDOWN
============================================================

📂 Ingresa la ruta de la carpeta con los PDFs:
   > D:\code\cZr_CosteoCatering\DATA\Modelo

📁 Ingresa la ruta donde guardar los archivos MD:
   (Presiona Enter para usar la misma carpeta de entrada)
   > D:\code\cZr_CosteoCatering\DATA\md

📄 Encontrados 12 archivos PDF
📂 Carpeta de entrada: D:\code\cZr_CosteoCatering\DATA\Modelo
📁 Carpeta de salida: D:\code\cZr_CosteoCatering\DATA\md

🔄 Procesando: Arquitectura.pdf... ✅ Guardado como: Arquitectura.md
🔄 Procesando: Documentación.pdf... ✅ Guardado como: Documentación.md
...

============================================================
✅ Convertidos exitosamente: 12
============================================================
```

## ⚙️ Características

- ✅ Convierte múltiples PDFs automáticamente
- ✅ Preserva el título del documento
- ✅ Maneja errores gracefully
- ✅ Muestra progreso en tiempo real
- ✅ Crea carpeta de salida si no existe
- ✅ Codificación UTF-8 para caracteres especiales

## 🔧 Troubleshooting

**Error: "pypdf not found"**

```bash
pip install pypdf
```

**Error: "Carpeta no existe"**

- Verifica que la ruta sea correcta
- Usa rutas absolutas (ej: `D:\carpeta\subcarpeta`)
- Puedes pegar rutas con comillas, el script las limpia automáticamente
