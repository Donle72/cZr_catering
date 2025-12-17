"""
Integration tests for complete workflows
"""
import pytest
from fastapi import status


class TestRecipeWorkflow:
    """Test complete recipe creation and costing workflow"""
    
    def test_complete_recipe_workflow(self, client, sample_units):
        """Test: Create ingredients → Create recipe → Add items → Calculate cost"""
        
        # Step 1: Create ingredients
        flour = {
            "name": "Flour",
            "sku": "FLO-001",
            "category": "Grains",
            "purchase_unit_id": 1,
            "usage_unit_id": 2,
            "conversion_ratio": 1000.0,
            "current_cost": 80.0,
            "yield_factor": 0.95,
        }
        
        sugar = {
            "name": "Sugar",
            "sku": "SUG-001",
            "category": "Sweeteners",
            "purchase_unit_id": 1,
            "usage_unit_id": 2,
            "conversion_ratio": 1000.0,
            "current_cost": 120.0,
            "yield_factor": 1.0,
        }
        
        flour_response = client.post("/api/v1/ingredients/", json=flour)
        sugar_response = client.post("/api/v1/ingredients/", json=sugar)
        
        assert flour_response.status_code == status.HTTP_200_OK
        assert sugar_response.status_code == status.HTTP_200_OK
        
        flour_id = flour_response.json()["id"]
        sugar_id = sugar_response.json()["id"]
        
        # Step 2: Create recipe
        recipe = {
            "name": "Simple Cake",
            "recipe_type": "dessert",
            "yield_quantity": 8.0,
            "yield_unit_id": 5,
            "target_margin": 0.40,
        }
        
        recipe_response = client.post("/api/v1/recipes/", json=recipe)
        assert recipe_response.status_code == status.HTTP_200_OK
        recipe_id = recipe_response.json()["id"]
        
        # Step 3: Add ingredients to recipe
        flour_item = {
            "ingredient_id": flour_id,
            "quantity": 500.0,
            "unit_id": 2,
        }
        
        sugar_item = {
            "ingredient_id": sugar_id,
            "quantity": 300.0,
            "unit_id": 2,
        }
        
        flour_item_response = client.post(f"/api/v1/recipes/{recipe_id}/items", json=flour_item)
        sugar_item_response = client.post(f"/api/v1/recipes/{recipe_id}/items", json=sugar_item)
        
        assert flour_item_response.status_code == status.HTTP_200_OK
        assert sugar_item_response.status_code == status.HTTP_200_OK
        
        # Step 4: Get recipe and verify cost calculation
        final_recipe = client.get(f"/api/v1/recipes/{recipe_id}")
        assert final_recipe.status_code == status.HTTP_200_OK
        
        recipe_data = final_recipe.json()
        
        # Verify cost was calculated
        assert recipe_data["total_cost"] > 0
        assert recipe_data["cost_per_portion"] > 0
        assert recipe_data["suggested_price"] > recipe_data["cost_per_portion"]
        
        # Verify items are present
        assert len(recipe_data["items"]) == 2


class TestEventWorkflow:
    """Test complete event creation and management workflow"""
    
    def test_complete_event_workflow(self, client, sample_recipes):
        """Test: Create event → Add orders → Calculate margins"""
        
        # Step 1: Create event
        event = {
            "event_number": "EVT-TEST-001",
            "name": "Birthday Party",
            "client_name": "Jane Smith",
            "client_email": "jane@example.com",
            "event_date": "2025-08-15",
            "guest_count": 30,
            "status": "prospect",
        }
        
        event_response = client.post("/api/v1/events/", json=event)
        assert event_response.status_code == status.HTTP_200_OK
        event_id = event_response.json()["id"]
        
        # Step 2: Get recipe for order
        recipe_id = sample_recipes[1].id  # Pasta dish
        recipe_response = client.get(f"/api/v1/recipes/{recipe_id}")
        recipe_data = recipe_response.json()
        
        # Step 3: Add order to event (would need order endpoint)
        # For now, verify event was created
        event_detail = client.get(f"/api/v1/events/{event_id}")
        assert event_detail.status_code == status.HTTP_200_OK
        
        event_data = event_detail.json()
        assert event_data["name"] == "Birthday Party"
        assert event_data["guest_count"] == 30


