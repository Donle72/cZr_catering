from enum import Enum
from pydantic import BaseModel

class Season(str, Enum):
    SUMMER = "summer"
    WINTER = "winter"
    SPRING = "spring"
    AUTUMN = "autumn"

class EventType(str, Enum):
    WEDDING = "wedding"
    CORPORATE = "corporate"
    BIRTHDAY = "birthday"

class EstimationRequest(BaseModel):
    guest_count: int
    duration_hours: int
    season: Season
    event_type: EventType

class EstimationResult(BaseModel):
    soft_drinks_liters: float
    wine_bottles: float
    champagne_bottles: float
    beer_liters: float
    beer_liters: float
    ice_kg: float
    finger_food_pieces: int

class EstimationService:
    @staticmethod
    def calculate_beverages(request: EstimationRequest) -> EstimationResult:
        """
        Calculates beverage requirements based on standard catering algorithms.
        
        Base Logic (per person per hour):
        - Soft Drinks: 0.5 Liters (Summer) / 0.3 Liters (Winter)
        - Ice: 0.7 kg (Summer) / 0.4 kg (Winter) per person (Total event)
        """
        
        # 1. Determine Season Factors
        if request.season == Season.SUMMER:
            soft_drink_factor = 0.6  # Liters per hour per person
            ice_factor_per_pax = 1.0 # Kg per person total
            beer_factor = 0.5        # Liters per hour
        elif request.season == Season.WINTER:
            soft_drink_factor = 0.3
            ice_factor_per_pax = 0.4
            beer_factor = 0.2
        else: # Spring/Autumn
            soft_drink_factor = 0.45
            ice_factor_per_pax = 0.7
            beer_factor = 0.35

        # 2. Adjust for Event Type (Alcohol consumption estimates)
        wine_factor = 0.0 # Bottles per person total
        champagne_factor = 0.0 # Bottles per person total
        
        if request.event_type == EventType.WEDDING:
            wine_factor = 0.4  # Approx 1 bottle per 2.5 people
            champagne_factor = 0.2 # Toast
            # Weddings usually imply heavier drinking
            beer_factor *= 1.2
            soft_drink_factor *= 0.8
            
        elif request.event_type == EventType.CORPORATE:
            wine_factor = 0.2
            champagne_factor = 0.05
            beer_factor *= 0.8
            
        elif request.event_type == EventType.BIRTHDAY:
            wine_factor = 0.25
            champagne_factor = 0.1
            
        # 3. Calculate Totals
        # Soft drinks & Beer depend on duration
        total_soft_drinks = request.guest_count * soft_drink_factor * request.duration_hours
        total_beer = request.guest_count * beer_factor * request.duration_hours
        
        # Wine & Champagne usually fixed per headcount (avg consumption) 
        # but could scale slightly with very long events. Keeping it simple for MVP.
        total_wine = request.guest_count * wine_factor
        total_champagne = request.guest_count * champagne_factor
        
        # Ice is total per person estimates
        total_ice = request.guest_count * ice_factor_per_pax
        
        # 4. Finger Food Estimation (Pieces per person)
        # Cocktail Heavy: 12-16 pieces (avg 14)
        # Cocktail Light: 4-6 pieces (avg 5)
        # We can infer type from duration? 
        # > 3 hours = Heavy, < 3 hours = Light
        pieces_per_person = 5 if request.duration_hours < 3 else 14
        
        # Adjust for event type
        if request.event_type == EventType.CORPORATE:
            pieces_per_person = max(3, pieces_per_person - 2) # Corporate eat less?
        
        total_pices = request.guest_count * pieces_per_person

        return EstimationResult(
            soft_drinks_liters=round(total_soft_drinks, 1),
            wine_bottles=round(total_wine, 1),
            champagne_bottles=round(total_champagne, 1),
            beer_liters=round(total_beer, 1),
            ice_kg=round(total_ice, 1),
            finger_food_pieces=int(total_pices)
        )
