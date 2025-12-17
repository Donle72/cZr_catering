"""
Database models - Base imports
Import all models here for Alembic to detect them
"""
from app.core.database import Base
from app.models.associations import recipe_tags  # Import association tables first
from app.models.ingredient import Ingredient, IngredientPriceHistory
from app.models.recipe import Recipe, RecipeItem
from app.models.unit import Unit, UnitCategory
from app.models.supplier import Supplier, SupplierProduct
from app.models.event import Event, EventOrder
from app.models.proposal import Proposal
from app.models.asset import Asset
from app.models.event_asset import EventAsset
from app.models.user import User
from app.models.i18n import Translation
from app.models.tag import Tag

__all__ = [
    "Base",
    "Ingredient",
    "IngredientPriceHistory",
    "Recipe",
    "RecipeItem",
    "Unit",
    "UnitCategory",
    "Supplier",
    "SupplierProduct",
    "Event",
    "EventOrder",
    "Proposal",
    "Asset",
    "EventAsset",
    "User",
    "Translation",
    "Tag"
]
