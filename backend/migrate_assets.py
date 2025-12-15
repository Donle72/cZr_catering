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

def migrate_assets_table():
    print("Migrating: Creating 'assets' table...")
    
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        try:
            # Check if table exists (PostgreSQL)
            result = conn.execute(text("SELECT to_regclass('public.assets')"))
            exists = result.fetchone()[0]
            
            if not exists:
                print("Creating assets table...")
                conn.execute(text("""
                    CREATE TABLE assets (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(200) NOT NULL,
                        category VARCHAR(100),
                        description TEXT,
                        total_quantity INTEGER DEFAULT 0 NOT NULL,
                        purchase_price FLOAT DEFAULT 0.0,
                        replacement_cost FLOAT DEFAULT 0.0,
                        state VARCHAR(50) DEFAULT 'available',
                        location VARCHAR(100),
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                    );
                    CREATE INDEX ix_assets_name ON assets (name);
                    CREATE INDEX ix_assets_category ON assets (category);
                """))
                conn.commit()
                print("Migration successful: Created assets table.")
            else:
                print("Table 'assets' already exists. Skipping.")
                
        except Exception as e:
            print(f"Migration failed: {e}")
            raise e

if __name__ == "__main__":
    migrate_assets_table()
