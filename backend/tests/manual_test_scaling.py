import sys
import os
import math
from unittest.mock import MagicMock

# Path setup
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../.env')
load_dotenv(env_path)

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../.env')
load_dotenv(env_path)

# Import models to ensure registry is populated
from app.models.unit import Unit
from app.models.supplier import Supplier
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe, RecipeItem
from app.services.recipe_service import RecipeService

def test_scaling_logic():
    print("Testing Scaling Logic...")
    
    # Mock Objects
    class MockUnit:
        symbol = "kg"
        
    class MockIngredient:
        def __init__(self, name, scaling_type):
            self.name = name
            self.scaling_type = scaling_type
            
    class MockItem:
        def __init__(self, quantity, ingredient):
            self.quantity = quantity
            self.ingredient = ingredient
            self.unit = MockUnit()
            self.unit_id = 1
            self.id = 1
            self.child_recipe = None
            
    class MockRecipe:
        def __init__(self, yield_qty, items):
            self.id = 1
            self.name = "Test Recipe"
            self.yield_quantity = yield_qty
            self.items = items
            
    # Scenario: 10kg Yield -> 100kg Target (Factor 10)
    # Water (Linear): 1L -> 10L
    # Salt (Log): 0.1kg -> 0.1 * (10^0.85) = 0.1 * 7.079 = 0.7079 kg
    
    water = MockItem(1.0, MockIngredient("Water", "linear"))
    salt = MockItem(0.1, MockIngredient("Salt", "logarithmic"))
    recipe = MockRecipe(10.0, [water, salt])
    
    # Mock DB Session
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_filter = MagicMock()
    
    # Chain: db.query(Recipe).options(...).filter(...).first()
    mock_db.query.return_value = mock_query
    mock_query.options.return_value = mock_query
    mock_query.filter.return_value = mock_filter
    mock_filter.first.return_value = recipe
    
    # Run Service
    result = RecipeService.scale_recipe(mock_db, 1, 100.0)
    
    print(f"Scaling Factor: {result['scaling_factor']}")
    
    for item in result['items']:
        print(f"Item: {item['name']} ({item['scaling_type']})")
        print(f"  Original: {item['original_quantity']}")
        print(f"  New:      {item['new_quantity']}")
        
        if item['name'] == "Water":
            assert math.isclose(item['new_quantity'], 10.0, rel_tol=1e-3), "Water should be 10.0"
        elif item['name'] == "Salt":
            expected = 0.1 * math.pow(10, 0.85)
            assert math.isclose(item['new_quantity'], expected, rel_tol=1e-3), f"Salt should be {expected}"

    print("✅ TEST PASSED: Scaling logic validates correctly.")

if __name__ == "__main__":
    test_scaling_logic()
