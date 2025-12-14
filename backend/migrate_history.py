import logging
import os
from sqlalchemy import create_engine, text
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate():
    """
    Manual migration to add ingredient_price_history table
    """
    try:
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as connection:
            logger.info("Checking if ingredient_price_history table exists...")
            
            # Check if table exists
            check_table = text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE  table_schema = 'public'
                    AND    table_name   = 'ingredient_price_history'
                );
            """)
            result = connection.execute(check_table).scalar()
            
            if not result:
                logger.info("Table does not exist. Creating...")
                create_table = text("""
                    CREATE TABLE ingredient_price_history (
                        id SERIAL PRIMARY KEY,
                        ingredient_id INTEGER NOT NULL REFERENCES ingredients(id),
                        old_cost DOUBLE PRECISION NOT NULL,
                        new_cost DOUBLE PRECISION NOT NULL,
                        changed_by VARCHAR(100),
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );
                    
                    CREATE INDEX ix_ingredient_price_history_ingredient_id ON ingredient_price_history (ingredient_id);
                """)
                connection.execute(create_table)
                connection.commit()
                logger.info("Successfully created ingredient_price_history table.")
            else:
                logger.info("Table already exists. Skipping.")
                
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise

if __name__ == "__main__":
    migrate()
