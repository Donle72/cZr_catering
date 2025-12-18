"""
Ingredients API endpoints - Simple version
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import math

from app.core.database import get_db
from app.models.ingredient import Ingredient, IngredientPriceHistory
from app.schemas.ingredient import (
    IngredientCreate,
    IngredientUpdate,
    IngredientResponse,
    IngredientList,
    IngredientBulkUpdate
)

router = APIRouter()


@router.get("/", response_model=IngredientList)
def list_ingredients(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: str = Query(None),
    search: str = Query(None),
    db: Session = Depends(get_db)
):
    """List all ingredients with pagination and filtering"""
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
    
    # Apply pagination with deterministic ordering
    ingredients = query.order_by(Ingredient.name).offset(skip).limit(limit).all()
    
    return {
        "items": ingredients,
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
    """Create a new ingredient"""
    # Check for duplicate SKU
    if ingredient.sku:
        existing = db.query(Ingredient).filter(Ingredient.sku == ingredient.sku).first()
        if existing:
            raise HTTPException(status_code=409, detail=f"Ingredient with SKU {ingredient.sku} already exists")
    
    # Create ingredient
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
    """Get a specific ingredient by ID"""
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
    """Update an ingredient"""
    db_ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    
    # Update fields
    update_data = ingredient_update.model_dump(exclude_unset=True)
    
    # Track price change
    old_cost = db_ingredient.current_cost
    new_cost = update_data.get('current_cost')
    
    for field, value in update_data.items():
        setattr(db_ingredient, field, value)
    
    # Log history if cost changed
    if new_cost is not None and new_cost != old_cost:
        history = IngredientPriceHistory(
            ingredient_id=db_ingredient.id,
            old_cost=old_cost,
            new_cost=new_cost,
            changed_by="API User" # Placeholder for auth
        )
        db.add(history)
    
    db.commit()
    db.refresh(db_ingredient)
    
    return db_ingredient


@router.delete("/{ingredient_id}", status_code=204)
def delete_ingredient(
    ingredient_id: int,
    db: Session = Depends(get_db)
):
    """Delete an ingredient"""
    from app.models.recipe import RecipeItem
    from app.models.ingredient import IngredientPriceHistory
    from sqlalchemy.orm import joinedload
    
    db_ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    
    # Check if ingredient is used in any recipes (use joinedload to avoid lazy loading issues)
    recipes_using = db.query(RecipeItem).options(
        joinedload(RecipeItem.parent_recipe)
    ).filter(RecipeItem.ingredient_id == ingredient_id).all()
    
    if recipes_using:
        # Get unique recipe names
        recipe_names = list(set([item.parent_recipe.name for item in recipes_using if item.parent_recipe]))
        
        raise HTTPException(
            status_code=409,
            detail={
                "message": f"Cannot delete ingredient '{db_ingredient.name}' because it is used in {len(recipe_names)} recipe(s)",
                "ingredient_name": db_ingredient.name,
                "recipes_using": recipe_names[:10],  # Limit to first 10
                "total_recipes": len(recipe_names),
                "suggestion": "Remove this ingredient from all recipes before deleting, or consider marking it as inactive instead"
            }
        )
    
    # Delete price history first (to avoid FK constraint error)
    db.query(IngredientPriceHistory).filter(
        IngredientPriceHistory.ingredient_id == ingredient_id
    ).delete()
    
    # Now delete the ingredient
    db.delete(db_ingredient)
    db.commit()
    
    return None


@router.post("/bulk-price-update")
def bulk_price_update(
    update_data: IngredientBulkUpdate,
    db: Session = Depends(get_db)
):
    """
    Bulk update prices by category (anti-inflation feature)
    Formula: New Cost = Current Cost * (1 + percentage/100)
    """
    query = db.query(Ingredient)
    
    if update_data.category:
        query = query.filter(Ingredient.category == update_data.category)
    
    ingredients = query.all()
    
    # Allow empty results - return 0 updated
    if not ingredients:
        return {
            "message": "No ingredients found in category",
            "category": update_data.category or "all",
            "percentage_increase": update_data.percentage_increase,
            "multiplier": 1 + (update_data.percentage_increase / 100),
            "ingredients_updated": 0,
            "total_cost_before": 0.0,
            "total_cost_after": 0.0
        }
    
    updated_count = 0
    multiplier = 1 + (update_data.percentage_increase / 100)
    total_cost_before = 0.0
    total_cost_after = 0.0
    
    for ingredient in ingredients:
        old_cost = ingredient.current_cost
        new_cost = old_cost * multiplier
        
        total_cost_before += old_cost
        total_cost_after += new_cost
        
        if new_cost != old_cost:
            ingredient.current_cost = new_cost
            
            # Log history
            history = IngredientPriceHistory(
                ingredient_id=ingredient.id,
                old_cost=old_cost,
                new_cost=new_cost,
                changed_by=f"Bulk Update {update_data.percentage_increase}%"
            )
            db.add(history)
            
            updated_count += 1
    
    db.commit()
    
    return {
        "message": f"Successfully updated {updated_count} ingredient(s)",
        "category": update_data.category or "all",
        "percentage_increase": update_data.percentage_increase,
        "multiplier": multiplier,
        "ingredients_updated": updated_count,
        "total_cost_before": total_cost_before,
        "total_cost_after": total_cost_after
    }

