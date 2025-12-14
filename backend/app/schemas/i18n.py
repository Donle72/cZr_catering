from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class LanguageBase(BaseModel):
    code: str
    name: str
    is_active: bool = True
    is_default: bool = False

class LanguageCreate(LanguageBase):
    pass

class LanguageResponse(LanguageBase):
    created_at: Optional[str] = None
    
    class Config:
        from_attributes = True

class TranslationBase(BaseModel):
    language_code: str
    entity_type: str
    entity_id: str
    field_name: str
    translation_value: str

class TranslationCreate(TranslationBase):
    pass

class TranslationResponse(TranslationBase):
    id: int
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True

class DictionaryResponse(BaseModel):
    """
    Key-Value pair response for UI translations
    e.g. {"btn.save": "Guardar", "menu.home": "Inicio"}
    """
    language_code: str
    translations: Dict[str, str]
