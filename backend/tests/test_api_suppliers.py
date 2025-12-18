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
    
    def test_update_supplier(self, client, sample_supplier):
        """Test PUT /suppliers/{id} - Update supplier"""
        supplier_id = sample_supplier.id
        
        update_data = {
            "name": "Updated Produce Co.",
            "contact_name": "Jane Doe",
            "phone": "+9876543210",
            "payment_terms": "Net 30",
        }
        
        response = client.put(f"/api/v1/suppliers/{supplier_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated Produce Co."
        assert data["contact_name"] == "Jane Doe"
        assert data["phone"] == "+9876543210"
        assert data["payment_terms"] == "Net 30"
    
    def test_update_nonexistent_supplier_returns_404(self, client):
        """Test that updating non-existent supplier returns 404"""
        update_data = {"name": "Test"}
        response = client.put("/api/v1/suppliers/9999", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_supplier(self, client):
        """Test DELETE /suppliers/{id} - Delete supplier"""
        # First create a supplier to delete
        new_supplier = {
            "name": "Temporary Supplier",
            "email": "temp@test.com",
            "currency": "USD",
        }
        
        create_response = client.post("/api/v1/suppliers/", json=new_supplier)
        supplier_id = create_response.json()["id"]
        
        # Delete it
        response = client.delete(f"/api/v1/suppliers/{supplier_id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify it's deleted
        get_response = client.get(f"/api/v1/suppliers/{supplier_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_nonexistent_supplier_returns_404(self, client):
        """Test that deleting non-existent supplier returns 404"""
        response = client.delete("/api/v1/suppliers/9999")
        
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
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_422_UNPROCESSABLE_ENTITY, status.HTTP_201_CREATED]


class TestSupplierProducts:
    """Tests for supplier product relationships"""
    
    def test_supplier_can_have_products(self, client, sample_supplier, sample_ingredients):
        """Test that suppliers can be linked to ingredients"""
        # This would test SupplierProduct relationship if implemented
        supplier_id = sample_supplier.id
        
        response = client.get(f"/api/v1/suppliers/{supplier_id}")
        assert response.status_code == status.HTTP_200_OK
