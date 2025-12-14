from pypdf import PdfReader
import sys

try:
    reader = PdfReader('/app/temp_analysis.pdf')
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n\n"
    
    with open('/app/pdf_content.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Extraction complete.")
except Exception as e:
    print(f"Error: {e}")
