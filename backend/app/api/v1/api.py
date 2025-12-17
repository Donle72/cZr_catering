"""
Main API router - aggregates all endpoint routers
"""
from fastapi import APIRouter
from app.api.v1.endpoints import ingredients, recipes, units, suppliers, events, production, i18n, search, estimation, simulation, assets, stats, proposals, tags, suggestions

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(ingredients.router, prefix="/ingredients", tags=["ingredients"])

api_router.include_router(recipes.router, prefix="/recipes", tags=["recipes"])

api_router.include_router(events.router, prefix="/events", tags=["events"])

api_router.include_router(production.router, prefix="/production", tags=["production"])

api_router.include_router(suppliers.router, prefix="/suppliers", tags=["suppliers"])

api_router.include_router(units.router, prefix="/units", tags=["Units"])

api_router.include_router(i18n.router, prefix="/i18n", tags=["i18n"])

api_router.include_router(search.router, prefix="/search", tags=["search"])

api_router.include_router(estimation.router, prefix="/estimation", tags=["estimation"])

api_router.include_router(simulation.router, prefix="/simulation", tags=["simulation"])

api_router.include_router(assets.router, prefix="/assets", tags=["assets"])

api_router.include_router(stats.router, prefix="/stats", tags=["stats"])

api_router.include_router(proposals.router, prefix="/proposals", tags=["proposals"])

api_router.include_router(tags.router, prefix="/tags", tags=["tags"])

api_router.include_router(suggestions.router, prefix="/suggestions", tags=["suggestions"])
