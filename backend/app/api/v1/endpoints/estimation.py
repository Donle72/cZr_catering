from fastapi import APIRouter, Depends, Query
from app.services.estimation_service import EstimationService, EstimationRequest, EstimationResult, Season, EventType

router = APIRouter()

@router.post("/calculate", response_model=EstimationResult)
def calculate_estimation(
    request: EstimationRequest
):
    """
    Predictive calculation for event beverages and ice.
    Based on guest count, duration, and season.
    """
    return EstimationService.calculate_beverages(request)
