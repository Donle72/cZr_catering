from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import Optional

from app.core.database import get_db
from app.services.production_service import ProductionService

router = APIRouter()

@router.get("/plan")
def get_production_plan(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Get consolidated production plan for a date range.
    Defaults to next 7 days if not specified.
    """
    if not start_date:
        start_date = date.today()
    if not end_date:
        end_date = start_date + timedelta(days=7)
        
    return ProductionService.get_production_plan(db, start_date, end_date)

@router.get("/shopping-list")
def get_shopping_list(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Get shopping list based on production plan minus current stock.
    """
    if not start_date:
        start_date = date.today()
    if not end_date:
        end_date = start_date + timedelta(days=7)
        
    plan = ProductionService.get_production_plan(db, start_date, end_date)
    
    # Filter only ingredients that need purchasing
    shopping_items = [
        item for item in plan["ingredients"] 
        if item["to_buy"] > 0
    ]
    
    return {
        "period": {
            "start": start_date,
            "end": end_date
        },
        "total_items": len(shopping_items),
        "items": shopping_items
    }
