"""
Proposal model for versioned quotations
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Proposal(Base):
    """
    Versioned proposals/quotations sent to clients
    Allows tracking multiple versions and acceptance
    """
    __tablename__ = "proposals"
    
    id = Column(Integer, primary_key=True, index=True)
    
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    
    # Version control
    version_number = Column(Integer, default=1, nullable=False)
    
    # Proposal details
    title = Column(String(200))
    description = Column(Text)
    
    # Financial
    total_amount = Column(Float, nullable=False)
    
    # Validity
    valid_until = Column(Date)
    
    # Status
    is_accepted = Column(Integer, default=0)  # Boolean as Integer
    accepted_at = Column(DateTime(timezone=True))
    
    # PDF generation
    pdf_url = Column(String(500))  # Path to generated PDF
    
    # Additional data (flexible JSON field for custom data)
    proposal_metadata = Column(JSON)
    
    # Timestamps
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    event = relationship("Event", back_populates="proposals")
