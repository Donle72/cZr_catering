"""
Recipe Tag models for intelligent filtering and suggestions
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Tag(Base):
    """
    Tags for categorizing recipes
    Examples: FINGER_FOOD, COCKTAIL, ENTRANTE, PRINCIPAL, POSTRE, 
              APTO_CELIACO, VEGANO, BEBIDA, BARRA, CORTESIA, etc.
    """
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(50))  # EVENT_TYPE, COURSE, DIETARY, SERVICE, etc.
    description = Column(String(500))
    
    # Relationships - using string reference to avoid circular import
    recipes = relationship("Recipe", secondary="recipe_tags", back_populates="tags", lazy="dynamic")
