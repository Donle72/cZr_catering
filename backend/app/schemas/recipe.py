from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime
from app.schemas.ingredient import IngredientResponse

class RecipeItemBase(BaseModel):
    quantity: float
    unit_id: int
    notes: Optional[str] = None
    is_scalable: bool = True

class RecipeItemCreate(RecipeItemBase):
    ingredient_id: Optional[int] = None
    child_recipe_id: Optional[int] = None

class RecipeItemResponse(RecipeItemBase):
    id: int
    ingredient: Optional[IngredientResponse] = None
    # child_recipe handled manually to avoid circular import loops in types
    child_recipe_id: Optional[int] = None
    child_recipe_name: Optional[str] = None
    item_cost: float

    class Config:
        from_attributes = True

class RecipeBase(BaseModel):
    name: str
    description: Optional[str] = None
    recipe_type: Literal["final_dish", "sub_recipe", "beverage", "dessert", "appetizer"] = "final_dish"
    yield_quantity: float = 1.0
    yield_unit_id: Optional[int] = None
    target_margin: float = 0.35
    preparation_time: int = 0
    instructions: Optional[str] = None
    shelf_life_hours: int = 24

class RecipeCreate(RecipeBase):
    items: Optional[List[RecipeItemCreate]] = None

class RecipeUpdate(RecipeBase):
    name: Optional[str] = None
    yield_quantity: Optional[float] = None

class RecipeResponse(RecipeBase):
    id: int
    total_cost: float
    cost_per_portion: float
    suggested_price: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[RecipeItemResponse] = []

    class Config:
        from_attributes = True
