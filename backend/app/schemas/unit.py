"""
Unit schemas for API responses
"""
from pydantic import BaseModel
from typing import Optional


class UnitBase(BaseModel):
    """Base schema for Unit"""
    name: str
    abbreviation: str
    symbol: Optional[str] = None
    display_name: Optional[str] = None
    category_id: int
    conversion_to_base: float = 1.0
    is_base_unit: bool = False


class UnitResponse(UnitBase):
    """Schema for unit response"""
    id: int
    
    class Config:
        from_attributes = True


class UnitCategoryResponse(BaseModel):
    """Schema for unit category response"""
    id: int
    name: str
    description: Optional[str] = None
    
    class Config:
        from_attributes = True
