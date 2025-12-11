"""
Unit and Unit Category models
Handles measurement units (kg, liters, grams, etc.)
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class UnitCategory(Base):
    """
    Categories of units (Weight, Volume, Count, etc.)
    """
    __tablename__ = "unit_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)  # "Weight", "Volume", "Count"
    description = Column(String(200))
    
    # Relationships
    units = relationship("Unit", back_populates="category")


class Unit(Base):
    """
    Measurement units with conversion ratios
    """
    __tablename__ = "units"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)  # "Kilogram", "Liter"
    abbreviation = Column(String(10), unique=True, nullable=False)  # "kg", "L"
    category_id = Column(Integer, ForeignKey("unit_categories.id"), nullable=False)
    
    # Conversion to base unit of category (e.g., 1 kg = 1000 g)
    conversion_to_base = Column(Float, default=1.0, nullable=False)
    is_base_unit = Column(Boolean, default=False)  # True for kg, L, etc.
    
    # Relationships
    category = relationship("UnitCategory", back_populates="units")
