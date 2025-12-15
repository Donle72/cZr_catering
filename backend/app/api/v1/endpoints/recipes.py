"""
Recipes API endpoints
Full CRUD with recursive composition logic
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List
import math

from app.core.database import get_db
from app.models.recipe import Recipe, RecipeItem
from app.schemas.recipe import (
    RecipeCreate, 
    RecipeUpdate, 
    RecipeResponse, 
    RecipeItemCreate
)
from app.services.recipe_service import RecipeService

router = APIRouter()

@router.get("/", response_model=None)
def list_recipes(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    type: str = Query(None),
    search: str = Query(None),
    db: Session = Depends(get_db)
):
    """
    List all recipes with pagination
    """
    query = db.query(Recipe)
    
    if type:
        query = query.filter(Recipe.recipe_type == type)
        
    if search:
        query = query.filter(Recipe.name.ilike(f"%{search}%"))
        
    total = query.count()
    recipes = query.offset(skip).limit(limit).all()
    
    # Manual serialization to avoid circular issues and optimize
    items = []
    for r in recipes:
        items.append({
            "id": r.id,
            "name": r.name,
            "recipe_type": r.recipe_type,
            "yield_quantity": r.yield_quantity,
            "total_cost": r.total_cost,
            "cost_per_portion": r.cost_per_portion,
            "suggested_price": r.suggested_price,
            "target_margin": r.target_margin
        })
    
    return {
        "items": items,
        "total": total,
        "page": skip // limit + 1 if limit > 0 else 1,
        "pages": math.ceil(total / limit) if total > 0 and limit > 0 else 0
    }


@router.get("/{recipe_id}/scale")
def scale_recipe(
    recipe_id: int, 
    target_quantity: float = Query(..., gt=0, description="Target yield quantity"), 
    db: Session = Depends(get_db)
):
    """
    Calculates required ingredients for a specific yield quantity.
    Uses non-linear scaling for specific ingredients (Salt/Spices).
    """
    return RecipeService.scale_recipe(db, recipe_id, target_quantity)

@router.post("/", response_model=RecipeResponse, status_code=201)
def create_recipe(
    recipe: RecipeCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new recipe with optional initial items
    """
    # 1. Create Recipe Header
    db_recipe = Recipe(
        name=recipe.name,
        description=recipe.description,
        recipe_type=recipe.recipe_type,
        yield_quantity=recipe.yield_quantity,
        yield_unit_id=recipe.yield_unit_id,
        target_margin=recipe.target_margin,
        preparation_time=recipe.preparation_time,
        instructions=recipe.instructions,
        shelf_life_hours=recipe.shelf_life_hours
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    
    # 2. Create Items if provided
    if recipe.items:
        for item in recipe.items:
            db_item = RecipeItem(
                parent_recipe_id=db_recipe.id,
                ingredient_id=item.ingredient_id,
                child_recipe_id=item.child_recipe_id,
                quantity=item.quantity,
                unit_id=item.unit_id,
                notes=item.notes,
                is_scalable=item.is_scalable
            )
            db.add(db_item)
        db.commit()
        db.refresh(db_recipe)
        
    return db_recipe

@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """
    Get full recipe details with items and calculated costs
    """
    # Use joinedload to fetch items and their relations efficiently
    recipe = db.query(Recipe).options(
        joinedload(Recipe.items).joinedload(RecipeItem.ingredient),
        joinedload(Recipe.items).joinedload(RecipeItem.child_recipe),
        joinedload(Recipe.items).joinedload(RecipeItem.unit)
    ).filter(Recipe.id == recipe_id).first()
    
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Transform items for response
    response_items = []
    for item in recipe.items:
        response_item = {
            "id": item.id,
            "quantity": item.quantity,
            "unit_id": item.unit_id,
            "notes": item.notes,
            "is_scalable": item.is_scalable,
            "item_cost": item.item_cost,
            "ingredient": item.ingredient,
            "child_recipe_id": item.child_recipe_id,
            "child_recipe_name": item.child_recipe.name if item.child_recipe else None
        }
        response_items.append(response_item)

    # Manual construction of response to handle properties
    return {
        "id": recipe.id,
        "name": recipe.name,
        "description": recipe.description,
        "recipe_type": recipe.recipe_type,
        "yield_quantity": recipe.yield_quantity,
        "yield_unit_id": recipe.yield_unit_id,
        "target_margin": recipe.target_margin,
        "preparation_time": recipe.preparation_time,
        "instructions": recipe.instructions,
        "shelf_life_hours": recipe.shelf_life_hours,
        "created_at": recipe.created_at,
        "updated_at": recipe.updated_at,
        "total_cost": recipe.total_cost,
        "cost_per_portion": recipe.cost_per_portion,
        "suggested_price": recipe.suggested_price,
        "items": response_items
    }

@router.post("/{recipe_id}/items", status_code=201)
def add_recipe_item(
    recipe_id: int,
    item: RecipeItemCreate,
    db: Session = Depends(get_db)
):
    """
    Add an ingredient or sub-recipe to an existing recipe
    """
    # Validate parent exists
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
        
    # Validate it's not self-referential
    if item.child_recipe_id == recipe_id:
        raise HTTPException(status_code=400, detail="Cannot add recipe to itself")
        
    # Validate either ingredient OR child_recipe (XOR logic)
    if not (item.ingredient_id or item.child_recipe_id):
        raise HTTPException(status_code=400, detail="Must provide ingredient_id OR child_recipe_id")
    if item.ingredient_id and item.child_recipe_id:
        raise HTTPException(status_code=400, detail="Cannot provide both ingredient and child recipe")
        
    db_item = RecipeItem(
        parent_recipe_id=recipe_id,
        ingredient_id=item.ingredient_id,
        child_recipe_id=item.child_recipe_id,
        quantity=item.quantity,
        unit_id=item.unit_id,
        notes=item.notes,
        is_scalable=item.is_scalable
    )
    
    db.add(db_item)
    db.commit()
    db.refresh(recipe)
    
    return {"message": "Item added successfully", "new_total_cost": recipe.total_cost}

@router.delete("/{recipe_id}/items/{item_id}", status_code=204)
def remove_recipe_item(
    recipe_id: int,
    item_id: int,
    db: Session = Depends(get_db)
):
    """
    Remove an item from a recipe
    """
    item = db.query(RecipeItem).filter(
        RecipeItem.id == item_id,
        RecipeItem.parent_recipe_id == recipe_id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
        
    db.delete(item)
    db.commit()
    
    return None
