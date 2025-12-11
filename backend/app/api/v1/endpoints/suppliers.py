"""
Suppliers API endpoints (basic structure)
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.supplier import Supplier

router = APIRouter()


@router.get("/")
def list_suppliers(db: Session = Depends(get_db)):
    """List all suppliers"""
    suppliers = db.query(Supplier).all()
    return suppliers
