import logging
import os
from sqlalchemy import create_engine, text
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate():
    """
    Manual migration to add i18n tables
    """
    try:
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as connection:
            logger.info("Checking if languages table exists...")
            
            # Check if tables exist
            check_lang = text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'languages');")
            lang_exists = connection.execute(check_lang).scalar()
            
            if not lang_exists:
                logger.info("Creating languages table...")
                create_lang = text("""
                    CREATE TABLE languages (
                        code VARCHAR(5) PRIMARY KEY,
                        name VARCHAR(50) NOT NULL,
                        is_active BOOLEAN DEFAULT TRUE,
                        is_default BOOLEAN DEFAULT FALSE,
                        created_at VARCHAR
                    );
                    -- Insert default Spanish
                    INSERT INTO languages (code, name, is_active, is_default) VALUES ('es', 'Español', TRUE, TRUE);
                    INSERT INTO languages (code, name, is_active, is_default) VALUES ('en', 'English', TRUE, FALSE);
                """)
                connection.execute(create_lang)
                logger.info("Languages table created and seeded.")
            
            check_trans = text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'translations');")
            trans_exists = connection.execute(check_trans).scalar()
            
            if not trans_exists:
                logger.info("Creating translations table...")
                create_trans = text("""
                    CREATE TABLE translations (
                        id SERIAL PRIMARY KEY,
                        language_code VARCHAR(5) NOT NULL,
                        entity_type VARCHAR(50) NOT NULL,
                        entity_id VARCHAR(100) NOT NULL,
                        field_name VARCHAR(50) NOT NULL,
                        translation_value TEXT NOT NULL,
                        updated_at VARCHAR
                    );
                    
                    CREATE INDEX ix_translations_lookup ON translations (language_code, entity_type, entity_id, field_name);
                    CREATE INDEX ix_translations_entity ON translations (entity_type, entity_id);
                """)
                connection.execute(create_trans)
                logger.info("Translations table created.")
                
            connection.commit()
            logger.info("Migration complete.")
                
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise

if __name__ == "__main__":
    migrate()
