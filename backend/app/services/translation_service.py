from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from app.models.i18n import Language, Translation
from app.schemas.i18n import TranslationCreate

class TranslationService:
    @staticmethod
    def get_languages(db: Session, active_only: bool = True) -> List[Language]:
        query = db.query(Language)
        if active_only:
            query = query.filter(Language.is_active == True)
        return query.all()

    @staticmethod
    def get_ui_dictionary(db: Session, language_code: str) -> Dict[str, str]:
        """
        Fetch all UI translations for a language and flatten them into a key-value pair
        Key = entity_id (e.g., 'btn.save')
        Value = translation_value
        """
        translations = db.query(Translation).filter(
            Translation.language_code == language_code,
            Translation.entity_type == 'UI'
        ).all()
        
        return {t.entity_id: t.translation_value for t in translations}

    @staticmethod
    def set_translation(db: Session, translation: TranslationCreate) -> Translation:
        """
        Create or Update a translation
        """
        existing = db.query(Translation).filter(
            Translation.language_code == translation.language_code,
            Translation.entity_type == translation.entity_type,
            Translation.entity_id == translation.entity_id,
            Translation.field_name == translation.field_name
        ).first()

        if existing:
            existing.translation_value = translation.translation_value
            db.commit()
            db.refresh(existing)
            return existing
        else:
            new_trans = Translation(
                language_code=translation.language_code,
                entity_type=translation.entity_type,
                entity_id=translation.entity_id,
                field_name=translation.field_name,
                translation_value=translation.translation_value
            )
            db.add(new_trans)
            db.commit()
            db.refresh(new_trans)
            return new_trans

    @staticmethod
    def seed_initial_data(db: Session):
        """
        Seed basic Spanish translations to prevent empty UI
        """
        initial_data = {
            "btn_save": "Guardar",
            "btn_cancel": "Cancelar",
            "nav_ingredients": "Ingredientes",
            "nav_recipes": "Recetas",
            "nav_production": "Producción",
            "nav_events": "Eventos"
        }
        
        for key, value in initial_data.items():
            TranslationService.set_translation(db, TranslationCreate(
                language_code="es",
                entity_type="UI",
                entity_id=key,
                field_name="text",
                translation_value=value
            ))
            # Seed English too
            # Ideally this comes from a JSON file, but MVP hardcoded is fine
