"""
Supplier and Supplier Product models
Supports multi-currency and price comparison
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Supplier(Base):
    """
    Supplier information with multi-currency support
    """
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    
    # Contact information
    contact_name = Column(String(200))
    email = Column(String(200))
    phone = Column(String(50))
    address = Column(Text)
    
    # Tax information
    tax_id = Column(String(50))  # CUIT/RUC/etc
    
    # Currency (ARS, USD, EUR, etc.)
    currency_code = Column(String(3), default="ARS", nullable=False)
    
    # Payment terms (e.g., "30 days", "Cash on delivery")
    payment_terms = Column(String(200))
    
    # Delivery lead time in days
    lead_time_days = Column(Integer, default=1)
    
    # Minimum order amount
    minimum_order = Column(Float, default=0.0)
    
    # Active status
    is_active = Column(Integer, default=1)  # Using Integer for SQLite compatibility
    
    # Notes
    notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    products = relationship("SupplierProduct", back_populates="supplier")


class SupplierProduct(Base):
    """
    Price list by supplier
    Allows comparing the same ingredient across multiple suppliers
    """
    __tablename__ = "supplier_products"
    
    id = Column(Integer, primary_key=True, index=True)
    
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    
    # Supplier's SKU for this product
    supplier_sku = Column(String(100))
    
    # Price in supplier's currency
    price = Column(Float, nullable=False)
    
    # Package size (e.g., sold in boxes of 10 kg)
    package_size = Column(Float, default=1.0)
    package_unit_id = Column(Integer, ForeignKey("units.id"))
    
    # Last updated
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Availability
    is_available = Column(Integer, default=1)
    
    # Notes
    notes = Column(String(500))
    
    # Relationships
    supplier = relationship("Supplier", back_populates="products")
    ingredient = relationship("Ingredient", back_populates="supplier_products")
    package_unit = relationship("Unit")
