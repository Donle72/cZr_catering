from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.simulation_service import SimulationService

router = APIRouter()

@router.get("/inflation")
def simulate_inflation(
    category: str = Query(..., description="Category to simulate (e.g. 'Meats')"),
    percentage: float = Query(..., description="Percentage increase (e.g. 15.0)"),
    db: Session = Depends(get_db)
):
    """
    Simulate what happens to Recipe costs if a specific Ingredient Category increases in price.
    Does NOT modify database.
    """
    return SimulationService.simulate_inflation(db, category, percentage)
