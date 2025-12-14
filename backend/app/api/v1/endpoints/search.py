from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from pydantic import BaseModel

from app.core.database import get_db
from app.models.ingredient import Ingredient
from app.models.unit import Unit

router = APIRouter()

class SearchResultItem(BaseModel):
    id: int
    name: str
    sku: Optional[str] = None
    category: str
    current_cost: float
    unit_symbol: str
    
    class Config:
        from_attributes = True

@router.get("/ingredients", response_model=List[SearchResultItem])
def search_ingredients(
    q: str = Query(..., min_length=2, description="Search query string"),
    limit: int = Query(10, le=50),
    db: Session = Depends(get_db)
):
    """
    Optimized search endpoint for autocomplete.
    Searches in name and sku.
    """
    search_term = f"%{q}%"
    
    results = db.query(
        Ingredient.id,
        Ingredient.name,
        Ingredient.sku,
        Ingredient.category,
        Ingredient.current_cost,
        Unit.symbol.label("unit_symbol")
    ).join(
        Unit, Ingredient.usage_unit_id == Unit.id
    ).filter(
        or_(
            Ingredient.name.ilike(search_term),
            Ingredient.sku.ilike(search_term)
        )
    ).limit(limit).all()
    
    return results
