"""
Tests for Ingredients API endpoints
Covers CRUD operations, validations, and business logic
"""
import pytest
from fastapi import status


class TestIngredientsAPI:
    """Test suite for ingredients endpoints"""
    
    def test_create_ingredient_success(self, client, sample_ingredient_data):
        """Test successful ingredient creation"""
        response = client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == sample_ingredient_data["name"]
        assert data["sku"] == sample_ingredient_data["sku"]
        assert data["yield_factor"] == sample_ingredient_data["yield_factor"]
        assert "id" in data
    
    def test_create_ingredient_duplicate_sku(self, client, sample_ingredient_data):
        """Test that duplicate SKU returns 409 error"""
        # Create first ingredient
        client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        
        # Try to create duplicate
        response = client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        
        assert response.status_code == status.HTTP_409_CONFLICT
        data = response.json()
        assert "error" in data
        assert data["error"] == "DuplicateResourceError"
    
    def test_create_ingredient_invalid_yield_factor(self, client, sample_ingredient_data):
        """Test validation of yield factor > 1.0"""
        sample_ingredient_data["yield_factor"] = 1.5
        
        response = client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        assert "error" in data
    
    def test_create_ingredient_negative_cost(self, client, sample_ingredient_data):
        """Test validation of negative cost"""
        sample_ingredient_data["current_cost"] = -100.0
        
        response = client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_ingredient_short_name(self, client, sample_ingredient_data):
        """Test validation of name length"""
        sample_ingredient_data["name"] = "AB"  # Too short
        
        response = client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_list_ingredients_empty(self, client):
        """Test listing ingredients when database is empty"""
        response = client.get("/api/v1/ingredients/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
    
    def test_list_ingredients_with_data(self, client, sample_ingredient_data):
        """Test listing ingredients with data"""
        # Create some ingredients
        client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        
        sample_ingredient_data["sku"] = "TOM-002"
        sample_ingredient_data["name"] = "Test Onion"
        client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        
        response = client.get("/api/v1/ingredients/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 2
    
    def test_list_ingredients_pagination(self, client, sample_ingredient_data):
        """Test pagination of ingredients list"""
        # Create 5 ingredients
        for i in range(5):
            sample_ingredient_data["sku"] = f"TOM-{i:03d}"
            sample_ingredient_data["name"] = f"Test Ingredient {i}"
            client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        
        # Get first page (limit 2)
        response = client.get("/api/v1/ingredients/?skip=0&limit=2")
        data = response.json()
        
        assert len(data["items"]) == 2
        assert data["total"] == 5
        assert data["page"] == 1
        assert data["pages"] == 3
    
    def test_list_ingredients_filter_by_category(self, client, sample_ingredient_data):
        """Test filtering ingredients by category"""
        # Create vegetables
        sample_ingredient_data["category"] = "Vegetables"
        sample_ingredient_data["sku"] = "VEG-001"
        client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        
        # Create meats
        sample_ingredient_data["category"] = "Meats"
        sample_ingredient_data["sku"] = "MEAT-001"
        sample_ingredient_data["name"] = "Test Beef"
        client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        
        # Filter by Vegetables
        response = client.get("/api/v1/ingredients/?category=Vegetables")
        data = response.json()
        
        assert len(data["items"]) == 1
        assert data["items"][0]["category"] == "Vegetables"
    
    def test_list_ingredients_search(self, client, sample_ingredient_data):
        """Test search functionality"""
        sample_ingredient_data["name"] = "Red Tomato"
        sample_ingredient_data["sku"] = "TOM-001"
        client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        
        sample_ingredient_data["name"] = "Green Pepper"
        sample_ingredient_data["sku"] = "PEP-001"
        client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        
        # Search by name
        response = client.get("/api/v1/ingredients/?search=Tomato")
        data = response.json()
        
        assert len(data["items"]) == 1
        assert "Tomato" in data["items"][0]["name"]
    
    def test_get_ingredient_success(self, client, sample_ingredient_data):
        """Test getting a specific ingredient"""
        # Create ingredient
        create_response = client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        ingredient_id = create_response.json()["id"]
        
        # Get ingredient
        response = client.get(f"/api/v1/ingredients/{ingredient_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == ingredient_id
        assert data["name"] == sample_ingredient_data["name"]
    
    def test_get_ingredient_not_found(self, client):
        """Test getting non-existent ingredient returns 404"""
        response = client.get("/api/v1/ingredients/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["error"] == "ResourceNotFoundError"
    
    def test_update_ingredient_success(self, client, sample_ingredient_data):
        """Test successful ingredient update"""
        # Create ingredient
        create_response = client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        ingredient_id = create_response.json()["id"]
        
        # Update ingredient
        update_data = {"name": "Updated Tomato", "current_cost": 150.0}
        response = client.put(f"/api/v1/ingredients/{ingredient_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated Tomato"
        assert data["current_cost"] == 150.0
    
    def test_update_ingredient_not_found(self, client):
        """Test updating non-existent ingredient"""
        update_data = {"name": "Updated"}
        response = client.put("/api/v1/ingredients/999", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_ingredient_duplicate_sku(self, client, sample_ingredient_data):
        """Test that updating to duplicate SKU fails"""
        # Create first ingredient
        client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        
        # Create second ingredient
        sample_ingredient_data["sku"] = "TOM-002"
        sample_ingredient_data["name"] = "Second Tomato"
        create_response = client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        ingredient_id = create_response.json()["id"]
        
        # Try to update second to first's SKU
        update_data = {"sku": "TOM-001"}
        response = client.put(f"/api/v1/ingredients/{ingredient_id}", json=update_data)
        
        assert response.status_code == status.HTTP_409_CONFLICT
    
    def test_delete_ingredient_success(self, client, sample_ingredient_data):
        """Test successful ingredient deletion"""
        # Create ingredient
        create_response = client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        ingredient_id = create_response.json()["id"]
        
        # Delete ingredient
        response = client.delete(f"/api/v1/ingredients/{ingredient_id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify it's deleted
        get_response = client.get(f"/api/v1/ingredients/{ingredient_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_ingredient_not_found(self, client):
        """Test deleting non-existent ingredient"""
        response = client.delete("/api/v1/ingredients/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_bulk_price_update_all(self, client, sample_ingredient_data):
        """Test bulk price update for all ingredients"""
        # Create ingredients
        for i in range(3):
            sample_ingredient_data["sku"] = f"ING-{i:03d}"
            sample_ingredient_data["name"] = f"Ingredient {i}"
            sample_ingredient_data["current_cost"] = 100.0
            client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        
        # Update all by 10%
        response = client.post("/api/v1/ingredients/bulk-price-update?percentage_increase=10")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["ingredients_updated"] == 3
        assert data["multiplier"] == 1.1
        assert data["total_cost_before"] == 300.0
        assert data["total_cost_after"] == 330.0
    
    def test_bulk_price_update_by_category(self, client, sample_ingredient_data):
        """Test bulk price update filtered by category"""
        # Create vegetables
        sample_ingredient_data["category"] = "Vegetables"
        sample_ingredient_data["sku"] = "VEG-001"
        sample_ingredient_data["current_cost"] = 100.0
        client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        
        # Create meats
        sample_ingredient_data["category"] = "Meats"
        sample_ingredient_data["sku"] = "MEAT-001"
        sample_ingredient_data["current_cost"] = 200.0
        client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        
        # Update only vegetables
        response = client.post(
            "/api/v1/ingredients/bulk-price-update?category=Vegetables&percentage_increase=20"
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["ingredients_updated"] == 1
        assert data["category"] == "Vegetables"
    
    def test_bulk_price_update_no_ingredients(self, client):
        """Test bulk update when no ingredients match"""
        response = client.post(
            "/api/v1/ingredients/bulk-price-update?category=NonExistent&percentage_increase=10"
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_bulk_price_update_negative_percentage(self, client, sample_ingredient_data):
        """Test bulk update with price decrease"""
        # Create ingredient
        sample_ingredient_data["current_cost"] = 100.0
        client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        
        # Decrease by 10%
        response = client.post("/api/v1/ingredients/bulk-price-update?percentage_increase=-10")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["multiplier"] == 0.9
        assert data["total_cost_after"] == 90.0
    
    def test_bulk_price_update_invalid_percentage(self, client):
        """Test bulk update with invalid percentage"""
        response = client.post("/api/v1/ingredients/bulk-price-update?percentage_increase=-150")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
