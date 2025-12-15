from sqlalchemy import create_engine, text
import os
import sys
from dotenv import load_dotenv

# Ensure we can import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load env vars explicitly
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(env_path)

from app.core.config import settings

def migrate_scaling_column():
    print("Migrating: Adding 'scaling_type' column to ingredients table...")
    
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        try:
            # Check if column exists (PostgreSQL friendly)
            # Using information_schema standard
            result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='ingredients' AND column_name='scaling_type'"))
            exists = result.fetchone()
            
            if not exists:
                print("Adding scaling_type column...")
                conn.execute(text("ALTER TABLE ingredients ADD COLUMN scaling_type VARCHAR(50) DEFAULT 'linear'"))
                conn.commit()
                print("Migration successful: Added scaling_type column.")
            else:
                print("Column 'scaling_type' already exists. Skipping.")
                
        except Exception as e:
            print(f"Migration failed: {e}")
            raise e

if __name__ == "__main__":
    migrate_scaling_column()
