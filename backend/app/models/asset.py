from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class AssetState(str, enum.Enum):
    AVAILABLE = "available"
    MAINTENANCE = "maintenance"
    BROKEN = "broken"
    LOST = "lost"

class Asset(Base):
    """
    Physical assets owned by the catering company (tables, chairs, ovens, decor).
    Not consumable like ingredients.
    """
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    category = Column(String(100), index=True) # e.g. "Furniture", "Tableware", "Kitchenware"
    description = Column(Text)
    
    total_quantity = Column(Integer, default=0, nullable=False)
    
    # Financials
    purchase_price = Column(Float, default=0.0)
    replacement_cost = Column(Float, default=0.0) # Cost to buy new if lost
    
    state = Column(String(50), default=AssetState.AVAILABLE)
    
    # Tracking
    location = Column(String(100)) # Warehouse A, Shelf 3
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
