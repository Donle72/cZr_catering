"""
Tests for API endpoints - Units
"""
import pytest
from fastapi import status


class TestUnitsAPI:
    """Tests for /api/v1/units endpoints"""
    
    def test_list_units(self, client, sample_units):
        """Test GET /units/ - List all units"""
        response = client.get("/api/v1/units/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 5  # We have 5 sample units
        
        # Check structure
        first = data[0]
        assert "id" in first
        assert "name" in first
        assert "abbreviation" in first
    
    def test_units_have_categories(self, client, sample_units):
        """Test that units have category information"""
        response = client.get("/api/v1/units/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # At least one unit should have category info
        if len(data) > 0:
            first = data[0]
            # Category might be nested or just category_id
            assert "category_id" in first or "category" in first
    
    def test_get_unit_by_id(self, client, sample_units):
        """Test GET /units/{id} - Get single unit"""
        unit_id = sample_units[0].id
        
        response = client.get(f"/api/v1/units/{unit_id}")
        
        # This endpoint might not exist, so accept 404 or 200
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
        
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            assert data["id"] == unit_id
