from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, extract
from datetime import datetime

from app.core.database import get_db
from app.models.event import Event, EventStatus
from app.models.recipe import Recipe
from app.models.ingredient import Ingredient


router = APIRouter()

@router.get("/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Get aggregated stats for the dashboard
    """
    current_date = datetime.now()
    
    # 1. Events Stats
    events_count = db.query(Event).filter(
        extract('month', Event.event_date) == current_date.month,
        extract('year', Event.event_date) == current_date.year
    ).count()
    
    # 2. Revenue (Optimized with eager loading)
    confirmed_events_month = db.query(Event).options(joinedload(Event.orders)).filter(
        Event.status == EventStatus.CONFIRMED,
        extract('month', Event.event_date) == current_date.month,
        extract('year', Event.event_date) == current_date.year
    ).all()
    
    estimated_revenue = sum(ev.total_revenue for ev in confirmed_events_month)
    
    # 3. Recipes Stats
    active_recipes = db.query(Recipe).count()
    
    # PERFORMANCE OPTIMIZATION: 
    # Calculating average cost requires recursive queries for ALL recipes.
    # Disabling for now to prevent dashboard lag.
    # all_recipes = db.query(Recipe).all()
    # avg_recipe_cost = ...
    avg_recipe_cost = 0 
    profitable_recipes = 0

    # 4. Ingredients Stats
    total_ingredients = db.query(Ingredient).count()
    
    # Inventory Value (Sum of stock * cost)
    # Ingredient.stock_quantity * Ingredient.current_cost
    inventory_value = db.query(
        func.sum(Ingredient.stock_quantity * Ingredient.current_cost)
    ).scalar() or 0.0
    
    low_stock_count = db.query(Ingredient).filter(
        Ingredient.stock_quantity <= Ingredient.min_stock_threshold
    ).count()

    return {
        "events_month": events_count,
        "revenue_month": estimated_revenue,
        "active_recipes": active_recipes,
        "avg_recipe_cost": avg_recipe_cost,
        "profitable_recipes": profitable_recipes,
        "total_ingredients": total_ingredients,
        "inventory_value": inventory_value,
        "low_stock_count": low_stock_count
    }
