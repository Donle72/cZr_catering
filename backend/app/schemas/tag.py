"""
Tag schemas for validation
"""
from pydantic import BaseModel
from typing import Optional


class TagCreate(BaseModel):
    """Create a new tag"""
    name: str
    category: Optional[str] = None  # EVENT_TYPE, COURSE, DIETARY, SERVICE
    description: Optional[str] = None


class TagResponse(BaseModel):
    """Tag response"""
    id: int
    name: str
    category: Optional[str]
    description: Optional[str]
    
    class Config:
        from_attributes = True
