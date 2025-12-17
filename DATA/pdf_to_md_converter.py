#!/usr/bin/env python3
"""
PDF to Markdown Converter
Convierte todos los archivos PDF de una carpeta a formato Markdown
"""

import os
from pathlib import Path
from pypdf import PdfReader


def pdf_to_markdown(pdf_path: Path) -> str:
    """
    Extrae el texto de un PDF y lo formatea como Markdown
    
    Args:
        pdf_path: Ruta al archivo PDF
        
    Returns:
        Texto en formato Markdown
    """
    try:
        reader = PdfReader(pdf_path)
        
        # Extraer metadata
        metadata = reader.metadata
        title = metadata.get('/Title', pdf_path.stem) if metadata else pdf_path.stem
        
        # Construir contenido Markdown
        markdown_content = f"# {title}\n\n"
        
        # Extraer texto de todas las páginas
        full_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text.strip():
                full_text += text + "\n"
        
        # Intentar limpiar el texto si tiene muchas líneas cortas
        lines = full_text.split('\n')
        
        # Si hay muchas líneas muy cortas, probablemente está mal formateado
        short_lines = sum(1 for line in lines if len(line.strip()) < 50 and len(line.strip()) > 0)
        total_lines = len([l for l in lines if l.strip()])
        
        if total_lines > 0 and (short_lines / total_lines) > 0.7:
            # Intentar unir líneas
            cleaned_lines = []
            current_line = ""
            
            for line in lines:
                line = line.strip()
                if not line:
                    if current_line:
                        cleaned_lines.append(current_line)
                        current_line = ""
                    cleaned_lines.append("")
                elif line.endswith(('.', ':', '!', '?', '}', ']', ')')):
                    current_line += " " + line if current_line else line
                    cleaned_lines.append(current_line)
                    current_line = ""
                else:
                    current_line += " " + line if current_line else line
            
            if current_line:
                cleaned_lines.append(current_line)
            
            markdown_content += "\n".join(cleaned_lines)
        else:
            # El texto está bien formateado, usarlo tal cual
            markdown_content += full_text
        
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
        markdown_content = pdf_to_markdown(pdf_file)
        
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
        print("📄 CONVERSOR DE PDF A MARKDOWN")
        print("=" * 60)
        
        convert_pdfs_to_markdown(input_folder, output_folder)
        print("\n✨ Proceso completado!")
        return
    
    # Modo interactivo
    print("=" * 60)
    print("📄 CONVERSOR DE PDF A MARKDOWN")
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
