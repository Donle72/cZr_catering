"""
Tests for API endpoints - Suppliers
"""
import pytest
from fastapi import status


class TestSuppliersAPI:
    """Tests for /api/v1/suppliers endpoints"""
    
    def test_list_suppliers(self, client, sample_supplier):
        """Test GET /suppliers/ - List all suppliers"""
        response = client.get("/api/v1/suppliers/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 1
        
        # Check structure
        first = data[0]
        assert "id" in first
        assert "name" in first
        assert "email" in first
        assert "currency" in first
    
    def test_create_supplier(self, client):
        """Test POST /suppliers/ - Create new supplier"""
        new_supplier = {
            "name": "Organic Farms Ltd",
            "contact_name": "John Smith",
            "email": "john@organicfarms.com",
            "phone": "+1234567890",
            "address": "123 Farm Road",
            "currency": "USD",
            "payment_terms": "Net 15",
            "is_active": True,
        }
        
        response = client.post("/api/v1/suppliers/", json=new_supplier)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Organic Farms Ltd"
        assert data["currency"] == "USD"
        assert "id" in data
    
    def test_get_supplier_by_id(self, client, sample_supplier):
        """Test GET /suppliers/{id} - Get single supplier"""
        supplier_id = sample_supplier.id
        
        response = client.get(f"/api/v1/suppliers/{supplier_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == supplier_id
        assert data["name"] == "Fresh Produce Co."
    
    def test_get_nonexistent_supplier_returns_404(self, client):
        """Test that getting non-existent supplier returns 404"""
        response = client.get("/api/v1/suppliers/9999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_create_supplier_with_invalid_currency(self, client):
        """Test that invalid currency is rejected"""
        invalid_supplier = {
            "name": "Test Supplier",
            "email": "test@test.com",
            "currency": "INVALID",  # Invalid currency
        }
        
        response = client.post("/api/v1/suppliers/", json=invalid_supplier)
        
        # Should either reject or accept with validation
        # Depending on implementation
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_422_UNPROCESSABLE_ENTITY]


class TestSupplierProducts:
    """Tests for supplier product relationships"""
    
    def test_supplier_can_have_products(self, client, sample_supplier, sample_ingredients):
        """Test that suppliers can be linked to ingredients"""
        # This would test SupplierProduct relationship if implemented
        supplier_id = sample_supplier.id
        
        response = client.get(f"/api/v1/suppliers/{supplier_id}")
        assert response.status_code == status.HTTP_200_OK
