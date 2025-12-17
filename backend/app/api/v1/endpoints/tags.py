"""
Tags API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagResponse

router = APIRouter()


@router.get("/", response_model=List[TagResponse])
def list_tags(
    category: str = None,
    db: Session = Depends(get_db)
):
    """List all tags, optionally filtered by category"""
    query = db.query(Tag)
    
    if category:
        query = query.filter(Tag.category == category)
    
    return query.order_by(Tag.name).all()


@router.post("/", response_model=TagResponse, status_code=201)
def create_tag(
    tag: TagCreate,
    db: Session = Depends(get_db)
):
    """Create a new tag"""
    # Check if tag already exists
    existing = db.query(Tag).filter(Tag.name == tag.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tag already exists")
    
    new_tag = Tag(**tag.dict())
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    
    return new_tag


@router.delete("/{tag_id}", status_code=204)
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db)
):
    """Delete a tag"""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    db.delete(tag)
    db.commit()
    
    return None
