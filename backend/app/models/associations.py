"""
Association tables for many-to-many relationships
"""
from sqlalchemy import Column, Integer, ForeignKey, Table
from app.core.database import Base


# Recipe <-> Tag association
recipe_tags = Table(
    'recipe_tags',
    Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)
