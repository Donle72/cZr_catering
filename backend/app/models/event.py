"""
Event and Event Order models
Core sales object for catering events
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date, Text, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class EventStatus(str, enum.Enum):
    """Event lifecycle status"""
    PROSPECT = "prospect"  # Initial contact
    QUOTED = "quoted"  # Proposal sent
    CONFIRMED = "confirmed"  # Contract signed
    IN_PROGRESS = "in_progress"  # Event is happening
    COMPLETED = "completed"  # Event finished
    CANCELLED = "cancelled"



class Event(Base):
    """
    Central sales object - represents a catering event
    """
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Event identification
    event_number = Column(String(50), unique=True, index=True)  # e.g., "EVT-2025-001"
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Client information (simplified for MVP, will be FK to Client table later)
    client_name = Column(String(200), nullable=False)
    client_email = Column(String(200))
    client_phone = Column(String(50))
    client_company = Column(String(200))  # Empresa del cliente
    
    # Contact information (puede ser diferente del cliente)
    contact_name = Column(String(200))
    contact_email = Column(String(200))
    contact_phone = Column(String(50))
    
    # Event details
    event_date = Column(Date, nullable=False, index=True)
    event_time = Column(String(20))  # e.g., "19:00"
    event_end_time = Column(String(20))  # Hora de fin
    
    # Event type (configurable, not hardcoded)
    event_type = Column(String(100))  # COCKTAIL, COMPLETO_FORMAL, INFORMAL, etc.
    service_type = Column(String(100))  # BARRA, CORTESIA, etc.
    
    # PAX breakdown
    guest_count = Column(Integer, nullable=False)  # Total
    adult_count = Column(Integer, default=0)
    minor_count = Column(Integer, default=0)
    
    # Special dietary requirements (JSON for flexibility)
    special_diets = Column(JSON)  # {"celiaco": 2, "vegano": 1, "bajo_sodio": 3}
    
    # Venue information (simplified for MVP)
    venue_name = Column(String(200))
    venue_address = Column(Text)
    venue_city = Column(String(100))
    venue_state = Column(String(100))
    venue_zip = Column(String(20))
    
    # Status
    status = Column(Enum(EventStatus), default=EventStatus.PROSPECT, nullable=False, index=True)
    
    # Pricing
    total_amount = Column(Float, default=0.0)
    deposit_amount = Column(Float, default=0.0)
    deposit_paid = Column(Integer, default=0)  # Boolean as Integer
    
    # Special requirements
    special_requirements = Column(Text)
    dietary_restrictions = Column(Text)
    
    # Staff assignment (simplified for MVP)
    assigned_chef = Column(String(200))
    assigned_coordinator = Column(String(200))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    orders = relationship("EventOrder", back_populates="event", cascade="all, delete-orphan")
    proposals = relationship("Proposal", back_populates="event", cascade="all, delete-orphan")
    
    @property
    def total_cost(self) -> float:
        """Calculate total cost from all orders"""
        return sum(order.total_cost for order in self.orders)
    
    @property
    def total_revenue(self) -> float:
        """Calculate total revenue from all orders"""
        return sum(order.total_price for order in self.orders)
    
    @property
    def margin(self) -> float:
        """Calculate profit margin"""
        if self.total_revenue == 0:
            return 0.0
        return (self.total_revenue - self.total_cost) / self.total_revenue


class EventOrder(Base):
    """
    Line items for an event - recipes/services sold
    """
    __tablename__ = "event_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    
    # Quantity ordered
    quantity = Column(Float, nullable=False)
    
    # Frozen prices at time of sale (for historical analysis)
    unit_price_frozen = Column(Float, nullable=False)  # Price charged to client
    cost_at_sale = Column(Float, nullable=False)  # Cost at time of sale
    
    # Notes
    notes = Column(String(500))
    
    # Relationships
    event = relationship("Event", back_populates="orders")
    recipe = relationship("Recipe")
    
    @property
    def total_price(self) -> float:
        """Total price for this line item"""
        return self.quantity * self.unit_price_frozen
    
    @property
    def total_cost(self) -> float:
        """Total cost for this line item"""
        return self.quantity * self.cost_at_sale
    
    @property
    def margin(self) -> float:
        """Margin for this line item"""
        if self.total_price == 0:
            return 0.0
        return (self.total_price - self.total_cost) / self.total_price
