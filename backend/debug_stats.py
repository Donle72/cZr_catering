import sys
import os

# Ensure we can import app
sys.path.append(os.getcwd())

from app.core.database import SessionLocal
from app.models.ingredient import Ingredient
from app.models.event import Event, EventStatus
from app.models.recipe import Recipe
from sqlalchemy import func
from datetime import datetime

db = SessionLocal()

def log(msg):
    print(msg)
    sys.stdout.flush()

try:
    log("--- DEBUG STATS START ---")
    
    # Check Ingredients
    ing_count = db.query(Ingredient).count()
    log(f"Total Ingredients Count: {ing_count}")
    
    ingredients = db.query(Ingredient).limit(5).all()
    for ing in ingredients:
        log(f"Ing: {ing.name} | Stock: {ing.stock_quantity} | Cost: {ing.current_cost}")

    inv_value_query = db.query(func.sum(Ingredient.stock_quantity * Ingredient.current_cost))
    inv_value = inv_value_query.scalar()
    log(f"Inventory Value (SQL Sum): {inv_value}")
    
    if inv_value is None:
        # Calculate manually to check
        all_ings = db.query(Ingredient).all()
        manual_sum = sum((i.stock_quantity or 0) * (i.current_cost or 0) for i in all_ings)
        log(f"Inventory Value (Manual Sum): {manual_sum}")

    # Check Events for Revenue
    confirmed_events = db.query(Event).filter(Event.status == EventStatus.CONFIRMED).all()
    log(f"Confirmed Events: {len(confirmed_events)}")
    for ev in confirmed_events:
        log(f"Event: {ev.name} | Total Amount: {ev.total_amount} | Revenue Prop: {ev.total_revenue}")
        
    log("--- DEBUG STATS END ---")
    
except Exception as e:
    log(f"ERROR: {e}")
finally:
    db.close()
