"""
Database RESET script
WARNING: This will DROP ALL TABLES and recreate them.
"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import SessionLocal, engine
from app.db.base import Base
# Import all models to ensure they are registered
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe, RecipeItem
from app.models.unit import Unit, UnitCategory
from app.models.supplier import Supplier, SupplierProduct
from app.models.event import Event, EventOrder
from app.models.proposal import Proposal
from app.models.user import User
from init_db import init_db as populate_data

def reset_db():
    print("⚠️  DANGER: DELETING ALL DATA AND TABLES...")
    
    # Drop all tables correctly handling dependencies
    try:
        Base.metadata.drop_all(bind=engine)
        print("✅ Tables dropped successfully.")
    except Exception as e:
        print(f"❌ Error dropping tables: {e}")
        # Force drop if needed (PostgreSQL specific)
        with engine.connect() as connection:
            connection.execute(text("DROP SCHEMA public CASCADE; CREATE SCHEMA public;"))
            connection.commit()
        print("✅ Forced schema reset.")

    print("🔨 Recreating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables recreated.")

    print("🚀 Populating initial data...")
    populate_data()
    print("✅ System successfully reset!")

if __name__ == "__main__":
    reset_db()
