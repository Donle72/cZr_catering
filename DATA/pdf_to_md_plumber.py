#!/usr/bin/env python3
"""
PDF to Markdown Converter using pdfplumber
Convierte todos los archivos PDF de una carpeta a formato Markdown
"""

import os
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("❌ pdfplumber no está instalado. Instalando...")
    import subprocess
    subprocess.check_call(["pip", "install", "pdfplumber"])
    import pdfplumber


def pdf_to_markdown_plumber(pdf_path: Path) -> str:
    """
    Extrae el texto de un PDF usando pdfplumber
    
    Args:
        pdf_path: Ruta al archivo PDF
        
    Returns:
        Texto en formato Markdown
    """
    try:
        # Usar el nombre del archivo como título
        title = pdf_path.stem
        markdown_content = f"# {title}\n\n"
        
        # Abrir PDF con pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # Extraer texto preservando layout
                text = page.extract_text()
                if text and text.strip():
                    markdown_content += text + "\n\n"
        
        return markdown_content
    
    except Exception as e:
        print(f"❌ Error procesando {pdf_path.name}: {e}")
        return None


def convert_pdfs_to_markdown(input_folder: str, output_folder: str):
    """
    Convierte todos los PDFs de una carpeta a Markdown
    
    Args:
        input_folder: Carpeta con los PDFs
        output_folder: Carpeta donde guardar los MD
    """
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    
    # Validar carpeta de entrada
    if not input_path.exists():
        print(f"❌ La carpeta de entrada no existe: {input_folder}")
        return
    
    # Crear carpeta de salida si no existe
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Buscar todos los PDFs
    pdf_files = list(input_path.glob("*.pdf"))
    
    if not pdf_files:
        print(f"⚠️  No se encontraron archivos PDF en: {input_folder}")
        return
    
    print(f"\n📄 Encontrados {len(pdf_files)} archivos PDF")
    print(f"📂 Carpeta de entrada: {input_path}")
    print(f"📁 Carpeta de salida: {output_path}\n")
    
    # Procesar cada PDF
    converted = 0
    failed = 0
    
    for pdf_file in pdf_files:
        print(f"🔄 Procesando: {pdf_file.name}...", end=" ")
        
        # Convertir a Markdown
        markdown_content = pdf_to_markdown_plumber(pdf_file)
        
        if markdown_content:
            # Guardar archivo MD
            output_file = output_path / f"{pdf_file.stem}.md"
            output_file.write_text(markdown_content, encoding='utf-8')
            print(f"✅ Guardado como: {output_file.name}")
            converted += 1
        else:
            failed += 1
    
    # Resumen
    print(f"\n{'='*60}")
    print(f"✅ Convertidos exitosamente: {converted}")
    if failed > 0:
        print(f"❌ Fallidos: {failed}")
    print(f"{'='*60}\n")


def main():
    """Función principal con interfaz interactiva o por argumentos"""
    import sys
    
    # Si se pasan argumentos, usar modo no-interactivo
    if len(sys.argv) >= 2:
        input_folder = sys.argv[1]
        output_folder = sys.argv[2] if len(sys.argv) >= 3 else input_folder
        
        print("=" * 60)
        print("📄 CONVERSOR DE PDF A MARKDOWN (pdfplumber)")
        print("=" * 60)
        
        convert_pdfs_to_markdown(input_folder, output_folder)
        print("\n✨ Proceso completado!")
        return
    
    # Modo interactivo
    print("=" * 60)
    print("📄 CONVERSOR DE PDF A MARKDOWN (pdfplumber)")
    print("=" * 60)
    
    # Solicitar carpeta de entrada
    print("\n📂 Ingresa la ruta de la carpeta con los PDFs:")
    input_folder = input("   > ").strip().strip('"')
    
    if not input_folder:
        print("❌ Debes ingresar una carpeta de entrada")
        return
    
    # Solicitar carpeta de salida
    print("\n📁 Ingresa la ruta donde guardar los archivos MD:")
    print("   (Presiona Enter para usar la misma carpeta de entrada)")
    output_folder = input("   > ").strip().strip('"')
    
    if not output_folder:
        output_folder = input_folder
    
    # Ejecutar conversión
    convert_pdfs_to_markdown(input_folder, output_folder)
    
    print("\n✨ Proceso completado!")
    input("\nPresiona Enter para salir...")


if __name__ == "__main__":
    main()
