"""
Main API router - aggregates all endpoint routers
"""
from fastapi import APIRouter
from app.api.v1.endpoints import ingredients, recipes, events, suppliers, units

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    ingredients.router,
    prefix="/ingredients",
    tags=["Ingredients"]
)

api_router.include_router(
    recipes.router,
    prefix="/recipes",
    tags=["Recipes"]
)

api_router.include_router(
    events.router,
    prefix="/events",
    tags=["Events"]
)

api_router.include_router(
    suppliers.router,
    prefix="/suppliers",
    tags=["Suppliers"]
)

api_router.include_router(
    units.router,
    prefix="/units",
    tags=["Units"]
)
