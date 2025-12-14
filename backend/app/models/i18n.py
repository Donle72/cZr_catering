from sqlalchemy import Column, Integer, String, Boolean, Text, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from datetime import datetime

class Language(Base):
    """
    Supported languages in the system
    """
    __tablename__ = "languages"

    code = Column(String(5), primary_key=True)  # e.g., 'es', 'en', 'pt-BR'
    name = Column(String(50), nullable=False)   # e.g., 'Español', 'English'
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)
    
    created_at = Column(String, default=lambda: datetime.now().isoformat())

class Translation(Base):
    """
    Universal translation table (Polymorphic-ish)
    Can store translations for:
    1. UI Elements (entity_type='UI', entity_id='btn_save')
    2. Database Entities (entity_type='ingredients', entity_id='15')
    """
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, index=True)
    
    language_code = Column(String(5), nullable=False) # FK manually managed or simple string
    
    # Polymorphic addressing
    entity_type = Column(String(50), nullable=False, index=True) # 'UI', 'ingredients', 'recipes'
    entity_id = Column(String(100), nullable=False, index=True)  # 'btn_save', '1', 'UUID'
    
    # The actual content
    field_name = Column(String(50), nullable=False) # 'text', 'name', 'description'
    translation_value = Column(Text, nullable=False)
    
    updated_at = Column(String, default=lambda: datetime.now().isoformat())

    # Composite Index for fast lookups
    __table_args__ = (
        Index('ix_translations_lookup', 'language_code', 'entity_type', 'entity_id', 'field_name', unique=True),
    )
