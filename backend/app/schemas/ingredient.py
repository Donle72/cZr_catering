"""
Pydantic schemas for Ingredients
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class IngredientBase(BaseModel):
    """Base schema for Ingredient"""
    name: str = Field(..., min_length=1, max_length=200)
    sku: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    purchase_unit_id: int
    usage_unit_id: int
    conversion_ratio: float = Field(default=1.0, gt=0)
    current_cost: float = Field(default=0.0, ge=0)
    yield_factor: float = Field(default=1.0, gt=0, le=1.0, description="Yield factor (0-1, where 1=100% yield)")
    tax_rate: float = Field(default=0.0, ge=0)
    default_supplier_id: Optional[int] = None


class IngredientCreate(IngredientBase):
    """Schema for creating an ingredient"""
    pass


class IngredientUpdate(BaseModel):
    """Schema for updating an ingredient"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    sku: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    purchase_unit_id: Optional[int] = None
    usage_unit_id: Optional[int] = None
    conversion_ratio: Optional[float] = Field(None, gt=0)
    current_cost: Optional[float] = Field(None, ge=0)
    yield_factor: Optional[float] = Field(None, gt=0, le=1.0)
    tax_rate: Optional[float] = Field(None, ge=0)
    default_supplier_id: Optional[int] = None


class IngredientResponse(IngredientBase):
    """Schema for ingredient response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        
    @property
    def real_cost_per_usage_unit(self) -> float:
        """Calculate real cost considering yield factor"""
        if not hasattr(self, 'yield_factor') or self.yield_factor == 0:
            return 0.0
        cost_per_usage_unit = self.current_cost / self.conversion_ratio
        return cost_per_usage_unit / self.yield_factor


class IngredientList(BaseModel):
    """Schema for paginated ingredient list"""
    items: list[IngredientResponse]
    total: int
    page: int
    page_size: int
    pages: int
