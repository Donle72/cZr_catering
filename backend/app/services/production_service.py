"""
Production Service
Handles logic for consolidating event orders into production plans and shopping lists.
"""
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Dict, Any, Optional

from app.models.event import Event, EventStatus
from app.models.recipe import Recipe, RecipeItem, RecipeType
from app.models.ingredient import Ingredient

class ProductionService:
    @staticmethod
    def get_production_plan(db: Session, start_date: date, end_date: date) -> Dict[str, Any]:
        """
        Consolidate all recipes from confirmed events within date range.
        Returns a dictionary with:
        - events: List of events included
        - ingredients: Aggregated list of ingredients needed
        - sub_recipes: Aggregated list of sub-recipes to prepare
        """
        # 1. Fetch relevant events
        events = db.query(Event).filter(
            Event.event_date >= start_date,
            Event.event_date <= end_date,
            Event.status.in_([EventStatus.CONFIRMED, EventStatus.IN_PROGRESS])
        ).all()
        
        if not events:
            return {"events": [], "ingredients": [], "sub_recipes": []}

        # 2. Initialize aggregators
        ingredient_needs: Dict[int, Dict] = {} # ingredient_id -> {qty, details}
        sub_recipe_needs: Dict[int, Dict] = {} # recipe_id -> {qty, details}
        
        # 3. Process each event
        for event in events:
            for order in event.orders:
                recipe = order.recipe
                if not recipe:
                    continue
                    
                # Calculate total servings needed for this order
                qty_needed = order.quantity
                
                # Recursive explosion of recipe
                ProductionService._explode_recipe(
                    db, recipe, qty_needed, ingredient_needs, sub_recipe_needs, event.name
                )

        # 4. Format output
        return {
            "events": [
                {"id": e.id, "name": e.name, "date": e.event_date, "guests": e.guest_count} 
                for e in events
            ],
            "ingredients": list(ingredient_needs.values()),
            "sub_recipes": list(sub_recipe_needs.values())
        }

    @staticmethod
    def _explode_recipe(
        db: Session, 
        recipe: Recipe, 
        quantity_needed: float, 
        ing_agg: Dict, 
        sub_agg: Dict,
        event_ref: str
    ):
        """
        Recursively break down a recipe into ingredients and sub-recipes.
        quantity_needed: Number of 'yield units' of this recipe needed (e.g. 50 portions)
        """
        
        # Base logic: How many "batches" of the recipe do we need?
        # If recipe yields 10 portions and we need 50, we need 5 batches.
        # However, 'quantity' in RecipeItem is usually per 1 unit of yield if yield_quantity=1
        
        # Let's assume standard catering model:
        # Recipe defined for X portions (yield_quantity).
        # We need Y portions.
        # Scaling Factor = Y / X
        
        if recipe.yield_quantity == 0:
            return

        scaling_factor = quantity_needed / recipe.yield_quantity
        
        # If this is a SUB_RECIPE (mise en place), track it as a production item itself
        if recipe.recipe_type == RecipeType.SUB_RECIPE:
            if recipe.id not in sub_agg:
                sub_agg[recipe.id] = {
                    "id": recipe.id,
                    "name": recipe.name,
                    "unit": recipe.yield_unit.name if recipe.yield_unit else "units",
                    "total_quantity": 0.0,
                    "events": []
                }
            sub_agg[recipe.id]["total_quantity"] += quantity_needed
            if event_ref not in sub_agg[recipe.id]["events"]:
                sub_agg[recipe.id]["events"].append(event_ref)

        # Process items
        for item in recipe.items:
            # Scaled quantity for this item
            item_qty = item.quantity * scaling_factor
            
            if item.ingredient_id:
                # Aggregate Ingredient
                ing_id = item.ingredient_id
                if ing_id not in ing_agg:
                    ing = item.ingredient
                    ing_agg[ing_id] = {
                        "id": ing.id,
                        "name": ing.name,
                        "sku": ing.sku,
                        "category": ing.category_rel.name if ing.category_rel else None,
                        "unit": item.unit.name if item.unit else "units", # Assuming consistent units for MVP 
                        "stock": ing.stock_quantity,
                        "total_required": 0.0,
                        "to_buy": 0.0,
                        "events": []
                    }
                
                ing_agg[ing_id]["total_required"] += item_qty
                
                # Logic to determine "To Buy"
                net_needed = ing_agg[ing_id]["total_required"] - ing_agg[ing_id]["stock"]
                ing_agg[ing_id]["to_buy"] = max(0.0, net_needed)
                
                if event_ref not in ing_agg[ing_id]["events"]:
                    ing_agg[ing_id]["events"].append(event_ref)
                    
            elif item.child_recipe_id:
                # Recursive call for Sub-Recipe
                child = item.child_recipe
                ProductionService._explode_recipe(
                    db, child, item_qty, ing_agg, sub_agg, event_ref
                )
