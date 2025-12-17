"""
Suggestions API endpoints
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.services.suggestion_service import SuggestionService
from app.schemas.recipe import RecipeResponse

router = APIRouter()


@router.get("/recipes", response_model=List[RecipeResponse])
def suggest_recipes(
    event_type: str = Query(..., description="Event type (COCKTAIL, COMPLETO_FORMAL, etc.)"),
    course_type: Optional[str] = Query(None, description="Course type (ENTRANTE, PRINCIPAL, POSTRE)"),
    dietary: Optional[List[str]] = Query(None, description="Dietary restrictions"),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get recipe suggestions based on event type and requirements
    """
    return SuggestionService.suggest_recipes_for_event(
        db=db,
        event_type=event_type,
        course_type=course_type,
        dietary_restrictions=dietary,
        limit=limit
    )


@router.get("/beverages", response_model=List[RecipeResponse])
def suggest_beverages(
    service_type: str = Query(..., description="Service type (BARRA, CORTESIA, etc.)"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get beverage suggestions based on service type
    """
    return SuggestionService.suggest_beverages_for_service(
        db=db,
        service_type=service_type,
        limit=limit
    )
