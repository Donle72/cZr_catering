"""
Tests for validation logic
Covers Pydantic validators and business rule validations
"""
import pytest
from pydantic import ValidationError
from app.schemas.ingredient import IngredientCreate, IngredientUpdate


class TestIngredientValidations:
    """Test ingredient schema validations"""
    
    def test_yield_factor_valid_range(self):
        """Test valid yield factor values"""
        # Valid values
        for yield_factor in [0.5, 0.75, 0.95, 1.0]:
            data = {
                "name": "Test",
                "yield_factor": yield_factor,
                "purchase_unit_id": 1,
                "usage_unit_id": 1
            }
            ingredient = IngredientCreate(**data)
            assert ingredient.yield_factor == yield_factor
    
    def test_yield_factor_too_high(self):
        """Test yield factor > 1.0 fails"""
        with pytest.raises(ValidationError) as exc_info:
            IngredientCreate(
                name="Test",
                yield_factor=1.5,
                purchase_unit_id=1,
                usage_unit_id=1
            )
        
        assert "yield_factor" in str(exc_info.value).lower()
    
    def test_yield_factor_zero(self):
        """Test yield factor = 0 fails"""
        with pytest.raises(ValidationError):
            IngredientCreate(
                name="Test",
                yield_factor=0.0,
                purchase_unit_id=1,
                usage_unit_id=1
            )
    
    def test_yield_factor_negative(self):
        """Test negative yield factor fails"""
        with pytest.raises(ValidationError):
            IngredientCreate(
                name="Test",
                yield_factor=-0.5,
                purchase_unit_id=1,
                usage_unit_id=1
            )
    
    def test_yield_factor_very_low_warning(self):
        """Test very low yield factor (< 0.1) triggers validation"""
        with pytest.raises(ValidationError) as exc_info:
            IngredientCreate(
                name="Test",
                yield_factor=0.05,
                purchase_unit_id=1,
                usage_unit_id=1
            )
        
        error_msg = str(exc_info.value).lower()
        assert "too low" in error_msg or "yield" in error_msg
    
    def test_cost_non_negative(self):
        """Test cost must be non-negative"""
        # Valid: zero cost
        ingredient = IngredientCreate(
            name="Test",
            current_cost=0.0,
            purchase_unit_id=1,
            usage_unit_id=1
        )
        assert ingredient.current_cost == 0.0
        
        # Invalid: negative cost
        with pytest.raises(ValidationError):
            IngredientCreate(
                name="Test",
                current_cost=-100.0,
                purchase_unit_id=1,
                usage_unit_id=1
            )
    
    def test_cost_very_high_warning(self):
        """Test very high cost triggers validation"""
        with pytest.raises(ValidationError) as exc_info:
            IngredientCreate(
                name="Test",
                current_cost=2000000.0,  # 2 million
                purchase_unit_id=1,
                usage_unit_id=1
            )
        
        assert "high" in str(exc_info.value).lower()
    
    def test_conversion_ratio_positive(self):
        """Test conversion ratio must be positive"""
        # Valid
        ingredient = IngredientCreate(
            name="Test",
            conversion_ratio=1000.0,
            purchase_unit_id=1,
            usage_unit_id=1
        )
        assert ingredient.conversion_ratio == 1000.0
        
        # Invalid: zero
        with pytest.raises(ValidationError):
            IngredientCreate(
                name="Test",
                conversion_ratio=0.0,
                purchase_unit_id=1,
                usage_unit_id=1
            )
        
        # Invalid: negative
        with pytest.raises(ValidationError):
            IngredientCreate(
                name="Test",
                conversion_ratio=-5.0,
                purchase_unit_id=1,
                usage_unit_id=1
            )
    
    def test_name_minimum_length(self):
        """Test name must be at least 3 characters"""
        # Valid
        ingredient = IngredientCreate(
            name="ABC",
            purchase_unit_id=1,
            usage_unit_id=1
        )
        assert ingredient.name == "ABC"
        
        # Invalid: too short
        with pytest.raises(ValidationError):
            IngredientCreate(
                name="AB",
                purchase_unit_id=1,
                usage_unit_id=1
            )
    
    def test_name_trimmed(self):
        """Test name is trimmed of whitespace"""
        ingredient = IngredientCreate(
            name="  Test Ingredient  ",
            purchase_unit_id=1,
            usage_unit_id=1
        )
        assert ingredient.name == "Test Ingredient"
    
    def test_tax_rate_valid_range(self):
        """Test tax rate must be between 0 and 1"""
        # Valid values
        for tax_rate in [0.0, 0.21, 0.5, 1.0]:
            ingredient = IngredientCreate(
                name="Test",
                tax_rate=tax_rate,
                purchase_unit_id=1,
                usage_unit_id=1
            )
            assert ingredient.tax_rate == tax_rate
        
        # Invalid: > 1.0
        with pytest.raises(ValidationError):
            IngredientCreate(
                name="Test",
                tax_rate=1.5,
                purchase_unit_id=1,
                usage_unit_id=1
            )
        
        # Invalid: negative
        with pytest.raises(ValidationError):
            IngredientCreate(
                name="Test",
                tax_rate=-0.1,
                purchase_unit_id=1,
                usage_unit_id=1
            )
    
    def test_update_partial_validation(self):
        """Test that update validates only provided fields"""
        # Update with valid yield factor
        update = IngredientUpdate(yield_factor=0.85)
        assert update.yield_factor == 0.85
        
        # Update with invalid yield factor
        with pytest.raises(ValidationError):
            IngredientUpdate(yield_factor=1.5)
        
        # Update without yield factor (should work)
        update = IngredientUpdate(name="New Name")
        assert update.name == "New Name"
        assert update.yield_factor is None
