"""
Events API endpoints (basic structure)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.event import Event

router = APIRouter()


@router.get("/")
def list_events(db: Session = Depends(get_db)):
    """List all events"""
    events = db.query(Event).all()
    return events


@router.get("/{event_id}")
def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get a specific event with financial calculations"""
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return {
        "id": event.id,
        "event_number": event.event_number,
        "name": event.name,
        "client_name": event.client_name,
        "event_date": event.event_date,
        "guest_count": event.guest_count,
        "status": event.status,
        "total_cost": event.total_cost,
        "total_revenue": event.total_revenue,
        "margin": event.margin,
        "orders": event.orders
    }
