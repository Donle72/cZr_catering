from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.core.database import get_db
from app.models.asset import Asset
from app.services.asset_service import AssetService

router = APIRouter()

class AssetCreate(BaseModel):
    name: str
    category: str
    total_quantity: int
    purchase_price: float = 0.0

class AssetAssign(BaseModel):
    event_id: int
    asset_id: int
    quantity: int

class AssetResponse(AssetCreate):
    id: int
    state: str
    
    class Config:
        from_attributes = True

@router.post("/", response_model=AssetResponse)
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    """Create a new physical asset"""
    return AssetService.create_asset(db, asset.model_dump())

@router.get("/", response_model=List[AssetResponse])
def list_assets(
    category: str = Query(None),
    db: Session = Depends(get_db)
):
    """List assets, optionally filtered by category"""
    query = db.query(Asset)
    if category:
        query = query.filter(Asset.category == category)
    return query.all()

@router.post("/{asset_id}/check-availability")
def check_availability(
    asset_id: int, 
    quantity: int = Query(..., gt=0), 
    db: Session = Depends(get_db)
):
    """Check if we have enough stock of an asset"""
    available = AssetService.check_availability(db, asset_id, quantity)
    return {"available": available}


@router.put("/{asset_id}", response_model=AssetResponse)
def update_asset(
    asset_id: int,
    asset_data: AssetCreate,
    db: Session = Depends(get_db)
):
    """Update an existing asset"""
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    # Update fields
    for key, value in asset_data.model_dump().items():
        setattr(asset, key, value)
    
    db.commit()
    db.refresh(asset)
    return asset


@router.delete("/{asset_id}", status_code=204)
def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db)
):
    """Delete an asset"""
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    db.delete(asset)
    db.commit()
    
    return None


@router.post("/assign")
def assign_asset_to_event(
    assignment: AssetAssign,
    db: Session = Depends(get_db)
):
    """Assign an asset to an event (deducting reliability from stock logic to be implemented)"""
    return AssetService.assign_to_event(db, assignment.event_id, assignment.asset_id, assignment.quantity)
