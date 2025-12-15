from sqlalchemy.orm import Session
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe, RecipeItem

class SimulationService:
    @staticmethod
    def simulate_inflation(db: Session, category: str, percentage: float):
        """
        Simulates cost impact if a category of ingredients increases by X%.
        Returns top affected recipes.
        """
        multiplier = 1 + (percentage / 100.0)
        
        # 1. Find Ingredients
        # We fetch ID and Current Cost
        ingredients = db.query(Ingredient.id, Ingredient.current_cost, Ingredient.name)\
            .filter(Ingredient.category == category).all()
            
        affected_ingredient_ids = {ing.id: ing.current_cost * multiplier for ing in ingredients}
        
        if not affected_ingredient_ids:
            return {"message": f"No ingredients found in category '{category}'", "impacted_recipes": []}

        # 2. Find Recipes using these ingredients
        # This is a naive implementation. For massive DBs, we'd use a more optimized query.
        impacted_recipes = []
        
        all_recipes = db.query(Recipe).all()
        
        for recipe in all_recipes:
            original_cost = recipe.total_cost
            new_cost = 0.0
            
            # Recalculate cost
            # We need to traverse items. 
            # Note: This simulation is shallow (doesn't recursively propagate sub-recipe changes efficiently yet)
            # For MVP, we calculate direct ingredient impact.
            
            affected = False
            simulated_items_cost = 0.0
            
            for item in recipe.items:
                if item.ingredient_id in affected_ingredient_ids:
                    # New cost for this item
                    # Quantity * New_Price / Yield... 
                    # We can approximate: ItemCost * Multiplier
                    item_impact = item.item_cost * multiplier
                    simulated_items_cost += item_impact
                    affected = True
                else:
                    simulated_items_cost += item.item_cost
            
            if affected:
                diff = simulated_items_cost - original_cost
                impacted_recipes.append({
                    "recipe_id": recipe.id,
                    "recipe_name": recipe.name,
                    "original_cost": round(original_cost, 2),
                    "new_cost": round(simulated_items_cost, 2),
                    "increase_amount": round(diff, 2),
                    "increase_percentage": round((diff / original_cost * 100), 2) if original_cost > 0 else 0
                })
        
        # Sort by impact
        impacted_recipes.sort(key=lambda x: x['increase_amount'], reverse=True)
        
        return {
            "category": category,
            "simulated_increase_pct": percentage,
            "ingredients_affected_count": len(ingredients),
            "recipes_affected_count": len(impacted_recipes),
            "top_impacted_recipes": impacted_recipes[:20]
        }
