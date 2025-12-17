"""
Events API endpoints (basic structure)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.event import Event

router = APIRouter()


@router.get("/")
def list_events(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """List all events with pagination"""
    total = db.query(Event).count()
    events = db.query(Event).order_by(Event.event_date.desc()).offset(skip).limit(limit).all()
    
    return {
        "items": events,
        "total": total,
        "page": (skip // limit) + 1,
        "size": limit
    }


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


@router.post("/", response_model=dict)
def create_event(
    event: dict,
    db: Session = Depends(get_db)
):
    """Create a new event"""
    from app.services.event_service import EventService
    return EventService.create_event(db, event)


@router.put("/{event_id}", response_model=dict)
def update_event(
    event_id: int,
    event_data: dict,
    db: Session = Depends(get_db)
):
    """Update an existing event"""
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Update fields
    for key, value in event_data.items():
        if hasattr(event, key):
            setattr(event, key, value)
    
    db.commit()
    db.refresh(event)
    
    # Return serializable dict
    return {
        "id": event.id,
        "event_number": event.event_number,
        "name": event.name,
        "description": event.description,
        "client_name": event.client_name,
        "client_email": event.client_email,
        "client_phone": event.client_phone,
        "event_date": event.event_date.isoformat() if event.event_date else None,
        "event_time": event.event_time,
        "guest_count": event.guest_count,
        "venue_name": event.venue_name,
        "venue_address": event.venue_address,
        "status": event.status.value if event.status else None,
        "total_amount": event.total_amount,
        "deposit_amount": event.deposit_amount,
        "deposit_paid": event.deposit_paid,
        "total_cost": event.total_cost,
        "total_revenue": event.total_revenue,
        "margin": event.margin
    }


@router.delete("/{event_id}", status_code=204)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    """Delete an event"""
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db.delete(event)
    db.commit()
    
    return None


@router.post("/{event_id}/items", response_model=dict)
def add_event_item(
    event_id: int,
    item: dict,
    db: Session = Depends(get_db)
):
    """Add a recipe/item to an event (Using Service for Snapshots)"""
    from app.services.event_service import EventService
    
    try:
        # Manually parsing item dict for now, DTO would be better
        return EventService.add_order_to_event(
            db=db,
            event_id=event_id,
            recipe_id=item.get("recipe_id"),
            quantity=item.get("quantity"),
            unit_price_override=item.get("unit_price")
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