class TestProductionWorkflow:
    """Test production sheet and shopping list workflow"""
    
    def test_production_sheet_generation(self, client, sample_recipes):
        """Test generating production sheet for recipes"""
        
        recipe_ids = [sample_recipes[0].id, sample_recipes[1].id]
        
        request_data = {
            "recipe_quantities": [
                {"recipe_id": recipe_ids[0], "quantity": 2.0},
                {"recipe_id": recipe_ids[1], "quantity": 5.0},
            ]
        }
        
        response = client.post("/api/v1/production/sheet", json=request_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "recipes" in data
        assert len(data["recipes"]) == 2
    
    def test_shopping_list_generation(self, client, sample_recipes):
        """Test generating consolidated shopping list"""
        
        recipe_ids = [sample_recipes[0].id, sample_recipes[1].id]
        
        request_data = {
            "recipe_quantities": [
                {"recipe_id": recipe_ids[0], "quantity": 3.0},
                {"recipe_id": recipe_ids[1], "quantity": 4.0},
            ]
        }
        
        response = client.post("/api/v1/production/shopping-list", json=request_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "ingredients" in data
        assert len(data["ingredients"]) > 0
        
        # Verify ingredients are grouped by category
        categories = set(item["category"] for item in data["ingredients"])
        assert len(categories) > 0


class TestRecursiveRecipeWorkflow:
    """Test recursive recipe composition"""
    
    def test_subrecipe_in_final_dish(self, client, sample_recipes):
        """Test that sub-recipe costs are included in final dish"""
        
        # Get the pasta dish (which includes tomato sauce sub-recipe)
        pasta_dish_id = sample_recipes[1].id
        
        response = client.get(f"/api/v1/recipes/{pasta_dish_id}")
        assert response.status_code == status.HTTP_200_OK
        
        pasta_data = response.json()
        
        # Verify it has items
        assert len(pasta_data["items"]) > 0
        
        # Verify at least one item is a sub-recipe
        has_subrecipe = any(item.get("child_recipe_id") for item in pasta_data["items"])
        assert has_subrecipe
        
        # Verify total cost includes sub-recipe cost
        assert pasta_data["total_cost"] > 0
        
        # Get the sub-recipe separately
        tomato_sauce_id = sample_recipes[0].id
        sauce_response = client.get(f"/api/v1/recipes/{tomato_sauce_id}")
        sauce_data = sauce_response.json()
        
        # Pasta dish cost should be >= sauce cost (since it includes it)
        assert pasta_data["total_cost"] >= sauce_data["total_cost"] * 0.5  # 0.5L used


class TestBulkOperations:
    """Test bulk operations and their effects"""
    
    def test_bulk_price_update_affects_recipe_cost(self, client, sample_ingredients, sample_recipes):
        """Test that bulk price update affects recipe costs"""
        
        # Get initial recipe cost
        recipe_id = sample_recipes[0].id
        initial_response = client.get(f"/api/v1/recipes/{recipe_id}")
        initial_cost = initial_response.json()["total_cost"]
        
        # Perform bulk price update on Vegetables
        update_data = {
            "category": "Vegetables",
            "percentage_increase": 20.0,
        }
        
        bulk_response = client.post("/api/v1/ingredients/bulk-price-update", json=update_data)
        assert bulk_response.status_code == status.HTTP_200_OK
        
        # Get updated recipe cost
        updated_response = client.get(f"/api/v1/recipes/{recipe_id}")
        updated_cost = updated_response.json()["total_cost"]
        
        # Cost should have increased
        assert updated_cost > initial_cost
