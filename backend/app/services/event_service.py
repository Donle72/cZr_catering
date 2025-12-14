from sqlalchemy.orm import Session, joinedload
from app.models.event import Event, EventOrder, EventStatus
from app.models.recipe import Recipe
from fastapi import HTTPException
from typing import List, Optional
from datetime import datetime

class EventService:
    @staticmethod
    def get_event(db: Session, event_id: int) -> Optional[Event]:
        return db.query(Event).filter(Event.id == event_id).first()

    @staticmethod
    def create_event(db: Session, event_data: dict) -> Event:
        event = Event(**event_data)
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def add_order_to_event(
        db: Session, 
        event_id: int, 
        recipe_id: int, 
        quantity: float, 
        unit_price_override: float = None
    ) -> EventOrder:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
            
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
            
        # Determine price and cost at this moment
        cost_at_sale = recipe.total_cost
        
        # Freezing logic: 
        # If manual override not provided, use recipe suggested price
        # IMPORTANT: This creates the "Snapshot"
        unit_price_frozen = unit_price_override if unit_price_override is not None else recipe.suggested_price
        
        order = EventOrder(
            event_id=event_id,
            recipe_id=recipe_id,
            quantity=quantity,
            unit_price_frozen=unit_price_frozen,
            cost_at_sale=cost_at_sale
        )
        
        db.add(order)
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def update_event_status(db: Session, event_id: int, new_status: EventStatus) -> Event:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
            
        # If moving to CONFIRMED or QUOTED, we might want to re-validate costs
        # But for Phase 1 (Data Integrity), we rely on the fact that 'cost_at_sale'
        # was frozen when the Order was created.
        
        # Enhancement: If we wanted to "Refresh" costs before confirming:
        # We would iterate over orders and update cost_at_sale to current recipe.total_cost
        # For now, we respect the original snapshot
        
        event.status = new_status
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def recalculate_event_financials(db: Session, event_id: int):
        """
        Manually trigger a refresh of costs (e.g., if client asks for updated quote)
        WARNING: This overrides historical data. Use with caution.
        """
        event = db.query(Event).options(joinedload(Event.orders).joinedload(EventOrder.recipe)).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
            
        for order in event.orders:
            # Re-fetch current recipe cost
            current_cost = order.recipe.total_cost
            order.cost_at_sale = current_cost
            # We do NOT change unit_price_frozen automatically, as that's the agreed price
            
        db.commit()
        db.refresh(event)
        return event
