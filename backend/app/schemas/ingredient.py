"""
Pydantic schemas for Ingredients with enhanced validation
"""
from pydantic import BaseModel, Field, field_validator, computed_field
from typing import Optional
from datetime import datetime


class IngredientBase(BaseModel):
    """Base schema for Ingredient"""
    name: str = Field(..., min_length=3, max_length=200, description="Ingredient name (min 3 characters)")
    sku: Optional[str] = Field(None, max_length=50, description="Stock Keeping Unit code")
    description: Optional[str] = Field(None, max_length=500, description="Detailed description")
    category: Optional[str] = Field(None, max_length=100, description="Category (e.g., Vegetables, Meats)")
    purchase_unit_id: int = Field(..., gt=0, description="Unit used for purchasing")
    usage_unit_id: int = Field(..., gt=0, description="Unit used in recipes")
    conversion_ratio: float = Field(default=1.0, gt=0, description="Conversion ratio between purchase and usage units")
    current_cost: float = Field(default=0.0, ge=0, description="Current cost per purchase unit")
    yield_factor: float = Field(
        default=1.0, 
        gt=0, 
        le=1.0, 
        description="Yield factor (0-1, where 1=100% yield, 0.8=80% yield after waste)"
    )
    tax_rate: float = Field(default=0.0, ge=0, le=1.0, description="Tax rate (0-1, where 0.21=21%)")
    default_supplier_id: Optional[int] = Field(None, gt=0, description="Default supplier ID")
    stock_quantity: float = Field(default=0.0, description="Current stock quantity")
    min_stock_threshold: float = Field(default=0.0, description="Alert threshold for low stock")
    
    @field_validator('yield_factor')
    @classmethod
    def validate_yield_factor(cls, v: float) -> float:
        """Validate yield factor is between 0 and 1"""
        if v <= 0 or v > 1.0:
            raise ValueError('Yield factor must be between 0 and 1.0 (e.g., 0.85 for 85% yield)')
        if v < 0.1:
            raise ValueError('Yield factor seems too low. Did you mean a higher value?')
        return v
    
    @field_validator('conversion_ratio')
    @classmethod
    def validate_conversion_ratio(cls, v: float) -> float:
        """Validate conversion ratio is positive"""
        if v <= 0:
            raise ValueError('Conversion ratio must be positive')
        if v > 10000:
            raise ValueError('Conversion ratio seems too high. Please verify.')
        return v
    
    @field_validator('current_cost')
    @classmethod
    def validate_current_cost(cls, v: float) -> float:
        """Validate current cost is non-negative"""
        if v < 0:
            raise ValueError('Cost cannot be negative')
        if v > 1000000:
            raise ValueError('Cost seems unusually high. Please verify.')
        return v
    
    @field_validator('tax_rate')
    @classmethod
    def validate_tax_rate(cls, v: float) -> float:
        """Validate tax rate is between 0 and 1"""
        if v < 0 or v > 1.0:
            raise ValueError('Tax rate must be between 0 and 1.0 (e.g., 0.21 for 21%)')
        return v
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate and clean name"""
        v = v.strip()
        if len(v) < 3:
            raise ValueError('Name must be at least 3 characters long')
        return v


class IngredientCreate(IngredientBase):
    """Schema for creating an ingredient"""
    pass


class IngredientUpdate(BaseModel):
    """Schema for updating an ingredient"""
    name: Optional[str] = Field(None, min_length=3, max_length=200)
    sku: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=500)
    category: Optional[str] = Field(None, max_length=100)
    purchase_unit_id: Optional[int] = Field(None, gt=0)
    usage_unit_id: Optional[int] = Field(None, gt=0)
    conversion_ratio: Optional[float] = Field(None, gt=0)
    current_cost: Optional[float] = Field(None, ge=0)
    yield_factor: Optional[float] = Field(None, gt=0, le=1.0)
    tax_rate: Optional[float] = Field(None, ge=0, le=1.0)
    default_supplier_id: Optional[int] = Field(None, gt=0)
    
    @field_validator('yield_factor')
    @classmethod
    def validate_yield_factor(cls, v: Optional[float]) -> Optional[float]:
        """Validate yield factor if provided"""
        if v is not None and (v <= 0 or v > 1.0):
            raise ValueError('Yield factor must be between 0 and 1.0')
        return v
    
    @field_validator('conversion_ratio')
    @classmethod
    def validate_conversion_ratio(cls, v: Optional[float]) -> Optional[float]:
        """Validate conversion ratio if provided"""
        if v is not None and v <= 0:
            raise ValueError('Conversion ratio must be positive')
        return v


class IngredientResponse(IngredientBase):
    """Schema for ingredient response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        
    @computed_field
    @property
    def real_cost_per_usage_unit(self) -> float:
        """Calculate real cost considering yield factor"""
        if not hasattr(self, 'yield_factor') or self.yield_factor == 0:
            return 0.0
        # Determine conversion_ratio safe value
        c_ratio = self.conversion_ratio if self.conversion_ratio and self.conversion_ratio > 0 else 1.0
        
        cost_per_usage_unit = self.current_cost / c_ratio
        return cost_per_usage_unit / self.yield_factor


class IngredientList(BaseModel):
    """Schema for paginated ingredient list"""
    items: list[IngredientResponse]
    total: int
    page: int
    page_size: int
    pages: int


class IngredientBulkUpdate(BaseModel):
    """Schema for bulk price update"""
    percentage_increase: float = Field(..., description="Percentage to increase prices, e.g., 15 for 15%")
    category: Optional[str] = Field(None, description="Category filter for update")

    @field_validator('percentage_increase')
    @classmethod
    def validate_percentage(cls, v: float) -> float:
        """Validate percentage is within reasonable limits"""
        if v < -90:
            raise ValueError('Cannot decrease price by more than 90%')
        if v > 1000:
            raise ValueError('Cannot increase price by more than 1000% at once')
        return v
