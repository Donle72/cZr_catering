"""
Pytest configuration and shared fixtures
"""
import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Set environment variables BEFORE importing app
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only-min-32-chars"
os.environ["REDIS_URL"] = "redis://localhost:6379/0"
os.environ["ENVIRONMENT"] = "testing"
os.environ["DEBUG"] = "true"
os.environ["CORS_ORIGINS"] = "http://localhost:3020,http://localhost:5173"

from app.main import app
from app.core.database import Base, get_db
from app.models.unit import Unit, UnitCategory


# Test database URL (SQLite in memory)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def db_session():
    """
    Create a fresh database session for each test
    Uses SQLite in-memory database for speed
    """
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    # Create basic units for testing
    kg_unit = Unit(id=1, name="Kilogram", symbol="kg", category=UnitCategory.WEIGHT)
    g_unit = Unit(id=2, name="Gram", symbol="g", category=UnitCategory.WEIGHT)
    l_unit = Unit(id=3, name="Liter", symbol="L", category=UnitCategory.VOLUME)
    un_unit = Unit(id=4, name="Unit", symbol="un", category=UnitCategory.COUNT)
    
    session.add_all([kg_unit, g_unit, l_unit, un_unit])
    session.commit()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Create a test client with database override
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_ingredient_data():
    """Sample ingredient data for testing"""
    return {
        "name": "Test Tomato",
        "sku": "TOM-001",
        "category": "Vegetables",
        "description": "Fresh red tomatoes",
        "current_cost": 100.0,
        "yield_factor": 0.95,
        "purchase_unit_id": 1,
        "usage_unit_id": 1,
        "conversion_ratio": 1.0,
        "tax_rate": 0.21
    }


@pytest.fixture
def sample_recipe_data():
    """Sample recipe data for testing"""
    return {
        "name": "Test Recipe",
        "description": "A test recipe",
        "recipe_type": "final_dish",
        "yield_quantity": 4.0,
        "yield_unit_id": 4,
        "target_margin": 0.35,
        "preparation_time": 30,
        "instructions": "Test instructions"
    }

