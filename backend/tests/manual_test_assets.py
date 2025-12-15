import sys
import os
from unittest.mock import MagicMock

# Add parent dir (backend) to path
try:
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(backend_dir)
except:
    pass

from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../.env')
load_dotenv(env_path)

from app.services.asset_service import AssetService
from app.models.asset import Asset, AssetState
from fastapi import HTTPException

def test_assets_logic():
    print("Testing Asset Availability Logic...")
    
    # Mock Asset
    # ID 1: "Round Table", Qty 10
    asset_1 = Asset(id=1, name="Round Table", total_quantity=10, state=AssetState.AVAILABLE)
    
    # Mock DB
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_filter = MagicMock()
    
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_filter
    
    # Side effect for finding asset
    def first_side_effect():
        return asset_1
    
    mock_filter.first.side_effect = first_side_effect
    
    # Test 1: Check availability for 5 tables (Should pass)
    print(" Check 1: Need 5 (Have 10) -> Expect True")
    result = AssetService.check_availability(mock_db, 1, 5)
    assert result is True
    
    # Test 2: Check availability for 15 tables (Should raise 400)
    print(" Check 2: Need 15 (Have 10) -> Expect Error 400")
    try:
        AssetService.check_availability(mock_db, 1, 15)
        print(" ❌ Failed: Should have raised exception")
    except HTTPException as e:
        assert e.status_code == 400
        print(" ✅ Correctly raised 400 Not Enough Assets")
        
    print("✅ Assets Logic Validated.")

if __name__ == "__main__":
    test_assets_logic()
