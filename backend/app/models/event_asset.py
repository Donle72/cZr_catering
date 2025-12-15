from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class EventAsset(Base):
    """
    Link table for assigning assets to events (e.g., 50 Chairs for Wedding X)
    """
    __tablename__ = "event_assets"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    
    quantity = Column(Integer, default=1, nullable=False)
    
    # Relationships
    event = relationship("Event", backref="assigned_assets")
    asset = relationship("Asset")
