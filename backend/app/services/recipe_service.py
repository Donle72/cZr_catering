from sqlalchemy.orm import Session, joinedload
from app.models.recipe import Recipe, RecipeItem
from app.models.ingredient import Ingredient
from fastapi import HTTPException
import math

class RecipeService:
    @staticmethod
    def scale_recipe(db: Session, recipe_id: int, target_quantity: float):
        """
        Scales a recipe to a target quantity.
        Applies non-linear scaling (logarithmic) for ingredients marked as such (e.g., Salt, Spices).
        Formula: 
            Linear: New = Old * Factor
            Logarithmic: New = Old * (Factor ^ 0.85)
        """
        recipe = db.query(Recipe).options(
            joinedload(Recipe.items).joinedload(RecipeItem.ingredient),
            joinedload(Recipe.items).joinedload(RecipeItem.child_recipe),
            joinedload(Recipe.items).joinedload(RecipeItem.unit)
        ).filter(Recipe.id == recipe_id).first()
        
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
            
        if recipe.yield_quantity <= 0:
             raise HTTPException(status_code=400, detail="Original recipe yield must be greater than 0")

        factor = target_quantity / recipe.yield_quantity
        scaled_items = []

        for item in recipe.items:
            # Determine if we should apply logarithmic scaling
            # Only applies to Ingredients, not Sub-recipes
            # And only if ingredient.scaling_type == 'logarithmic'
            
            is_logarithmic = False
            if item.ingredient and item.ingredient.scaling_type == 'logarithmic':
                is_logarithmic = True
            
            # Apply formula
            if is_logarithmic and factor > 1:
                # Logarithmic scaling (usually for scaling UP, prevents over-salting)
                # For scaling DOWN, linear is usually safer or keeping same logic? 
                # Standard culinary practice is mostly concerned with scaling UP.
                # We will apply the formula consistently.
                modified_factor = math.pow(factor, 0.85)
                new_quantity = item.quantity * modified_factor
            else:
                # Linear scaling
                new_quantity = item.quantity * factor
                
            scaled_items.append({
                "item_id": item.id,
                "name": item.ingredient.name if item.ingredient else item.child_recipe.name,
                "type": "ingredient" if item.ingredient else "recipe",
                "original_quantity": item.quantity,
                "new_quantity": round(new_quantity, 4),
                "unit": item.unit.symbol,
                "unit_id": item.unit_id,
                "scaling_type": "logarithmic" if is_logarithmic else "linear"
            })
            
        return {
            "recipe_id": recipe.id,
            "recipe_name": recipe.name,
            "original_yield": recipe.yield_quantity,
            "target_yield": target_quantity,
            "scaling_factor": round(factor, 4),
            "items": scaled_items
        }
