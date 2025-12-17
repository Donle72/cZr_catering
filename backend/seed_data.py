"""
Seed data script - Creates initial tags using raw SQL
"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import SessionLocal


def create_tags(db: Session):
    """Create initial tags for categorization"""
    
    tags_data = [
        # Event Types
        ("COCKTAIL", "EVENT_TYPE", "Evento tipo cocktail con bocados"),
        ("COMPLETO_FORMAL", "EVENT_TYPE", "Evento formal completo"),
        ("INFORMAL", "EVENT_TYPE", "Evento informal"),
        ("WEDDING", "EVENT_TYPE", "Boda"),
        ("CORPORATE", "EVENT_TYPE", "Evento corporativo"),
        ("BIRTHDAY", "EVENT_TYPE", "Cumpleaños"),
        
        # Course Types
        ("ENTRANTE", "COURSE", "Entrada o aperitivo"),
        ("PRINCIPAL", "COURSE", "Plato principal"),
        ("POSTRE", "COURSE", "Postre"),
        ("BEBIDA", "COURSE", "Bebida"),
        
        # Dietary Restrictions
        ("APTO_CELIACO", "DIETARY", "Sin gluten"),
        ("VEGANO", "DIETARY", "Sin productos animales"),
        ("VEGETARIANO", "DIETARY", "Sin carne"),
        ("BAJO_SODIO", "DIETARY", "Reducido en sodio"),
        
        # Service Types
        ("BARRA", "SERVICE", "Servicio de barra"),
        ("CORTESIA", "SERVICE", "Cortesía"),
        ("FINGER_FOOD", "SERVICE", "Finger food / bocados"),
        
        # Additional
        ("ADULTOS", "AUDIENCE", "Para adultos"),
        ("MENORES", "AUDIENCE", "Para menores"),
    ]
    
    # Use raw SQL to avoid ORM relationship issues
    for name, category, description in tags_data:
        db.execute(
            text("INSERT INTO tags (name, category, description) VALUES (:name, :category, :description)"),
            {"name": name, "category": category, "description": description}
        )
    
    db.commit()
    print(f"✅ Created {len(tags_data)} tags")


def main():
    """Main seed function"""
    db = SessionLocal()
    
    try:
        print("🌱 Starting seed data creation...")
        
        # Create tags
        create_tags(db)
        
        print("✅ Seed data created successfully!")
        print("\n📝 Next steps:")
        print("   - Tag recipes via API: POST /api/v1/recipes/{id}/tags")
        print("   - Or use SQL: INSERT INTO recipe_tags (recipe_id, tag_id) VALUES (1, 1)")
        
    except Exception as e:
        print(f"❌ Error creating seed data: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
