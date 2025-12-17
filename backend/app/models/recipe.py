"""
Recipe models with recursive composition support
Supports both final dishes and sub-recipes (mise en place)
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class RecipeType(str, enum.Enum):
    """Recipe types"""
    FINAL_DISH = "final_dish"  # Plato final para servir
    SUB_RECIPE = "sub_recipe"  # Pre-producción / Mise en place
    BEVERAGE = "beverage"
    DESSERT = "dessert"
    APPETIZER = "appetizer"


class Recipe(Base):
    """
    Recipe header - can be a final dish or a sub-recipe
    """
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    
    # Recipe type
    recipe_type = Column(Enum(RecipeType), default=RecipeType.FINAL_DISH, nullable=False)
    
    # Yield quantity (number of portions this recipe produces)
    yield_quantity = Column(Float, default=1.0, nullable=False)
    yield_unit_id = Column(Integer, ForeignKey("units.id"))
    
    # Target margin for pricing (0.0 to 1.0, e.g., 0.35 = 35%)
    target_margin = Column(Float, default=0.35)
    
    # Preparation time in minutes
    preparation_time = Column(Integer, default=0)
    
    # Cooking instructions
    instructions = Column(Text)
    
    # Scaling behavior
    is_linear_scaling = Column(Boolean, default=True)  # False for recipes with non-linear ingredients
    
    # Shelf life in hours (for production planning)
    shelf_life_hours = Column(Integer, default=24)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    yield_unit = relationship("Unit")
    items = relationship(
        "RecipeItem", 
        back_populates="parent_recipe", 
        cascade="all, delete-orphan",
        foreign_keys="[RecipeItem.parent_recipe_id]"
    )
    tags = relationship("Tag", secondary="recipe_tags", back_populates="recipes", lazy="select")

    
    @property
    def total_cost(self) -> float:
        """
        Calculate total cost recursively
        Sums costs of all ingredients and sub-recipes
        """
        total = 0.0
        for item in self.items:
            total += item.item_cost
        return total
    
    @property
    def cost_per_portion(self) -> float:
        """
        Cost per portion
        """
        if self.yield_quantity == 0:
            return 0.0
        return self.total_cost / self.yield_quantity
    
    @property
    def suggested_price(self) -> float:
        """
        Suggested selling price based on target margin
        Formula: Price = Cost / (1 - Margin)
        """
        if self.target_margin >= 1.0:
            return 0.0
        return self.cost_per_portion / (1 - self.target_margin)


class RecipeItem(Base):
    """
    Recursive table for recipe composition
    Can contain either an ingredient OR another recipe (sub-recipe)
    """
    __tablename__ = "recipe_items"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Parent recipe
    parent_recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    
    # Either ingredient OR child recipe (one must be null)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=True)
    child_recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=True)
    
    # Quantity needed
    quantity = Column(Float, nullable=False)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    
    # Optional notes
    notes = Column(String(500))
    
    # Scaling behavior for this specific item
    is_scalable = Column(Boolean, default=True)
    scaling_factor = Column(Float, default=1.0)  # For non-linear scaling adjustments
    
    # Relationships - Using primaryjoin to resolve ambiguity explicitly
    parent_recipe = relationship(
        "Recipe", 
        foreign_keys=[parent_recipe_id], 
        back_populates="items"
    )
    
    ingredient = relationship("Ingredient", foreign_keys=[ingredient_id])
    
    child_recipe = relationship(
        "Recipe", 
        foreign_keys=[child_recipe_id]
    )
    
    unit = relationship("Unit")
    
    @property
    def item_cost(self) -> float:
        """
        Calculate cost of this item
        Either from ingredient or from child recipe
        """
        if self.ingredient:
            # Cost from ingredient
            return self.ingredient.real_cost_per_usage_unit * self.quantity
        elif self.child_recipe:
            # Cost from sub-recipe
            return self.child_recipe.cost_per_portion * self.quantity
        return 0.0
