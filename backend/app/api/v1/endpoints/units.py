"""
Units API endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.unit import Unit, UnitCategory

router = APIRouter()


@router.get("/")
def list_units(db: Session = Depends(get_db)):
    """List all units"""
    units = db.query(Unit).all()
    return units


@router.get("/categories")
def list_unit_categories(db: Session = Depends(get_db)):
    """List all unit categories"""
    categories = db.query(UnitCategory).all()
    return categories
