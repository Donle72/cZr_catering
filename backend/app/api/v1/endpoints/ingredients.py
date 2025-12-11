"""
Ingredients API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import math

from app.core.database import get_db
from app.models.ingredient import Ingredient
from app.schemas.ingredient import (
    IngredientCreate,
    IngredientUpdate,
    IngredientResponse,
    IngredientList
)

router = APIRouter()


@router.get("/")
def list_ingredients(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: str = Query(None),
    search: str = Query(None),
    db: Session = Depends(get_db)
):
    """
    List all ingredients with pagination and filtering
    """
    query = db.query(Ingredient)
    
    # Apply filters
    if category:
        query = query.filter(Ingredient.category == category)
    
    if search:
        query = query.filter(
            Ingredient.name.ilike(f"%{search}%") | 
            Ingredient.sku.ilike(f"%{search}%")
        )
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    ingredients = query.offset(skip).limit(limit).all()
    
    # Convert to dict manually
    items = []
    for ing in ingredients:
        items.append({
            "id": ing.id,
            "name": ing.name,
            "sku": ing.sku,
            "description": ing.description,
            "category": ing.category,
            "current_cost": ing.current_cost,
            "yield_factor": ing.yield_factor,
            "real_cost_per_usage_unit": ing.real_cost_per_usage_unit,
            "purchase_unit_id": ing.purchase_unit_id,
            "usage_unit_id": ing.usage_unit_id,
            "conversion_ratio": ing.conversion_ratio,
            "tax_rate": ing.tax_rate
        })
    
    return {
        "items": items,
        "total": total,
        "page": skip // limit + 1 if limit > 0 else 1,
        "page_size": limit,
        "pages": math.ceil(total / limit) if total > 0 and limit > 0 else 0
    }


@router.post("/", response_model=IngredientResponse, status_code=201)
def create_ingredient(
    ingredient: IngredientCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new ingredient
    """
    # Check if SKU already exists
    if ingredient.sku:
        existing = db.query(Ingredient).filter(Ingredient.sku == ingredient.sku).first()
        if existing:
            raise HTTPException(status_code=400, detail="SKU already exists")
    
    db_ingredient = Ingredient(**ingredient.model_dump())
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    
    return db_ingredient


@router.get("/{ingredient_id}", response_model=IngredientResponse)
def get_ingredient(
    ingredient_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific ingredient by ID
    """
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    
    return ingredient


@router.put("/{ingredient_id}", response_model=IngredientResponse)
def update_ingredient(
    ingredient_id: int,
    ingredient_update: IngredientUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an ingredient
    """
    db_ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    
    # Update fields
    update_data = ingredient_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_ingredient, field, value)
    
    db.commit()
    db.refresh(db_ingredient)
    
    return db_ingredient


@router.delete("/{ingredient_id}", status_code=204)
def delete_ingredient(
    ingredient_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an ingredient
    """
    db_ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    
    db.delete(db_ingredient)
    db.commit()
    
    return None


@router.post("/bulk-price-update")
def bulk_price_update(
    category: str = Query(None),
    percentage_increase: float = Query(..., description="Percentage to increase prices (e.g., 15 for 15%)"),
    db: Session = Depends(get_db)
):
    """
    Bulk update prices by category (anti-inflation feature)
    Formula: New Cost = Current Cost * (1 + percentage/100)
    """
    query = db.query(Ingredient)
    
    if category:
        query = query.filter(Ingredient.category == category)
    
    ingredients = query.all()
    
    if not ingredients:
        raise HTTPException(status_code=404, detail="No ingredients found")
    
    updated_count = 0
    multiplier = 1 + (percentage_increase / 100)
    
    for ingredient in ingredients:
        ingredient.current_cost = ingredient.current_cost * multiplier
        updated_count += 1
    
    db.commit()
    
    return {
        "message": f"Updated {updated_count} ingredients",
        "category": category or "all",
        "percentage_increase": percentage_increase,
        "multiplier": multiplier
    }
