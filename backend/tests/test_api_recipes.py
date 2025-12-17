"""
Tests for API endpoints - Recipes
"""
import pytest
from fastapi import status


class TestRecipesAPI:
    """Tests for /api/v1/recipes endpoints"""
    
    def test_list_recipes(self, client, sample_recipes):
        """Test GET /recipes/ - List all recipes"""
        response = client.get("/api/v1/recipes/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 2  # At least our sample recipes
        
        # Check structure
        first = data[0]
        assert "id" in first
        assert "name" in first
        assert "recipe_type" in first
        assert "yield_quantity" in first
    
    def test_create_recipe(self, client, sample_units):
        """Test POST /recipes/ - Create new recipe"""
        new_recipe = {
            "name": "Caesar Salad",
            "description": "Classic Caesar salad",
            "recipe_type": "final_dish",
            "yield_quantity": 4.0,
            "yield_unit_id": 5,
            "target_margin": 0.40,
            "preparation_time": 20,
        }
        
        response = client.post("/api/v1/recipes/", json=new_recipe)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Caesar Salad"
        assert data["recipe_type"] == "final_dish"
        assert data["target_margin"] == 0.40
        assert "id" in data
    
    def test_get_recipe_by_id(self, client, sample_recipes):
        """Test GET /recipes/{id} - Get recipe with items"""
        recipe_id = sample_recipes[0].id  # Tomato Sauce
        
        response = client.get(f"/api/v1/recipes/{recipe_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == recipe_id
        assert data["name"] == "Tomato Sauce"
        assert "items" in data
        assert len(data["items"]) > 0  # Should have ingredients
    
    def test_get_recipe_shows_total_cost(self, client, sample_recipes):
        """Test that recipe detail includes calculated costs"""
        recipe_id = sample_recipes[0].id
        
        response = client.get(f"/api/v1/recipes/{recipe_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "total_cost" in data
        assert "cost_per_portion" in data
        assert "suggested_price" in data
        assert data["total_cost"] > 0
    
    def test_add_ingredient_to_recipe(self, client, sample_recipes, sample_ingredients):
        """Test POST /recipes/{id}/items - Add ingredient to recipe"""
        recipe_id = sample_recipes[0].id
        tomato_id = sample_ingredients[0].id
        
        new_item = {
            "ingredient_id": tomato_id,
            "quantity": 150.0,
            "unit_id": 2,  # grams
            "notes": "Fresh tomatoes",
        }
        
        response = client.post(f"/api/v1/recipes/{recipe_id}/items", json=new_item)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "id" in data
        assert data["ingredient_id"] == tomato_id
        assert data["quantity"] == 150.0
    
    def test_add_subrecipe_to_recipe(self, client, sample_recipes):
        """Test adding a sub-recipe to a recipe"""
        parent_recipe_id = sample_recipes[1].id  # Pasta dish
        subrecipe_id = sample_recipes[0].id  # Tomato sauce
        
        new_item = {
            "child_recipe_id": subrecipe_id,
            "quantity": 0.3,
            "unit_id": 3,  # liters
            "notes": "Homemade tomato sauce",
        }
        
        response = client.post(f"/api/v1/recipes/{parent_recipe_id}/items", json=new_item)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["child_recipe_id"] == subrecipe_id
        assert data["quantity"] == 0.3
    
    def test_add_item_without_ingredient_or_subrecipe_fails(self, client, sample_recipes):
        """Test that adding item without ingredient or sub-recipe fails"""
        recipe_id = sample_recipes[0].id
        
        invalid_item = {
            "quantity": 100.0,
            "unit_id": 2,
        }
        
        response = client.post(f"/api/v1/recipes/{recipe_id}/items", json=invalid_item)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_add_item_with_both_ingredient_and_subrecipe_fails(self, client, sample_recipes, sample_ingredients):
        """Test that adding item with both ingredient and sub-recipe fails"""
        recipe_id = sample_recipes[0].id
        
        invalid_item = {
            "ingredient_id": sample_ingredients[0].id,
            "child_recipe_id": sample_recipes[1].id,
            "quantity": 100.0,
            "unit_id": 2,
        }
        
        response = client.post(f"/api/v1/recipes/{recipe_id}/items", json=invalid_item)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_remove_item_from_recipe(self, client, sample_recipes):
        """Test DELETE /recipes/{id}/items/{item_id} - Remove item"""
        recipe = sample_recipes[0]
        item_id = recipe.items[0].id
        
        response = client.delete(f"/api/v1/recipes/{recipe.id}/items/{item_id}")
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify item was removed
        recipe_response = client.get(f"/api/v1/recipes/{recipe.id}")
        recipe_data = recipe_response.json()
        item_ids = [item["id"] for item in recipe_data["items"]]
        assert item_id not in item_ids
    
    def test_update_recipe(self, client, sample_recipes):
        """Test PUT /recipes/{id} - Update recipe"""
        recipe_id = sample_recipes[0].id
        
        update_data = {
            "name": "Updated Tomato Sauce",
            "target_margin": 0.40,
            "preparation_time": 45,
        }
        
        response = client.put(f"/api/v1/recipes/{recipe_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated Tomato Sauce"
        assert data["target_margin"] == 0.40
        assert data["preparation_time"] == 45
    
    def test_get_nonexistent_recipe_returns_404(self, client):
        """Test that getting non-existent recipe returns 404"""
        response = client.get("/api/v1/recipes/9999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestRecipeCalculations:
    """Tests for recipe cost calculations via API"""
    
    def test_recipe_with_ingredients_calculates_cost(self, client, sample_recipes):
        """Test that recipe with ingredients shows correct total cost"""
        recipe_id = sample_recipes[0].id  # Tomato Sauce
        
        response = client.get(f"/api/v1/recipes/{recipe_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Should have cost calculated from ingredients
        assert data["total_cost"] > 0
        assert data["cost_per_portion"] > 0
        assert data["suggested_price"] > data["cost_per_portion"]
    
    def test_recipe_with_subrecipe_includes_subrecipe_cost(self, client, sample_recipes):
        """Test that recipe with sub-recipe includes sub-recipe cost"""
        recipe_id = sample_recipes[1].id  # Pasta dish (has tomato sauce)
        
        response = client.get(f"/api/v1/recipes/{recipe_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Should include cost from sub-recipe
        assert data["total_cost"] > 0
        
        # Check that it has a sub-recipe item
        has_subrecipe = any(item.get("child_recipe_id") for item in data["items"])
        assert has_subrecipe
