"""
Tests for API endpoints - Assets (Logistics)
"""
import pytest
from fastapi import status


class TestAssetsAPI:
    """Tests for /api/v1/assets endpoints"""
    
    def test_list_assets(self, client):
        """Test GET /assets/ - List all assets"""
        response = client.get("/api/v1/assets/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
    
    def test_create_asset(self, client):
        """Test POST /assets/ - Create new asset"""
        new_asset = {
            "name": "Chafing Dish",
            "asset_type": "equipment",
            "category": "Serving",
            "quantity_available": 20,
            "unit_cost": 150.0,
            "status": "available",
            "location": "Warehouse A",
        }
        
        response = client.post("/api/v1/assets/", json=new_asset)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Chafing Dish"
        assert data["quantity_available"] == 20
        assert "id" in data
    
    def test_get_asset_by_id(self, client):
        """Test GET /assets/{id} - Get single asset"""
        # First create an asset
        new_asset = {
            "name": "Table",
            "asset_type": "furniture",
            "category": "Setup",
            "quantity_available": 10,
            "unit_cost": 200.0,
            "status": "available",
        }
        
        create_response = client.post("/api/v1/assets/", json=new_asset)
        asset_id = create_response.json()["id"]
        
        # Now get it
        response = client.get(f"/api/v1/assets/{asset_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == asset_id
        assert data["name"] == "Table"
    
    def test_update_asset(self, client):
        """Test PUT /assets/{id} - Update asset"""
        # Create asset
        new_asset = {
            "name": "Chair",
            "asset_type": "furniture",
            "category": "Setup",
            "quantity_available": 50,
            "unit_cost": 50.0,
            "status": "available",
        }
        
        create_response = client.post("/api/v1/assets/", json=new_asset)
        asset_id = create_response.json()["id"]
        
        # Update it
        update_data = {
            "quantity_available": 45,
            "status": "in_use",
        }
        
        response = client.put(f"/api/v1/assets/{asset_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["quantity_available"] == 45
        assert data["status"] == "in_use"
    
    def test_delete_asset(self, client):
        """Test DELETE /assets/{id} - Delete asset"""
        # Create asset
        new_asset = {
            "name": "Temporary Item",
            "asset_type": "equipment",
            "category": "Test",
            "quantity_available": 1,
            "unit_cost": 10.0,
            "status": "available",
        }
        
        create_response = client.post("/api/v1/assets/", json=new_asset)
        asset_id = create_response.json()["id"]
        
        # Delete it
        response = client.delete(f"/api/v1/assets/{asset_id}")
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify it's deleted
        get_response = client.get(f"/api/v1/assets/{asset_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_filter_assets_by_status(self, client):
        """Test filtering assets by status"""
        response = client.get("/api/v1/assets/?status=available")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # All returned assets should have status 'available'
        if len(data) > 0:
            assert all(asset["status"] == "available" for asset in data)


class TestEventAssets:
    """Tests for event asset assignments"""
    
    def test_assign_asset_to_event(self, client, sample_events):
        """Test assigning assets to events"""
        # Create an asset
        new_asset = {
            "name": "Event Table",
            "asset_type": "furniture",
            "category": "Setup",
            "quantity_available": 20,
            "unit_cost": 100.0,
            "status": "available",
        }
        
        asset_response = client.post("/api/v1/assets/", json=new_asset)
        asset_id = asset_response.json()["id"]
        
        # This would test EventAsset assignment if endpoint exists
        # For now, just verify asset was created
        assert asset_response.status_code == status.HTTP_200_OK
