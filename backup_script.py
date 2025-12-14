import os
import zipfile
from datetime import datetime

def backup_project():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    base_dir = os.path.dirname(os.path.abspath(__file__))
    backup_dir = os.path.join(base_dir, 'backups')
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        
    zip_filename = os.path.join(backup_dir, f'backup_{timestamp}.zip')
    
    excludes = {
        'node_modules', 
        'venv', 
        '.git', 
        '.gemini', 
        '__pycache__', 
        'backups',
        'temp_backup',
        'dist',
        '.idea',
        '.vscode'
    }
    
    print(f"Creating backup: {zip_filename}")
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in excludes]
            
            for file in files:
                if file.endswith('.zip') or file == 'backup_script.py':
                    continue
                    
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, base_dir)
                
                try:
                    zipf.write(file_path, arcname)
                except Exception as e:
                    print(f"Skipping {arcname}: {e}")
                    
    print("Backup created successfully.")

if __name__ == '__main__':
    backup_project()
