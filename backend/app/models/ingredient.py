"""
Ingredient model with Yield Factor for cost calculation
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Ingredient(Base):
    """
    Master table for ingredients with yield management
    Implements the Yield Factor formula: Cost_uso = Price_compra / Yield_%
    """
    __tablename__ = "ingredients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    sku = Column(String(50), unique=True, index=True)
    description = Column(Text)
    
    # Category (e.g., "Vegetables", "Meats", "Dairy")
    category = Column(String(100), index=True)
    
    # Units
    purchase_unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)  # kg, L
    usage_unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)  # g, mL
    
    # Conversion ratio between purchase and usage units
    # e.g., 1 kg = 1000 g, so conversion_ratio = 1000
    conversion_ratio = Column(Float, default=1.0, nullable=False)
    
    # Current cost per purchase unit
    current_cost = Column(Float, default=0.0, nullable=False)
    
    # Yield Factor (0.0 to 1.0, where 1.0 = 100% yield, no waste)
    # e.g., 0.80 means 20% waste during processing
    yield_factor = Column(Float, default=1.0, nullable=False)
    
    # Tax rate (e.g., 0.21 for 21% IVA)
    tax_rate = Column(Float, default=0.21) # IVA default 21%
    
    # Inventory Management (MVP)
    stock_quantity = Column(Float, default=0.0)
    min_stock_threshold = Column(Float, default=0.0)
    
    # Default supplier
    default_supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    purchase_unit = relationship("Unit", foreign_keys=[purchase_unit_id])
    usage_unit = relationship("Unit", foreign_keys=[usage_unit_id])
    default_supplier = relationship("Supplier", foreign_keys=[default_supplier_id])
    supplier_products = relationship("SupplierProduct", back_populates="ingredient")
    
    @property
    def real_cost_per_usage_unit(self) -> float:
        """
        Calculate real cost per usage unit considering yield factor
        Formula: Real_Cost = (Current_Cost / Conversion_Ratio) / Yield_Factor
        """
        try:
            # Default values to avoid NoneType errors
            yield_factor = self.yield_factor if self.yield_factor is not None else 1.0
            conversion_ratio = self.conversion_ratio if self.conversion_ratio is not None else 1.0
            current_cost = self.current_cost if self.current_cost is not None else 0.0
            
            if yield_factor == 0 or conversion_ratio == 0:
                return 0.0
            
            cost_per_usage_unit = current_cost / conversion_ratio
            return cost_per_usage_unit / yield_factor
        except Exception:
            return 0.0


class IngredientPriceHistory(Base):
    """
    Log of price changes for ingredients to track inflation/variations
    """
    __tablename__ = "ingredient_price_history"
    
    id = Column(Integer, primary_key=True, index=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    
    old_cost = Column(Float, nullable=False)
    new_cost = Column(Float, nullable=False)
    
    # Optional: who made the change (if we had auth)
    changed_by = Column(String(100), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    ingredient = relationship("Ingredient")
