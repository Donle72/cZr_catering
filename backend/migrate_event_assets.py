from sqlalchemy import create_engine, text
import os
import sys
from dotenv import load_dotenv

# Ensure we can import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load env vars
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(env_path)

from app.core.config import settings

def migrate_event_assets():
    print("Migrating: Creating 'event_assets' table...")
    
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        try:
            # Check existence
            result = conn.execute(text("SELECT to_regclass('public.event_assets')"))
            exists = result.fetchone()[0]
            
            if not exists:
                print("Creating event_assets table...")
                conn.execute(text("""
                    CREATE TABLE event_assets (
                        id SERIAL PRIMARY KEY,
                        event_id INTEGER NOT NULL,
                        asset_id INTEGER NOT NULL,
                        quantity INTEGER DEFAULT 1 NOT NULL,
                        CONSTRAINT fk_event FOREIGN KEY(event_id) REFERENCES events(id) ON DELETE CASCADE,
                        CONSTRAINT fk_asset FOREIGN KEY(asset_id) REFERENCES assets(id) ON DELETE CASCADE
                    );
                    CREATE INDEX ix_event_assets_event_id ON event_assets (event_id);
                """))
                conn.commit()
                print("Migration successful: Created event_assets table.")
            else:
                print("Table 'event_assets' already exists. Skipping.")
                
        except Exception as e:
            print(f"Migration failed: {e}")
            raise e

if __name__ == "__main__":
    migrate_event_assets()
