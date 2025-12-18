"""
Tests for API endpoints - Events
"""
import pytest
from fastapi import status


class TestEventsAPI:
    """Tests for /api/v1/events endpoints"""
    
    def test_list_events(self, client, sample_events):
        """Test GET /events/ - List all events"""
        response = client.get("/api/v1/events/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 1
        
        # Check structure
        first = data[0]
        assert "id" in first
        assert "event_number" in first
        assert "name" in first
        assert "client_name" in first
        assert "status" in first
    
    def test_create_event(self, client):
        """Test POST /events/ - Create new event"""
        new_event = {
            "event_number": "EVT-2025-002",
            "name": "Corporate Lunch",
            "client_name": "ABC Corporation",
            "client_email": "contact@abc.com",
            "client_phone": "+1234567890",
            "event_date": "2025-07-20",
            "event_time": "12:00",
            "guest_count": 50,
            "venue_name": "Office Building",
            "status": "prospect",
        }
        
        response = client.post("/api/v1/events/", json=new_event)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["event_number"] == "EVT-2025-002"
        assert data["name"] == "Corporate Lunch"
        assert data["guest_count"] == 50
        assert "id" in data
    
    def test_get_event_by_id(self, client, sample_events):
        """Test GET /events/{id} - Get event details"""
        event_id = sample_events[0].id
        
        response = client.get(f"/api/v1/events/{event_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == event_id
        assert data["event_number"] == "EVT-2025-001"
        assert "orders" in data
    
    def test_get_event_shows_calculated_totals(self, client, sample_events):
        """Test that event shows calculated costs and revenue"""
        event_id = sample_events[0].id
        
        response = client.get(f"/api/v1/events/{event_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "total_cost" in data
        assert "total_revenue" in data
        assert "margin" in data
        assert data["total_revenue"] > 0
    
    def test_update_event(self, client, sample_events):
        """Test PUT /events/{id} - Update event"""
        event_id = sample_events[0].id
        
        update_data = {
            "name": "Updated Wedding Reception",
            "guest_count": 120,
            "status": "in_progress",
        }
        
        response = client.put(f"/api/v1/events/{event_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated Wedding Reception"
        assert data["guest_count"] == 120
        assert data["status"] == "in_progress"
    
    def test_filter_events_by_status(self, client, sample_events):
        """Test filtering events by status"""
        response = client.get("/api/v1/events/?status=confirmed")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(event["status"] == "confirmed" for event in data)
    
    def test_get_nonexistent_event_returns_404(self, client):
        """Test that getting non-existent event returns 404"""
        response = client.get("/api/v1/events/9999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_event(self, client):
        """Test DELETE /events/{id} - Delete event"""
        # First create an event to delete
        new_event = {
            "event_number": "EVT-DELETE-001",
            "name": "Temporary Event",
            "client_name": "Test Client",
            "client_email": "test@test.com",
            "event_date": "2025-12-31",
            "guest_count": 10,
            "status": "prospect",
        }
        
        create_response = client.post("/api/v1/events/", json=new_event)
        event_id = create_response.json()["id"]
        
        # Delete it
        response = client.delete(f"/api/v1/events/{event_id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify it's deleted
        get_response = client.get(f"/api/v1/events/{event_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_nonexistent_event_returns_404(self, client):
        """Test that deleting non-existent event returns 404"""
        response = client.delete("/api/v1/events/9999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_add_event_order(self, client, sample_events, sample_recipes):
        """Test POST /events/{id}/items - Add order to event"""
        event_id = sample_events[0].id
        recipe_id = sample_recipes[0].id
        
        order_data = {
            "recipe_id": recipe_id,
            "quantity": 5,
            "unit_price": 25.00,
        }
        
        response = client.post(f"/api/v1/events/{event_id}/items", json=order_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "id" in data
        assert data["recipe_id"] == recipe_id
        assert data["quantity"] == 5


class TestEventCalculations:
    """Tests for event cost and margin calculations"""
    
    def test_event_total_cost_from_orders(self, client, sample_events):
        """Test that event total cost is calculated from orders"""
        event_id = sample_events[0].id
        
        response = client.get(f"/api/v1/events/{event_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Event has orders, so total_cost should be > 0
        assert data["total_cost"] > 0
        assert len(data["orders"]) > 0
    
    def test_event_margin_calculation(self, client, sample_events):
        """Test that event margin is calculated correctly"""
        event_id = sample_events[0].id
        
        response = client.get(f"/api/v1/events/{event_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Margin should be between 0 and 1
        assert 0 <= data["margin"] <= 1
        
        # Margin = (Revenue - Cost) / Revenue
        expected_margin = (data["total_revenue"] - data["total_cost"]) / data["total_revenue"]
        assert data["margin"] == pytest.approx(expected_margin, rel=0.01)
