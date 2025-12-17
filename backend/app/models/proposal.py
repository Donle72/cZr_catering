"""
Proposal model for versioned quotations with complete snapshot data
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Proposal(Base):
    """
    Versioned proposals/quotations sent to clients
    Stores complete snapshot of event data at time of generation
    """
    __tablename__ = "proposals"
    
    id = Column(Integer, primary_key=True, index=True)
    
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    
    # Version control
    version_number = Column(Integer, default=1, nullable=False)
    
    # Snapshot de datos del cliente (JSON)
    # {name, email, phone, company}
    client_snapshot = Column(JSON)
    
    # Snapshot de datos del evento (JSON)
    # {name, date, time, venue_name, venue_address, guest_count}
    event_snapshot = Column(JSON)
    
    # Snapshot del menú/items (JSON)
    # {items: [{recipe_name, quantity, unit_price, total_price}]}
    menu_snapshot = Column(JSON)
    
    # Proposal details
    title = Column(String(200))
    description = Column(Text)
    
    # Financial calculations
    subtotal = Column(Float, nullable=False, default=0.0)
    discount_amount = Column(Float, default=0.0)
    total_amount = Column(Float, nullable=False)
    
    # Validity
    valid_until = Column(Date)
    
    # Status
    is_accepted = Column(Integer, default=0)  # Boolean as Integer
    accepted_at = Column(DateTime(timezone=True))
    
    # PDF generation
    pdf_url = Column(String(500))  # Path to generated PDF
    
    # Additional notes
    notes = Column(Text)
    
    # Timestamps
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    event = relationship("Event", back_populates="proposals")
