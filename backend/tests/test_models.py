"""
Tests for data models (Ingredient, Recipe, Event)
"""
import pytest
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe, RecipeItem, RecipeType
from app.models.event import Event, EventOrder, EventStatus


class TestIngredientModel:
    """Tests for Ingredient model"""
    
    def test_real_cost_calculation_with_yield_factor(self, db_session, sample_units):
        """Test real cost calculation with yield factor"""
        ingredient = Ingredient(
            name="Potato",
            purchase_unit_id=1,  # kg
            usage_unit_id=2,  # g
            conversion_ratio=1000.0,
            current_cost=100.0,  # $100 per kg
            yield_factor=0.80,  # 80% yield (20% waste)
        )
        db_session.add(ingredient)
        db_session.commit()
        
        # Expected: (100 / 1000) / 0.80 = 0.125
        expected_cost = 0.125
        assert ingredient.real_cost_per_usage_unit == pytest.approx(expected_cost, rel=1e-3)
    
    def test_real_cost_with_perfect_yield(self, db_session, sample_units):
        """Test real cost with 100% yield (no waste)"""
        ingredient = Ingredient(
            name="Sugar",
            purchase_unit_id=1,  # kg
            usage_unit_id=2,  # g
            conversion_ratio=1000.0,
            current_cost=200.0,
            yield_factor=1.0,  # 100% yield
        )
        db_session.add(ingredient)
        db_session.commit()
        
        # Expected: (200 / 1000) / 1.0 = 0.2
        expected_cost = 0.2
        assert ingredient.real_cost_per_usage_unit == pytest.approx(expected_cost, rel=1e-3)
    
    def test_real_cost_with_low_yield(self, db_session, sample_units):
        """Test real cost with low yield (high waste)"""
        ingredient = Ingredient(
            name="Artichoke",
            purchase_unit_id=1,
            usage_unit_id=2,
            conversion_ratio=1000.0,
            current_cost=300.0,
            yield_factor=0.40,  # 40% yield (60% waste)
        )
        db_session.add(ingredient)
        db_session.commit()
        
        # Expected: (300 / 1000) / 0.40 = 0.75
        expected_cost = 0.75
        assert ingredient.real_cost_per_usage_unit == pytest.approx(expected_cost, rel=1e-3)
    
    def test_real_cost_with_zero_yield_returns_zero(self, db_session, sample_units):
        """Test that zero yield factor returns 0 (edge case)"""
        ingredient = Ingredient(
            name="Test",
            purchase_unit_id=1,
            usage_unit_id=2,
            conversion_ratio=1000.0,
            current_cost=100.0,
            yield_factor=0.0,
        )
        db_session.add(ingredient)
        db_session.commit()
        
        assert ingredient.real_cost_per_usage_unit == 0.0
    
    def test_real_cost_with_none_values(self, db_session, sample_units):
        """Test that None values are handled gracefully"""
        ingredient = Ingredient(
            name="Test",
            purchase_unit_id=1,
            usage_unit_id=2,
            conversion_ratio=None,
            current_cost=None,
            yield_factor=None,
        )
        db_session.add(ingredient)
        db_session.commit()
        
        # Should return 0.0 when values are None
        assert ingredient.real_cost_per_usage_unit == 0.0


