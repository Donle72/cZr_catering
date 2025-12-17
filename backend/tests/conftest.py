"""
Pytest configuration and shared fixtures for testing
"""
import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.models.unit import Unit
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe, RecipeItem, RecipeType
from app.models.event import Event, EventOrder, EventStatus
from app.models.supplier import Supplier


# Use in-memory SQLite for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Create a fresh database session for each test
    """
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Create a test client with overridden database dependency
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
def sample_units(db_session):
    """
    Create sample units for testing
    """
    from app.models.unit import UnitCategory
    
    # Create unit categories first
    weight_cat = UnitCategory(id=1, name="Weight", description="Weight measurements")
    volume_cat = UnitCategory(id=2, name="Volume", description="Volume measurements")
    count_cat = UnitCategory(id=3, name="Count", description="Counting units")
    
    db_session.add(weight_cat)
    db_session.add(volume_cat)
    db_session.add(count_cat)
    db_session.commit()
    
    # Create units
    units = [
        Unit(id=1, name="Kilogram", abbreviation="kg", category_id=1, is_base_unit=True, conversion_to_base=1.0),
        Unit(id=2, name="Gram", abbreviation="g", category_id=1, is_base_unit=False, conversion_to_base=0.001),
        Unit(id=3, name="Liter", abbreviation="L", category_id=2, is_base_unit=True, conversion_to_base=1.0),
        Unit(id=4, name="Milliliter", abbreviation="mL", category_id=2, is_base_unit=False, conversion_to_base=0.001),
        Unit(id=5, name="Unit", abbreviation="un", category_id=3, is_base_unit=True, conversion_to_base=1.0),
    ]
    
    for unit in units:
        db_session.add(unit)
    db_session.commit()
    
    return units



@pytest.fixture
def sample_ingredients(db_session, sample_units):
    """
    Create sample ingredients for testing
    """
    ingredients = [
        Ingredient(
            id=1,
            name="Tomato",
            sku="TOM-001",
            category="Vegetables",
            purchase_unit_id=1,  # kg
            usage_unit_id=2,  # g
            conversion_ratio=1000.0,  # 1 kg = 1000 g
            current_cost=150.0,  # $150 per kg
            yield_factor=0.85,  # 85% yield (15% waste)
            stock_quantity=50.0,
            min_stock_threshold=10.0,
        ),
        Ingredient(
            id=2,
            name="Onion",
            sku="ONI-001",
            category="Vegetables",
            purchase_unit_id=1,  # kg
            usage_unit_id=2,  # g
            conversion_ratio=1000.0,
            current_cost=80.0,  # $80 per kg
            yield_factor=0.90,  # 90% yield
            stock_quantity=30.0,
            min_stock_threshold=5.0,
        ),
        Ingredient(
            id=3,
            name="Olive Oil",
            sku="OIL-001",
            category="Oils",
            purchase_unit_id=3,  # L
            usage_unit_id=4,  # mL
            conversion_ratio=1000.0,
            current_cost=500.0,  # $500 per L
            yield_factor=1.0,  # 100% yield (no waste)
            stock_quantity=20.0,
            min_stock_threshold=5.0,
        ),
        Ingredient(
            id=4,
            name="Salt",
            sku="SAL-001",
            category="Seasonings",
            purchase_unit_id=1,  # kg
            usage_unit_id=2,  # g
            conversion_ratio=1000.0,
            current_cost=50.0,  # $50 per kg
            yield_factor=1.0,
            scaling_type='logarithmic',  # Non-linear scaling
            stock_quantity=100.0,
            min_stock_threshold=20.0,
        ),
    ]
    
    for ingredient in ingredients:
        db_session.add(ingredient)
    db_session.commit()
    
    # Refresh to get relationships
    for ingredient in ingredients:
        db_session.refresh(ingredient)
    
    return ingredients


@pytest.fixture
def sample_recipes(db_session, sample_units, sample_ingredients):
    """
    Create sample recipes for testing (including sub-recipes)
    """
    # Sub-recipe: Tomato Sauce
    tomato_sauce = Recipe(
        id=1,
        name="Tomato Sauce",
        description="Basic tomato sauce",
        recipe_type=RecipeType.SUB_RECIPE,
        yield_quantity=1.0,  # 1 liter
        yield_unit_id=3,  # L
        target_margin=0.30,
        preparation_time=30,
    )
    db_session.add(tomato_sauce)
    db_session.commit()
    db_session.refresh(tomato_sauce)
    
    # Add items to tomato sauce
    sauce_items = [
        RecipeItem(
            parent_recipe_id=1,
            ingredient_id=1,  # Tomato
            quantity=800.0,  # 800g
            unit_id=2,  # g
        ),
        RecipeItem(
            parent_recipe_id=1,
            ingredient_id=2,  # Onion
            quantity=100.0,  # 100g
            unit_id=2,  # g
        ),
        RecipeItem(
            parent_recipe_id=1,
            ingredient_id=3,  # Olive Oil
            quantity=50.0,  # 50mL
            unit_id=4,  # mL
        ),
        RecipeItem(
            parent_recipe_id=1,
            ingredient_id=4,  # Salt
            quantity=5.0,  # 5g
            unit_id=2,  # g
        ),
    ]
    
    for item in sauce_items:
        db_session.add(item)
    db_session.commit()
    
    # Final dish: Pasta with Tomato Sauce
    pasta_dish = Recipe(
        id=2,
        name="Pasta with Tomato Sauce",
        description="Classic pasta dish",
        recipe_type=RecipeType.FINAL_DISH,
        yield_quantity=4.0,  # 4 portions
        yield_unit_id=5,  # portions
        target_margin=0.35,
        preparation_time=45,
    )
    db_session.add(pasta_dish)
    db_session.commit()
    db_session.refresh(pasta_dish)
    
    # Add sub-recipe to pasta dish
    pasta_item = RecipeItem(
        parent_recipe_id=2,
        child_recipe_id=1,  # Tomato Sauce
        quantity=0.5,  # 0.5 liters
        unit_id=3,  # L
    )
    db_session.add(pasta_item)
    db_session.commit()
    
    # Refresh recipes to load relationships
    db_session.refresh(tomato_sauce)
    db_session.refresh(pasta_dish)
    
    return [tomato_sauce, pasta_dish]


@pytest.fixture
def sample_events(db_session, sample_recipes):
    """
    Create sample events for testing
    """
    event = Event(
        id=1,
        event_number="EVT-2025-001",
        name="Wedding Reception",
        description="Elegant wedding reception",
        client_name="John & Jane Doe",
        client_email="john.doe@example.com",
        client_phone="+1234567890",
        event_date=date(2025, 6, 15),  # Use date object instead of string
        event_time="19:00",
        guest_count=100,
        venue_name="Grand Hotel",
        venue_address="123 Main St, City",
        status=EventStatus.CONFIRMED,
        total_amount=15000.0,
        deposit_amount=5000.0,
        deposit_paid=1,
    )
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)
    
    # Add orders to event
    pasta_recipe = sample_recipes[1]  # Pasta dish
    
    order = EventOrder(
        event_id=1,
        recipe_id=pasta_recipe.id,
        quantity=100.0,  # 100 portions
        unit_price_frozen=150.0,  # $150 per portion
        cost_at_sale=pasta_recipe.cost_per_portion,
    )
    db_session.add(order)
    db_session.commit()
    
    db_session.refresh(event)
    return [event]


@pytest.fixture
def sample_supplier(db_session):
    """
    Create a sample supplier for testing
    """
    supplier = Supplier(
        id=1,
        name="Fresh Produce Co.",
        contact_name="Maria Garcia",
        email="maria@freshproduce.com",
        phone="+1234567890",
        address="456 Market St, City",
        currency="ARS",
        payment_terms="Net 30",
        is_active=True,
    )
    db_session.add(supplier)
    db_session.commit()
    db_session.refresh(supplier)
    
    return supplier
