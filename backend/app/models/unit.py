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
    name = Column(String(100), nullable=False)  # e.g., "Kilogram", "Liter"
    abbreviation = Column(String(20), nullable=False, unique=True)  # e.g., "kg", "L"
    
    # Display fields for flexible representation
    symbol = Column(String(10))  # Short symbol: "g", "°C", "L"
    display_name = Column(String(100))  # Full name: "gramos", "Grados Centígrados", "litros"
    
    category_id = Column(Integer, ForeignKey("unit_categories.id"), nullable=False)
    
    # Conversion to base unit of category (e.g., 1 kg = 1000 g)
    conversion_to_base = Column(Float, default=1.0, nullable=False)
    is_base_unit = Column(Boolean, default=False)  # True for kg, L, etc.
    
    # Relationships
    category = relationship("UnitCategory", back_populates="units")
