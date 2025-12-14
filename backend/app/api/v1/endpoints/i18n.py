from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.i18n import Language
from app.schemas.i18n import LanguageCreate, LanguageResponse, TranslationCreate, TranslationResponse, DictionaryResponse
from app.services.translation_service import TranslationService

router = APIRouter()

@router.get("/languages/", response_model=List[LanguageResponse])
def get_languages(db: Session = Depends(get_db)):
    """List all supported languages"""
    return TranslationService.get_languages(db)

@router.get("/dictionary/{language_code}", response_model=DictionaryResponse)
def get_dictionary(language_code: str, db: Session = Depends(get_db)):
    """Get the full UI dictionary for a specific language"""
    translations = TranslationService.get_ui_dictionary(db, language_code)
    return {
        "language_code": language_code,
        "translations": translations
    }

@router.post("/translations/", response_model=TranslationResponse)
def upsert_translation(
    translation: TranslationCreate,
    db: Session = Depends(get_db)
):
    """Create or update a translation entry"""
    return TranslationService.set_translation(db, translation)

@router.post("/seed/")
def seed_translations(db: Session = Depends(get_db)):
    """Manually trigger seeding of initial data"""
    TranslationService.seed_initial_data(db)
    return {"message": "Seeded initial translations"}
