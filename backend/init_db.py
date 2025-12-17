"""
Database initialization script with sample data
Run this to populate the database with example data
"""
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.db.base import Base
from app.models.unit import Unit, UnitCategory
from app.models.ingredient import Ingredient
from app.models.supplier import Supplier


def init_db():
    """Initialize database with sample data"""
    
    # Create all tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(UnitCategory).first():
            print("Database already initialized!")
            return
        
        print("Initializing database with sample data...")
        
        # 1. Create Unit Categories
        print("Creating unit categories...")
        weight_cat = UnitCategory(name="Weight", description="Weight measurements")
        volume_cat = UnitCategory(name="Volume", description="Volume measurements")
        count_cat = UnitCategory(name="Count", description="Countable items")
        
        db.add_all([weight_cat, volume_cat, count_cat])
        db.commit()
        
        # 2. Create Units
        print("Creating units...")
        units = [
            # Weight
            Unit(name="Kilogram", abbreviation="kg", symbol="kg", display_name="kilogramos", category_id=weight_cat.id, conversion_to_base=1.0, is_base_unit=True),
            Unit(name="Gram", abbreviation="g", symbol="g", display_name="gramos", category_id=weight_cat.id, conversion_to_base=0.001, is_base_unit=False),
            Unit(name="Pound", abbreviation="lb", symbol="lb", display_name="libras", category_id=weight_cat.id, conversion_to_base=0.453592, is_base_unit=False),
            
            # Volume
            Unit(name="Liter", abbreviation="L", symbol="L", display_name="litros", category_id=volume_cat.id, conversion_to_base=1.0, is_base_unit=True),
            Unit(name="Milliliter", abbreviation="mL", symbol="mL", display_name="mililitros", category_id=volume_cat.id, conversion_to_base=0.001, is_base_unit=False),
            Unit(name="Cup", abbreviation="cup", symbol="cup", display_name="tazas", category_id=volume_cat.id, conversion_to_base=0.236588, is_base_unit=False),
            
            # Count
            Unit(name="Unit", abbreviation="un", symbol="un", display_name="unidades", category_id=count_cat.id, conversion_to_base=1.0, is_base_unit=True),
            Unit(name="Dozen", abbreviation="dz", symbol="dz", display_name="docenas", category_id=count_cat.id, conversion_to_base=12.0, is_base_unit=False),
        ]
        
        db.add_all(units)
        db.commit()
        
        # Get unit IDs for reference
        kg_unit = db.query(Unit).filter(Unit.abbreviation == "kg").first()
        g_unit = db.query(Unit).filter(Unit.abbreviation == "g").first()
        l_unit = db.query(Unit).filter(Unit.abbreviation == "L").first()
        ml_unit = db.query(Unit).filter(Unit.abbreviation == "mL").first()
        un_unit = db.query(Unit).filter(Unit.abbreviation == "un").first()
        
        # 3. Create Suppliers
        print("Creating suppliers...")
        suppliers = [
            Supplier(
                name="Distribuidora Central",
                contact_name="Juan Pérez",
                email="ventas@distribuidoracentral.com",
                phone="+54 11 4567-8900",
                currency_code="ARS",
                payment_terms="30 días",
                lead_time_days=2,
                is_active=1
            ),
            Supplier(
                name="Carnes Premium SA",
                contact_name="María González",
                email="info@carnespremium.com",
                phone="+54 11 4567-8901",
                currency_code="ARS",
                payment_terms="Contado",
                lead_time_days=1,
                is_active=1
            ),
            Supplier(
                name="Verduras Frescas",
                contact_name="Carlos Rodríguez",
                email="pedidos@verdurasfrescas.com",
                phone="+54 11 4567-8902",
                currency_code="ARS",
                payment_terms="15 días",
                lead_time_days=1,
                is_active=1
            ),
        ]
        
        db.add_all(suppliers)
        db.commit()
        
        # 4. Create Sample Ingredients with STOCK
        print("Creating sample ingredients...")
        ingredients = [
            # Carnes
            Ingredient(
                name="Lomo de Res",
                sku="CARNE-001",
                description="Lomo de res premium para eventos",
                category="Carnes",
                purchase_unit_id=kg_unit.id,
                usage_unit_id=g_unit.id,
                conversion_ratio=1000,
                conversion_unit="g",
                current_cost=8500.00,
                yield_factor=0.85,  # 15% waste (trimming)
                tax_rate=0.21,
                default_supplier_id=suppliers[1].id,
                stock_quantity=25.0,  # 25 kg en stock
                min_stock_threshold=5.0
            ),
            Ingredient(
                name="Pollo Entero",
                sku="CARNE-002",
                description="Pollo entero fresco",
                category="Carnes",
                purchase_unit_id=kg_unit.id,
                usage_unit_id=g_unit.id,
                conversion_ratio=1000,
                conversion_unit="g",
                current_cost=1200.00,
                yield_factor=0.70,  # 30% waste (bones, skin)
                tax_rate=0.21,
                default_supplier_id=suppliers[1].id,
                stock_quantity=40.0,  # 40 kg en stock
                min_stock_threshold=10.0
            ),
            
            # Vegetales
            Ingredient(
                name="Papa",
                sku="VEG-001",
                description="Papa blanca para guarniciones",
                category="Vegetales",
                purchase_unit_id=kg_unit.id,
                usage_unit_id=g_unit.id,
                conversion_ratio=1000,
                conversion_unit="g",
                current_cost=450.00,
                yield_factor=0.80,  # 20% waste (peeling)
                tax_rate=0.21,
                default_supplier_id=suppliers[2].id,
                stock_quantity=100.0,  # 100 kg en stock
                min_stock_threshold=20.0
            ),
            Ingredient(
                name="Cebolla",
                sku="VEG-002",
                description="Cebolla blanca",
                category="Vegetales",
                purchase_unit_id=kg_unit.id,
                usage_unit_id=g_unit.id,
                conversion_ratio=1000,
                conversion_unit="g",
                current_cost=380.00,
                yield_factor=0.90,  # 10% waste
                tax_rate=0.21,
                default_supplier_id=suppliers[2].id,
                stock_quantity=50.0,  # 50 kg en stock
                min_stock_threshold=10.0
            ),
            Ingredient(
                name="Tomate",
                sku="VEG-003",
                description="Tomate perita",
                category="Vegetales",
                purchase_unit_id=kg_unit.id,
                usage_unit_id=g_unit.id,
                conversion_ratio=1000,
                conversion_unit="g",
                current_cost=520.00,
                yield_factor=0.95,  # 5% waste
                tax_rate=0.21,
                default_supplier_id=suppliers[2].id,
                stock_quantity=60.0,  # 60 kg en stock
                min_stock_threshold=15.0
            ),
            
            # Lácteos
            Ingredient(
                name="Leche Entera",
                sku="LACT-001",
                description="Leche entera pasteurizada",
                category="Lácteos",
                purchase_unit_id=l_unit.id,
                usage_unit_id=ml_unit.id,
                conversion_ratio=1000,
                conversion_unit="mL",
                current_cost=850.00,
                yield_factor=1.0,  # No waste
                tax_rate=0.21,
                default_supplier_id=suppliers[0].id,
                stock_quantity=80.0,  # 80 L en stock
                min_stock_threshold=20.0
            ),
            Ingredient(
                name="Queso Parmesano",
                sku="LACT-002",
                description="Queso parmesano rallado",
                category="Lácteos",
                purchase_unit_id=kg_unit.id,
                usage_unit_id=g_unit.id,
                conversion_ratio=1000,
                conversion_unit="g",
                current_cost=12500.00,
                yield_factor=1.0,  # No waste (already processed)
                tax_rate=0.21,
                default_supplier_id=suppliers[0].id,
                stock_quantity=15.0,  # 15 kg en stock
                min_stock_threshold=3.0
            ),
            
            # Especias
            Ingredient(
                name="Sal Fina",
                sku="ESP-001",
                description="Sal fina de mesa",
                category="Especias",
                purchase_unit_id=kg_unit.id,
                usage_unit_id=g_unit.id,
                conversion_ratio=1000,
                conversion_unit="g",
                current_cost=180.00,
                yield_factor=1.0,
                tax_rate=0.21,
                default_supplier_id=suppliers[0].id,
                stock_quantity=50.0,  # 50 kg en stock
                min_stock_threshold=10.0
            ),
            Ingredient(
                name="Pimienta Negra",
                sku="ESP-002",
                description="Pimienta negra molida",
                category="Especias",
                purchase_unit_id=kg_unit.id,
                usage_unit_id=g_unit.id,
                conversion_ratio=1000,
                conversion_unit="g",
                current_cost=3500.00,
                yield_factor=1.0,
                tax_rate=0.21,
                default_supplier_id=suppliers[0].id,
                stock_quantity=10.0,  # 10 kg en stock
                min_stock_threshold=2.0
            ),
            
            # Aceites
            Ingredient(
                name="Aceite de Oliva",
                sku="ACEIT-001",
                description="Aceite de oliva extra virgen",
                category="Aceites",
                purchase_unit_id=l_unit.id,
                usage_unit_id=ml_unit.id,
                conversion_ratio=1000,
                conversion_unit="mL",
                current_cost=4500.00,
                yield_factor=1.0,
                tax_rate=0.21,
                default_supplier_id=suppliers[0].id,
                stock_quantity=30.0,  # 30 L en stock
                min_stock_threshold=10.0
            ),
        ]
        
        db.add_all(ingredients)
        db.commit()
        
        print("✅ Database initialized successfully!")
        print(f"   - {len(units)} units created")
        print(f"   - {len(suppliers)} suppliers created")
        print(f"   - {len(ingredients)} ingredients created")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Initializing cZr Catering Database...")
    init_db()
    print("🎉 Done!")
