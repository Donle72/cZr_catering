"""
Tests for custom exceptions and error handling
Covers exception responses and error formatting
"""
import pytest
from fastapi import status


class TestExceptionHandling:
    """Test custom exception handling"""
    
    def test_resource_not_found_error_format(self, client):
        """Test ResourceNotFoundError returns proper format"""
        response = client.get("/api/v1/ingredients/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        
        # Check error structure
        assert "error" in data
        assert "message" in data
        assert "details" in data
        assert "path" in data
        assert "timestamp" in data
        
        # Check error type
        assert data["error"] == "ResourceNotFoundError"
        assert "999" in data["message"]
    
    def test_duplicate_resource_error_format(self, client, sample_ingredient_data):
        """Test DuplicateResourceError returns proper format"""
        # Create first ingredient
        client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        
        # Try to create duplicate
        response = client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        
        assert response.status_code == status.HTTP_409_CONFLICT
        data = response.json()
        
        assert data["error"] == "DuplicateResourceError"
        assert "sku" in data["message"].lower()
        assert data["details"]["field"] == "sku"
    
    def test_validation_error_format(self, client, sample_ingredient_data):
        """Test validation errors return proper format"""
        sample_ingredient_data["yield_factor"] = 1.5  # Invalid
        
        response = client.post("/api/v1/ingredients/", json=sample_ingredient_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        
        assert "error" in data
        assert "errors" in data or "message" in data
    
    def test_error_includes_path(self, client):
        """Test that errors include the request path"""
        response = client.get("/api/v1/ingredients/999")
        
        data = response.json()
        assert data["path"] == "/api/v1/ingredients/999"
    
    def test_error_includes_timestamp(self, client):
        """Test that errors include a timestamp"""
        response = client.get("/api/v1/ingredients/999")
        
        data = response.json()
        assert "timestamp" in data
        # Check it's ISO format
        assert "T" in data["timestamp"]
    
    def test_multiple_validation_errors(self, client):
        """Test multiple validation errors are reported"""
        invalid_data = {
            "name": "AB",  # Too short
            "yield_factor": 1.5,  # Too high
            "current_cost": -100,  # Negative
            "purchase_unit_id": 1,
            "usage_unit_id": 1
        }
        
        response = client.post("/api/v1/ingredients/", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        
        # Should have multiple errors
        if "errors" in data:
            assert len(data["errors"]) >= 2


class TestHealthCheck:
    """Test health check endpoint"""
    
    def test_health_check_success(self, client):
        """Test health check returns healthy status"""
        response = client.get("/health")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["status"] == "healthy"
        assert "checks" in data
        assert "database" in data["checks"]
        assert data["checks"]["database"]["status"] == "healthy"
    
    def test_health_check_includes_metadata(self, client):
        """Test health check includes system metadata"""
        response = client.get("/health")
        data = response.json()
        
        assert "timestamp" in data
        assert "environment" in data
        assert "version" in data


class TestRootEndpoint:
    """Test root API endpoint"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns API info"""
        response = client.get("/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "message" in data
        assert "version" in data
        assert "docs" in data
        assert "health" in data
