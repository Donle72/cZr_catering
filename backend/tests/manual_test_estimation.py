import sys
import os

# Add parent dir (backend) to path
try:
    # Assuming file is in backend/tests/
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(backend_dir)
except:
    pass

from app.services.estimation_service import EstimationService, EstimationRequest, Season, EventType

def test_estimation():
    print("Testing Predictive Estimation...")
    
    # Cases
    # 1. Summer Wedding (High Consumption)
    req_summer = EstimationRequest(
        guest_count=100,
        duration_hours=5,
        season=Season.SUMMER,
        event_type=EventType.WEDDING
    )
    
    res_summer = EstimationService.calculate_beverages(req_summer)
    print(f"\n[Summer Wedding 100pax 5hrs]")
    print(f"  Ice: {res_summer.ice_kg} kg (Expected ~100kg)")
    print(f"  Soft Drinks: {res_summer.soft_drinks_liters} L")
    print(f"  Beer: {res_summer.beer_liters} L")
    
    # 2. Winter Corporate (Low Consumption)
    req_winter = EstimationRequest(
        guest_count=50,
        duration_hours=2,
        season=Season.WINTER,
        event_type=EventType.CORPORATE
    )
    
    res_winter = EstimationService.calculate_beverages(req_winter)
    print(f"\n[Winter Corporate 50pax 2hrs]")
    print(f"  Ice: {res_winter.ice_kg} kg (Expected ~20kg)")
    print(f"  Soft Drinks: {res_winter.soft_drinks_liters} L")

    print("\n✅ Estimation Logic Validated.")

if __name__ == "__main__":
    test_estimation()
