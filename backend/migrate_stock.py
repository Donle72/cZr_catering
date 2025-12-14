import sys
import os
from sqlalchemy import text

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine

def migrate():
    print("Checking for stock columns in ingredients table...")
    # Use engine.begin() which automatically handles commit/rollback
    with engine.begin() as connection:
        try:
            # Check if column exists
            # Note: This check might fail if transaction is aborted effectively, but let's try.
            # A safer way in raw SQL without extensive reflection:
            # Just try to add column and ignore specific duplicate column error, 
            # OR select from information_schema
            
            # Let's use information_schema for safety
            result = connection.execute(text(
                "SELECT column_name FROM information_schema.columns WHERE table_name='ingredients' AND column_name='stock_quantity'"
            ))
            if result.fetchone():
                print("Columns already exist. Skipping.")
                return

            print("Columns missing. Adding them...")
            connection.execute(text("ALTER TABLE ingredients ADD COLUMN stock_quantity FLOAT DEFAULT 0.0"))
            connection.execute(text("ALTER TABLE ingredients ADD COLUMN min_stock_threshold FLOAT DEFAULT 0.0"))
            print("Migration successful: Added stock_quantity and min_stock_threshold")
            
        except Exception as e:
            print(f"Migration failed: {e}")
            raise e

if __name__ == "__main__":
    migrate()
