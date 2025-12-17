"""
Intelligent Suggestion Service
Filters recipes by tags based on event type and requirements
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.recipe import Recipe
from app.models.tag import Tag


class SuggestionService:
    @staticmethod
    def suggest_recipes_for_event(
        db: Session,
        event_type: str,
        course_type: Optional[str] = None,
        dietary_restrictions: Optional[List[str]] = None,
        limit: int = 20
    ) -> List[Recipe]:
        """
        Suggest recipes based on event type and requirements
        
        Args:
            event_type: COCKTAIL, COMPLETO_FORMAL, INFORMAL, etc.
            course_type: ENTRANTE, PRINCIPAL, POSTRE, etc.
            dietary_restrictions: List of dietary tags (APTO_CELIACO, VEGANO, etc.)
            limit: Maximum number of suggestions
        
        Returns:
            List of matching recipes
        """
        query = db.query(Recipe).join(Recipe.tags)
        
        # Filter by event type
        query = query.filter(Tag.name == event_type)
        
        # Filter by course type if specified
        if course_type:
            query = query.filter(Tag.name == course_type)
        
        # Filter by dietary restrictions if specified
        if dietary_restrictions:
            for restriction in dietary_restrictions:
                query = query.filter(Recipe.tags.any(Tag.name == restriction))
        
        # Get distinct recipes and limit
        recipes = query.distinct().limit(limit).all()
        
        return recipes
    
    @staticmethod
    def suggest_beverages_for_service(
        db: Session,
        service_type: str,
        limit: int = 10
    ) -> List[Recipe]:
        """
        Suggest beverages based on service type
        
        Args:
            service_type: BARRA, CORTESIA, etc.
            limit: Maximum number of suggestions
        
        Returns:
            List of matching beverage recipes
        """
        query = db.query(Recipe).join(Recipe.tags)
        
        # Filter by BEBIDA tag and service type
        query = query.filter(
            Tag.name.in_(['BEBIDA', service_type])
        )
        
        recipes = query.distinct().limit(limit).all()
        
        return recipes
