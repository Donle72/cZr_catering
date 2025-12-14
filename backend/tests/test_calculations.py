"""
Tests for calculation logic
Covers yield factor, conversion ratios, recipe costs, and pricing
"""
import pytest
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe, RecipeItem


class TestYieldFactorCalculation:
    """Test yield factor cost calculations"""
    
    def test_yield_factor_basic_calculation(self, db_session):
        """Test basic yield factor calculation"""
        # Create ingredient: $450/kg with 80% yield
        ingredient = Ingredient(
            name="Potato",
            current_cost=450.0,
            yield_factor=0.8,
            conversion_ratio=1.0,
            purchase_unit_id=1,
            usage_unit_id=1
        )
        db_session.add(ingredient)
        db_session.commit()
        
        # Real cost should be 450 / 0.8 = 562.5
        assert ingredient.real_cost_per_usage_unit == 562.5
    
    def test_yield_factor_with_conversion(self, db_session):
        """Test yield factor with unit conversion"""
        # Create ingredient: $1000/kg, use in grams, 85% yield
        ingredient = Ingredient(
            name="Beef",
            current_cost=1000.0,
            yield_factor=0.85,
            conversion_ratio=1000.0,  # 1 kg = 1000 g
            purchase_unit_id=1,  # kg
            usage_unit_id=2   # g
        )
        db_session.add(ingredient)
        db_session.commit()
        
        # Cost per gram = (1000 / 1000) / 0.85 = 1.176
        expected_cost = (1000.0 / 1000.0) / 0.85
        assert abs(ingredient.real_cost_per_usage_unit - expected_cost) < 0.01
    
    def test_yield_factor_perfect_yield(self, db_session):
        """Test with 100% yield (no waste)"""
        ingredient = Ingredient(
            name="Salt",
            current_cost=50.0,
            yield_factor=1.0,
            conversion_ratio=1.0,
            purchase_unit_id=1,
            usage_unit_id=1
        )
        db_session.add(ingredient)
        db_session.commit()
        
        # With 100% yield, real cost = purchase cost
        assert ingredient.real_cost_per_usage_unit == 50.0
    
    def test_yield_factor_zero_protection(self, db_session):
        """Test that zero yield factor doesn't crash"""
        ingredient = Ingredient(
            name="Test",
            current_cost=100.0,
            yield_factor=0.0,  # Invalid but shouldn't crash
            conversion_ratio=1.0,
            purchase_unit_id=1,
            usage_unit_id=1
        )
        db_session.add(ingredient)
        db_session.commit()
        
        # Should return 0 to avoid division by zero
        assert ingredient.real_cost_per_usage_unit == 0.0


class TestRecipeCostCalculation:
    """Test recipe cost calculations"""
    
    def test_recipe_cost_single_ingredient(self, db_session):
        """Test recipe cost with single ingredient"""
        # Create ingredient
        ingredient = Ingredient(
            name="Tomato",
            current_cost=100.0,
            yield_factor=0.95,
            conversion_ratio=1.0,
            purchase_unit_id=1,
            usage_unit_id=1
        )
        db_session.add(ingredient)
        db_session.commit()
        
        # Create recipe
        recipe = Recipe(
            name="Tomato Sauce",
            yield_quantity=4.0,
            yield_unit_id=4,
            target_margin=0.35
        )
        db_session.add(recipe)
        db_session.commit()
        
        # Add ingredient to recipe (2 kg)
        recipe_item = RecipeItem(
            parent_recipe_id=recipe.id,
            ingredient_id=ingredient.id,
            quantity=2.0,
            unit_id=1
        )
        db_session.add(recipe_item)
        db_session.commit()
        db_session.refresh(recipe)
        
        # Total cost = 2 kg * (100 / 0.95) = 210.53
        expected_cost = 2.0 * (100.0 / 0.95)
        assert abs(recipe.total_cost - expected_cost) < 0.01
    
    def test_recipe_cost_per_portion(self, db_session):
        """Test cost per portion calculation"""
        # Create ingredient
        ingredient = Ingredient(
            name="Pasta",
            current_cost=200.0,
            yield_factor=1.0,
            conversion_ratio=1.0,
            purchase_unit_id=1,
            usage_unit_id=1
        )
        db_session.add(ingredient)
        db_session.commit()
        
        # Create recipe for 4 portions
        recipe = Recipe(
            name="Pasta Dish",
            yield_quantity=4.0,
            yield_unit_id=4
        )
        db_session.add(recipe)
        db_session.commit()
        
        # Add 1 kg pasta
        recipe_item = RecipeItem(
            parent_recipe_id=recipe.id,
            ingredient_id=ingredient.id,
            quantity=1.0,
            unit_id=1
        )
        db_session.add(recipe_item)
        db_session.commit()
        db_session.refresh(recipe)
        
        # Cost per portion = 200 / 4 = 50
        assert recipe.cost_per_portion == 50.0
    
    def test_recipe_suggested_price(self, db_session):
        """Test suggested price calculation with margin"""
        # Create simple recipe with known cost
        recipe = Recipe(
            name="Test Dish",
            yield_quantity=1.0,
            yield_unit_id=4,
            target_margin=0.35  # 35% margin
        )
        db_session.add(recipe)
        db_session.commit()
        
        # Manually set total cost for testing
        # If cost = 100, price = 100 / (1 - 0.35) = 153.85
        ingredient = Ingredient(
            name="Test",
            current_cost=100.0,
            yield_factor=1.0,
            conversion_ratio=1.0,
            purchase_unit_id=1,
            usage_unit_id=1
        )
        db_session.add(ingredient)
        db_session.commit()
        
        recipe_item = RecipeItem(
            parent_recipe_id=recipe.id,
            ingredient_id=ingredient.id,
            quantity=1.0,
            unit_id=1
        )
        db_session.add(recipe_item)
        db_session.commit()
        db_session.refresh(recipe)
        
        # Suggested price = 100 / (1 - 0.35) = 153.846
        expected_price = 100.0 / (1 - 0.35)
        assert abs(recipe.suggested_price - expected_price) < 0.01


class TestBulkPriceUpdate:
    """Test bulk price update calculations"""
    
    def test_price_increase_calculation(self):
        """Test percentage increase calculation"""
        original_price = 100.0
        percentage = 15.0
        multiplier = 1 + (percentage / 100)
        new_price = original_price * multiplier
        
        assert new_price == 115.0
        assert multiplier == 1.15
    
    def test_price_decrease_calculation(self):
        """Test percentage decrease calculation"""
        original_price = 100.0
        percentage = -10.0
        multiplier = 1 + (percentage / 100)
        new_price = original_price * multiplier
        
        assert new_price == 90.0
        assert multiplier == 0.9
    
    def test_multiple_updates_compound(self):
        """Test that multiple updates compound correctly"""
        original_price = 100.0
        
        # First update: +10%
        price_after_first = original_price * 1.10
        assert price_after_first == 110.0
        
        # Second update: +10% on new price
        price_after_second = price_after_first * 1.10
        assert price_after_second == 121.0  # Not 120!
