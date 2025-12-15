from sqlalchemy.orm import Session
from app.models.asset import Asset, AssetState
from app.models.event_asset import EventAsset
from fastapi import HTTPException

class AssetService:
    @staticmethod
    def create_asset(db: Session, data: dict):
        asset = Asset(**data)
        db.add(asset)
        db.commit()
        db.refresh(asset)
        return asset

    @staticmethod
    def check_availability(db: Session, asset_id: int, quantity_needed: int):
        asset = db.query(Asset).filter(Asset.id == asset_id).first()
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        # Simple logic: Is total quantity enough? (In real world, we check overlaps with other events)
        # For MVP, we just check if we own enough.
        if asset.total_quantity < quantity_needed:
             raise HTTPException(status_code=400, detail=f"Not enough assets. Have {asset.total_quantity}, need {quantity_needed}")
        
        return True

    @staticmethod
    def update_state(db: Session, asset_id: int, new_state: AssetState):
        asset = db.query(Asset).filter(Asset.id == asset_id).first()
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
            
        asset.state = new_state
        db.commit()
        db.refresh(asset)
        return asset

    @staticmethod
    def assign_to_event(db: Session, event_id: int, asset_id: int, quantity: int):
        # 1. Check availability
        AssetService.check_availability(db, asset_id, quantity)
        
        # 2. Check if already assigned
        existing = db.query(EventAsset).filter(
            EventAsset.event_id == event_id,
            EventAsset.asset_id == asset_id
        ).first()
        
        if existing:
            existing.quantity += quantity # Add to existing assignment
        else:
            new_assignment = EventAsset(
                event_id=event_id,
                asset_id=asset_id,
                quantity=quantity
            )
            db.add(new_assignment)
            
        db.commit()
        return {"status": "assigned", "asset_id": asset_id, "event_id": event_id, "quantity": quantity}