class TestRecipeModel:
    """Tests for Recipe model"""
    
    def test_recipe_total_cost_with_ingredients_only(self, db_session, sample_units, sample_ingredients):
        """Test total cost calculation with ingredients only"""
        recipe = Recipe(
            name="Simple Salad",
            recipe_type=RecipeType.FINAL_DISH,
            yield_quantity=2.0,
            yield_unit_id=5,  # portions
            target_margin=0.30,
        )
        db_session.add(recipe)
        db_session.commit()
        
        # Add ingredients
        tomato = sample_ingredients[0]  # $150/kg, 85% yield, 1000g conversion
        onion = sample_ingredients[1]   # $80/kg, 90% yield, 1000g conversion
        
        items = [
            RecipeItem(
                parent_recipe_id=recipe.id,
                ingredient_id=tomato.id,
                quantity=200.0,  # 200g
                unit_id=2,  # g
            ),
            RecipeItem(
                parent_recipe_id=recipe.id,
                ingredient_id=onion.id,
                quantity=100.0,  # 100g
                unit_id=2,  # g
            ),
        ]
        
        for item in items:
            db_session.add(item)
        db_session.commit()
        db_session.refresh(recipe)
        
        # Calculate expected cost
        # Tomato: (150/1000)/0.85 * 200 = 35.29
        # Onion: (80/1000)/0.90 * 100 = 8.89
        # Total: 44.18
        expected_cost = 44.18
        assert recipe.total_cost == pytest.approx(expected_cost, rel=0.01)
    
    def test_recipe_cost_per_portion(self, db_session, sample_units, sample_ingredients):
        """Test cost per portion calculation"""
        recipe = Recipe(
            name="Dish",
            recipe_type=RecipeType.FINAL_DISH,
            yield_quantity=4.0,  # 4 portions
            yield_unit_id=5,
            target_margin=0.30,
        )
        db_session.add(recipe)
        db_session.commit()
        
        # Add one ingredient
        tomato = sample_ingredients[0]
        item = RecipeItem(
            parent_recipe_id=recipe.id,
            ingredient_id=tomato.id,
            quantity=400.0,  # 400g
            unit_id=2,
        )
        db_session.add(item)
        db_session.commit()
        db_session.refresh(recipe)
        
        # Total cost: (150/1000)/0.85 * 400 = 70.59
        # Cost per portion: 70.59 / 4 = 17.65
        expected_cost_per_portion = 17.65
        assert recipe.cost_per_portion == pytest.approx(expected_cost_per_portion, rel=0.01)
    
    def test_recipe_suggested_price(self, db_session, sample_units, sample_ingredients):
        """Test suggested price calculation based on margin"""
        recipe = Recipe(
            name="Dish",
            recipe_type=RecipeType.FINAL_DISH,
            yield_quantity=1.0,
            yield_unit_id=5,
            target_margin=0.35,  # 35% margin
        )
        db_session.add(recipe)
        db_session.commit()
        
        tomato = sample_ingredients[0]
        item = RecipeItem(
            parent_recipe_id=recipe.id,
            ingredient_id=tomato.id,
            quantity=100.0,
            unit_id=2,
        )
        db_session.add(item)
        db_session.commit()
        db_session.refresh(recipe)
        
        # Cost: (150/1000)/0.85 * 100 = 17.65
        # Suggested price: 17.65 / (1 - 0.35) = 27.15
        expected_price = 27.15
        assert recipe.suggested_price == pytest.approx(expected_price, rel=0.01)
    
    def test_recipe_recursive_cost_with_subrecipe(self, db_session, sample_recipes):
        """Test recursive cost calculation with sub-recipes"""
        pasta_dish = sample_recipes[1]  # Has tomato sauce as sub-recipe
        
        # The pasta dish should include the cost of the tomato sauce
        assert pasta_dish.total_cost > 0
        assert len(pasta_dish.items) > 0
    
    def test_recipe_with_zero_yield_quantity(self, db_session, sample_units):
        """Test that zero yield quantity returns 0 for cost per portion"""
        recipe = Recipe(
            name="Test",
            recipe_type=RecipeType.FINAL_DISH,
            yield_quantity=0.0,  # Invalid but should handle gracefully
            yield_unit_id=5,
        )
        db_session.add(recipe)
        db_session.commit()
        
        assert recipe.cost_per_portion == 0.0


class TestEventModel:
    """Tests for Event model"""
    
    def test_event_total_cost_from_orders(self, db_session, sample_events):
        """Test total cost calculation from event orders"""
        event = sample_events[0]
        
        # Event has 100 portions at cost_at_sale
        assert event.total_cost > 0
        assert len(event.orders) > 0
    
    def test_event_total_revenue(self, db_session, sample_events):
        """Test total revenue calculation"""
        event = sample_events[0]
        
        # 100 portions * $150 = $15,000
        expected_revenue = 15000.0
        assert event.total_revenue == pytest.approx(expected_revenue, rel=0.01)
    
    def test_event_margin_calculation(self, db_session, sample_events):
        """Test margin calculation"""
        event = sample_events[0]
        
        # Margin = (Revenue - Cost) / Revenue
        margin = event.margin
        assert 0 <= margin <= 1  # Margin should be between 0 and 1
    
    def test_event_with_no_orders_has_zero_cost(self, db_session, sample_units):
        """Test that event with no orders has zero cost"""
        event = Event(
            event_number="EVT-TEST-001",
            name="Test Event",
            client_name="Test Client",
            event_date="2025-12-31",
            guest_count=50,
            status=EventStatus.PROSPECT,
        )
        db_session.add(event)
        db_session.commit()
        
        assert event.total_cost == 0.0
        assert event.total_revenue == 0.0
        assert event.margin == 0.0


class TestEventOrderModel:
    """Tests for EventOrder model"""
    
    def test_event_order_total_price(self, db_session, sample_events):
        """Test total price calculation for event order"""
        event = sample_events[0]
        order = event.orders[0]
        
        # 100 portions * $150 = $15,000
        expected_total = 15000.0
        assert order.total_price == pytest.approx(expected_total, rel=0.01)
    
    def test_event_order_total_cost(self, db_session, sample_events):
        """Test total cost calculation for event order"""
        event = sample_events[0]
        order = event.orders[0]
        
        # Should be quantity * cost_at_sale
        assert order.total_cost > 0
    
    def test_event_order_margin(self, db_session, sample_events):
        """Test margin calculation for event order"""
        event = sample_events[0]
        order = event.orders[0]
        
        margin = order.margin
        assert 0 <= margin <= 1
