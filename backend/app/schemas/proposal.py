"""
Proposal schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date, datetime


class ProposalItemSnapshot(BaseModel):
    """Single item in proposal menu"""
    recipe_name: str
    quantity: float
    unit_price: float
    total_price: float


class ProposalCreate(BaseModel):
    """Request to create a new proposal from an event"""
    event_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    valid_days: int = Field(default=30, ge=1, le=365)
    discount_amount: float = Field(default=0.0, ge=0.0)
    notes: Optional[str] = None


class ProposalResponse(BaseModel):
    """Proposal response with all data"""
    id: int
    event_id: int
    version_number: int
    
    # Snapshots
    client_snapshot: Optional[Dict[str, Any]]
    event_snapshot: Optional[Dict[str, Any]]
    menu_snapshot: Optional[Dict[str, Any]]
    
    # Details
    title: Optional[str]
    description: Optional[str]
    
    # Financials
    subtotal: float
    discount_amount: float
    total_amount: float
    
    # Validity
    valid_until: Optional[date]
    
    # Status
    is_accepted: bool
    accepted_at: Optional[datetime]
    
    # PDF
    pdf_url: Optional[str]
    
    # Notes
    notes: Optional[str]
    
    # Timestamps
    generated_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ProposalListItem(BaseModel):
    """Simplified proposal for list view"""
    id: int
    event_id: int
    version_number: int
    title: Optional[str]
    total_amount: float
    valid_until: Optional[date]
    is_accepted: bool
    generated_at: datetime
    
    # Extracted from snapshots for convenience
    client_name: Optional[str] = None
    event_name: Optional[str] = None
    event_date: Optional[date] = None
    
    class Config:
        from_attributes = True
