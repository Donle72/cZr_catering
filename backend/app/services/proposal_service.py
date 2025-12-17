"""
Proposal Service
Handles business logic for creating and managing proposals
"""
from sqlalchemy.orm import Session, joinedload
from app.models.proposal import Proposal
from app.models.event import Event, EventStatus
from fastapi import HTTPException
from datetime import date, timedelta
from typing import Optional


class ProposalService:
    @staticmethod
    def create_from_event(
        db: Session,
        event_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        valid_days: int = 30,
        discount_amount: float = 0.0,
        notes: Optional[str] = None
    ) -> Proposal:
        """
        Create a proposal from an existing event
        Creates a snapshot of all event data at this moment
        """
        # 1. Fetch event with all related data
        event = db.query(Event).options(
            joinedload(Event.orders).joinedload('recipe')
        ).filter(Event.id == event_id).first()
        
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        if not event.orders or len(event.orders) == 0:
            raise HTTPException(
                status_code=400, 
                detail="Event must have at least one order/item to generate proposal"
            )
        
        # 2. Create comprehensive snapshots with all new fields
        client_snapshot = {
            "name": event.client_name,
            "email": event.client_email,
            "phone": event.client_phone,
            "company": event.client_company
        }
        
        # Contact info (puede ser diferente del cliente)
        contact_snapshot = {
            "name": event.contact_name or event.client_name,
            "email": event.contact_email or event.client_email,
            "phone": event.contact_phone or event.client_phone
        }
        
        event_snapshot = {
            "name": event.name,
            "date": event.event_date.isoformat() if event.event_date else None,
            "time": event.event_time,
            "end_time": event.event_end_time,
            "event_type": event.event_type,
            "service_type": event.service_type,
            "venue_name": event.venue_name,
            "venue_address": event.venue_address,
            "venue_city": event.venue_city,
            "venue_state": event.venue_state,
            "venue_zip": event.venue_zip,
            "guest_count": event.guest_count,
            "adult_count": event.adult_count,
            "minor_count": event.minor_count,
            "special_diets": event.special_diets,
            "contact": contact_snapshot
        }
        
        # 3. Create menu snapshot from orders
        menu_items = []
        subtotal = 0.0
        
        for order in event.orders:
            item_total = order.quantity * order.unit_price_frozen
            menu_items.append({
                "recipe_name": order.recipe.name if order.recipe else "Unknown",
                "quantity": order.quantity,
                "unit_price": order.unit_price_frozen,
                "total_price": item_total
            })
            subtotal += item_total
        
        menu_snapshot = {"items": menu_items}
        
        # 4. Calculate financials
        total_amount = subtotal - discount_amount
        
        # 5. Determine next version number for this event
        existing_proposals = db.query(Proposal).filter(
            Proposal.event_id == event_id
        ).all()
        next_version = len(existing_proposals) + 1
        
        # 6. Generate title if not provided
        if not title:
            title = f"Presupuesto - {event.name}"
        
        # 7. Calculate validity date
        valid_until = date.today() + timedelta(days=valid_days)
        
        # 8. Create proposal
        proposal = Proposal(
            event_id=event_id,
            version_number=next_version,
            client_snapshot=client_snapshot,
            event_snapshot=event_snapshot,
            menu_snapshot=menu_snapshot,
            title=title,
            description=description,
            subtotal=subtotal,
            discount_amount=discount_amount,
            total_amount=total_amount,
            valid_until=valid_until,
            notes=notes
        )
        
        db.add(proposal)
        
        # 9. Update event status to QUOTED if not already confirmed
        if event.status == EventStatus.PROSPECT:
            event.status = EventStatus.QUOTED
        
        db.commit()
        db.refresh(proposal)
        
        return proposal
    
    @staticmethod
    def get_proposal(db: Session, proposal_id: int) -> Optional[Proposal]:
        """Get a proposal by ID"""
        return db.query(Proposal).filter(Proposal.id == proposal_id).first()
    
    @staticmethod
    def list_proposals(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        event_id: Optional[int] = None
    ):
        """List proposals with pagination"""
        query = db.query(Proposal)
        
        if event_id:
            query = query.filter(Proposal.event_id == event_id)
        
        total = query.count()
        proposals = query.order_by(Proposal.generated_at.desc()).offset(skip).limit(limit).all()
        
        return {
            "items": proposals,
            "total": total,
            "page": (skip // limit) + 1,
            "size": limit
        }
    
    @staticmethod
    def delete_proposal(db: Session, proposal_id: int) -> bool:
        """Delete a proposal"""
        proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
        
        if not proposal:
            return False
        
        db.delete(proposal)
        db.commit()
        return True
