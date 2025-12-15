import sys
import os
from unittest.mock import MagicMock

# Add parent dir (backend) to path
try:
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(backend_dir)
except:
    pass

from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../.env')
load_dotenv(env_path)

from app.services.simulation_service import SimulationService

def test_inflation_simulation():
    print("Testing Inflation Simulation...")
    
    # Mock DB Session
    mock_db = MagicMock()
    
    # 1. Mock Ingredients (Category: Meats)
    class MockIngredient:
        def __init__(self, id, name, cost, category):
            self.id = id
            self.name = name
            self.current_cost = cost
            self.category = category
            
    meat_1 = MockIngredient(1, "Beef", 1000.0, "Meats") # +15% -> 1150 (+150)
    meat_2 = MockIngredient(2, "Pork", 800.0, "Meats")  # +15% -> 920 (+120)
    
    # Mock DB Query for Ingredients
    # chain: db.query(...).filter(...).all()
    mock_query_ing = MagicMock()
    mock_filter_ing = MagicMock()
    
    mock_db.query.return_value = mock_query_ing
    mock_query_ing.filter.return_value = mock_filter_ing
    mock_filter_ing.all.return_value = [meat_1, meat_2]
    
    # 2. Mock Recipes
    class MockItem:
        def __init__(self, ingredient_id, item_cost):
            self.ingredient_id = ingredient_id
            self.item_cost = item_cost # In a real recipe, this is calculated. Here simpler.
            
    class MockRecipe:
        def __init__(self, id, name, total_cost, items):
            self.id = id
            self.name = name
            self.total_cost = total_cost
            self.items = items
            
    # Recipe with Beef
    # Total Cost 2000. Beef part is 500 (item_cost). 
    # If Beef cost doubles (from ingredient price), item_cost doubles? 
    # Logic in service: item_impact = item.item_cost * multiplier
    # So if Beef (1000) becomes 1150 (1.15x), item cost (500) becomes 575. Diff = 75.
    r1 = MockRecipe(101, "Beef Stew", 2000.0, [MockItem(1, 500.0)])
    
    # Recipe with Pork
    # Pork part 400. 1.15x -> 460. Diff = 60.
    r2 = MockRecipe(102, "Pork Chop", 1500.0, [MockItem(2, 400.0)])
    
    # Recipe with Chicken (Not in affected ingredient list)
    r3 = MockRecipe(103, "Chicken Soup", 800.0, [MockItem(99, 300.0)])
    
    # We need to ensure db.query(Recipe).all() returns these when called later
    # The service calls db.query(Ingredient)... then db.query(Recipe)...
    # So we need side_effect on db.query
    
    def query_side_effect(*args, **kwargs):
        # We assume the first arg is the model or we check args[0]
        model = args[0] if args else None
        
        if hasattr(model, '__name__') and model.__name__ == 'Ingredient':
            return mock_query_ing # which filters to meats
        elif hasattr(model, '__name__') and model.__name__ == 'Recipe':
            q = MagicMock()
            q.all.return_value = [r1, r2, r3]
            return q
        # Handle tuple case for specific column selection: db.query(Ingredient.id, ...)
        # In this specific test case, we know the service calls query(Ingredient.id...)
        # We can just check if any arg is an attribute of Ingredient
        return mock_query_ing # Default fallback for this specific test context
        
    mock_db.query.side_effect = query_side_effect
    
    # Run Simulation
    # Simulate 15% increase on "Meats"
    result = SimulationService.simulate_inflation(mock_db, "Meats", 15.0)
    
    print(f"Category: {result['category']}")
    print(f"Increase: {result['simulated_increase_pct']}%")
    print(f"Impacted Recipes: {result['recipes_affected_count']}")
    
    for r in result['top_impacted_recipes']:
        print(f" - {r['recipe_name']}: +${r['increase_amount']} ({r['increase_percentage']}%)")
        
        if r['recipe_name'] == "Beef Stew":
            # Expected increase: item_cost(500) * 0.15 = 75.0
            assert r['increase_amount'] == 75.0
            
    print("✅ Inflation Simulation Validated.")

if __name__ == "__main__":
    test_inflation_simulation()
