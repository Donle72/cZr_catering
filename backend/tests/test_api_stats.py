"""
Tests for API endpoints - Statistics
"""
import pytest
from fastapi import status


class TestStatsAPI:
    """Tests for /api/v1/stats endpoints"""
    
    def test_dashboard_stats(self, client, sample_events, sample_ingredients):
        """Test GET /stats/dashboard - Get dashboard statistics"""
        response = client.get("/api/v1/stats/dashboard")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Check expected fields
        assert "total_events" in data
        assert "total_revenue" in data
        assert "total_ingredients" in data
        assert "low_stock_count" in data
        
        # Verify counts
        assert data["total_events"] >= 1
        assert data["total_ingredients"] >= 4
    
    def test_inventory_stats(self, client, sample_ingredients):
        """Test GET /stats/inventory - Get inventory statistics"""
        response = client.get("/api/v1/stats/inventory")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Check expected fields
        assert "total_items" in data
        assert "total_value" in data
        assert "low_stock_items" in data
        assert "by_category" in data
        
        # Verify structure
        assert isinstance(data["by_category"], list)
        if len(data["by_category"]) > 0:
            category = data["by_category"][0]
            assert "category" in category
            assert "count" in category
            assert "total_value" in category


class TestHealthCheck:
    """Tests for health check endpoint"""
    
    def test_health_check_returns_healthy(self, client):
        """Test GET /health - Health check"""
        response = client.get("/health")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["status"] == "healthy"
        assert "checks" in data
        assert "database" in data["checks"]
        assert data["checks"]["database"]["status"] == "healthy"
    
    def test_root_endpoint(self, client):
        """Test GET / - Root endpoint"""
        response = client.get("/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "message" in data
        assert "version" in data
        assert "status" in data
        assert data["status"] == "operational"
