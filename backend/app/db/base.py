"""
Database models - Base imports
Import all models here for Alembic to detect them
"""
from app.core.database import Base
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe, RecipeItem
from app.models.unit import Unit, UnitCategory
from app.models.supplier import Supplier, SupplierProduct
from app.models.event import Event, EventOrder
from app.models.proposal import Proposal
from app.models.user import User

__all__ = [
    "Base",
    "Ingredient",
    "Recipe",
    "RecipeItem",
    "Unit",
    "UnitCategory",
    "Supplier",
    "SupplierProduct",
    "Event",
    "EventOrder",
    "Proposal",
    "User"
]
