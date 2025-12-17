"""
Tests for API endpoints - Ingredients
"""
import pytest
from fastapi import status


class TestIngredientsAPI:
    """Tests for /api/v1/ingredients endpoints"""
    
    def test_list_ingredients(self, client, sample_ingredients):
        """Test GET /ingredients/ - List all ingredients"""
        response = client.get("/api/v1/ingredients/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Check pagination structure
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "page_size" in data
        
        # Check we have ingredients
        assert len(data["items"]) == 4  # We have 4 sample ingredients
        assert data["total"] == 4
        
        # Check first ingredient structure
        first = data["items"][0]
        assert "id" in first
        assert "name" in first
        assert "sku" in first
        assert "category" in first
        assert "current_cost" in first
        assert "yield_factor" in first
    
    def test_list_ingredients_with_search(self, client, sample_ingredients):
        """Test GET /ingredients/?search=tomato"""
        response = client.get("/api/v1/ingredients/?search=tomato")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) >= 1
        assert any("tomato" in ing["name"].lower() for ing in data["items"])
    
    def test_list_ingredients_with_category_filter(self, client, sample_ingredients):
        """Test GET /ingredients/?category=Vegetables"""
        response = client.get("/api/v1/ingredients/?category=Vegetables")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(ing["category"] == "Vegetables" for ing in data["items"])
    
    def test_create_ingredient(self, client, sample_units):
        """Test POST /ingredients/ - Create new ingredient"""
        new_ingredient = {
            "name": "Carrot",
            "sku": "CAR-001",
            "category": "Vegetables",
            "purchase_unit_id": 1,
            "usage_unit_id": 2,
            "conversion_ratio": 1000.0,
            "current_cost": 120.0,
            "yield_factor": 0.88,
            "stock_quantity": 25.0,
            "min_stock_threshold": 5.0,
        }
        
        response = client.post("/api/v1/ingredients/", json=new_ingredient)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Carrot"
        assert data["sku"] == "CAR-001"
        assert data["yield_factor"] == 0.88
        assert "id" in data
    
    def test_create_ingredient_with_duplicate_sku_fails(self, client, sample_ingredients):
        """Test that creating ingredient with duplicate SKU fails"""
        duplicate_ingredient = {
            "name": "Another Tomato",
            "sku": "TOM-001",  # Duplicate SKU
            "category": "Vegetables",
            "purchase_unit_id": 1,
            "usage_unit_id": 2,
            "conversion_ratio": 1000.0,
            "current_cost": 150.0,
            "yield_factor": 0.85,
        }
        
        response = client.post("/api/v1/ingredients/", json=duplicate_ingredient)
        
        assert response.status_code == status.HTTP_409_CONFLICT
        assert "already exists" in response.json()["message"].lower()
    
    def test_create_ingredient_with_invalid_yield_factor_fails(self, client, sample_units):
        """Test that invalid yield factor is rejected"""
        invalid_ingredient = {
            "name": "Test",
            "sku": "TEST-001",
            "category": "Test",
            "purchase_unit_id": 1,
            "usage_unit_id": 2,
            "conversion_ratio": 1000.0,
            "current_cost": 100.0,
            "yield_factor": 1.5,  # Invalid: > 1.0
        }
        
        response = client.post("/api/v1/ingredients/", json=invalid_ingredient)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_ingredient_by_id(self, client, sample_ingredients):
        """Test GET /ingredients/{id} - Get single ingredient"""
        ingredient_id = sample_ingredients[0].id
        
        response = client.get(f"/api/v1/ingredients/{ingredient_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == ingredient_id
        assert data["name"] == "Tomato"
    
    def test_get_nonexistent_ingredient_returns_404(self, client):
        """Test that getting non-existent ingredient returns 404"""
        response = client.get("/api/v1/ingredients/9999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["message"].lower()
    
    def test_update_ingredient(self, client, sample_ingredients):
        """Test PUT /ingredients/{id} - Update ingredient"""
        ingredient_id = sample_ingredients[0].id
        
        update_data = {
            "name": "Updated Tomato",
            "current_cost": 180.0,
            "yield_factor": 0.90,
        }
        
        response = client.put(f"/api/v1/ingredients/{ingredient_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated Tomato"
        assert data["current_cost"] == 180.0
        assert data["yield_factor"] == 0.90
    
    def test_update_ingredient_with_duplicate_sku_fails(self, client, sample_ingredients):
        """Test that updating to duplicate SKU fails"""
        ingredient_id = sample_ingredients[0].id
        
        update_data = {
            "sku": "ONI-001",  # SKU of second ingredient
        }
        
        response = client.put(f"/api/v1/ingredients/{ingredient_id}", json=update_data)
        
        assert response.status_code == status.HTTP_409_CONFLICT
    
    def test_delete_ingredient(self, client, sample_ingredients):
        """Test DELETE /ingredients/{id} - Delete ingredient"""
        ingredient_id = sample_ingredients[0].id
        
        response = client.delete(f"/api/v1/ingredients/{ingredient_id}")
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify it's deleted
        get_response = client.get(f"/api/v1/ingredients/{ingredient_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_bulk_price_update(self, client, sample_ingredients):
        """Test POST /ingredients/bulk-price-update - Bulk price update"""
        update_data = {
            "category": "Vegetables",
            "percentage_increase": 10.0,  # 10% increase
        }
        
        response = client.post("/api/v1/ingredients/bulk-price-update", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "ingredients_updated" in data
        assert data["ingredients_updated"] == 2  # Tomato and Onion
        assert data["percentage_increase"] == 10.0
        assert "total_cost_before" in data
        assert "total_cost_after" in data
        
        # Verify prices were updated
        tomato_response = client.get(f"/api/v1/ingredients/{sample_ingredients[0].id}")
        tomato = tomato_response.json()
        # Original: 150, +10% = 165
        assert tomato["current_cost"] == pytest.approx(165.0, rel=0.01)
    
    def test_bulk_price_update_with_negative_percentage(self, client, sample_ingredients):
        """Test bulk price update with price decrease"""
        update_data = {
            "category": "Oils",
            "percentage_increase": -20.0,  # 20% decrease
        }
        
        response = client.post("/api/v1/ingredients/bulk-price-update", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["ingredients_updated"] == 1  # Olive Oil
        
        # Verify price decreased
        oil_response = client.get(f"/api/v1/ingredients/{sample_ingredients[2].id}")
        oil = oil_response.json()
        # Original: 500, -20% = 400
        assert oil["current_cost"] == pytest.approx(400.0, rel=0.01)
    
    def test_bulk_price_update_with_invalid_percentage_fails(self, client, sample_ingredients):
        """Test that invalid percentage is rejected"""
        update_data = {
            "category": "Vegetables",
            "percentage_increase": 1500.0,  # Too high
        }
        
        response = client.post("/api/v1/ingredients/bulk-price-update", json=update_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_bulk_price_update_with_nonexistent_category(self, client, sample_ingredients):
        """Test bulk update with category that has no ingredients"""
        update_data = {
            "category": "NonExistentCategory",
            "percentage_increase": 10.0,
        }
        
        response = client.post("/api/v1/ingredients/bulk-price-update", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["ingredients_updated"] == 0
