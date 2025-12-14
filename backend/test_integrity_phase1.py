¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬st
import json
import time

BASE_URL = "http://0.0.0.0:8000/api/v1"

def make_request(method, endpoint, data=None):
    url = f"{BASE_URL}/{endpoint}"
    req = urllib.request.Request(url, method=method)
    req.add_header('Content-Type', 'application/json')
    
    body = None
    if data:
        body = json.dumps(data).encode('utf-8')
        
    try:
        with urllib.request.urlopen(req, data=body) as response:
            return {
                "status": response.status,
                "body": json.loads(response.read().decode('utf-8'))
            }
    except urllib.error.HTTPError as e:
        return {
            "status": e.code,
            "body": e.read().decode('utf-8')
        }
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def test_price_history():
    print(">>> Testing Price History Integrity...")
    
    # 1. Get an existing ingredient
    res = make_request("GET", "ingredients/?limit=1")
    if not res or not res['body']['items']:
        # Create dummy
        dummy = {
            "name": "Harina Test Integrity",
            "purchase_unit_id": 1,
            "usage_unit_id": 2,
            "current_cost": 100
        }
        res = make_request("POST", "ingredients/", dummy)
        ing = res['body']
    else:
        ing = res['body']['items'][0]
        
    ing_id = ing['id']
    old_cost = ing['current_cost']
    new_cost = old_cost + 50.0
    
    # 2. Update price
    print(f"Updating Ingredient {ing_id} cost from {old_cost} to {new_cost}")
    res = make_request("PUT", f"ingredients/{ing_id}", {"current_cost": new_cost})
    
    if res['status'] != 200:
        print(f"FAILED to update ingredient: {res['body']}")
        return
        
    print("Update successful. API returned 200.")
    print("Check backend logs or database for 'IngredientPriceHistory' entry to be 100% sure.")

def test_event_snapshot():
    print("\n>>> Testing Event Snapshot...")
    # 1. Create Event
    event_data = {
        "name": "Snapshot Test Event Host",
        "event_date": "2025-12-25",
        "guest_count": 100,
        "client_name": "Test Client"
    }
    res = make_request("POST", "events/", event_data)
    if not res or res['status'] != 200:
        print(f"Failed to create event: {res}")
        return
    event_id = res['body']['id']
    
    # 2. Get a recipe
    res = make_request("GET", "recipes/?limit=1")
    if not res or not res['body']['items']:
         print("No recipes found. Skipping item test.")
         return
    recipe_id = res['body']['items'][0]['id']
    
    # 3. Add Item to Event
    print(f"Adding Recipe {recipe_id} to Event {event_id}")
    item_data = {"recipe_id": recipe_id, "quantity": 10}
    res = make_request("POST", f"events/{event_id}/items", item_data)
    
    if not res or res['status'] != 200:
        print(f"Failed to add item: {res}")
        return
        
    order = res['body']
    cost_frozen = order.get('cost_at_sale')
    print(f"Order created. Frozen Cost per unit: {cost_frozen}")
    
    if cost_frozen is not None:
        print("SUCCESS: Cost was captured and frozen.")
    else:
        print("WARNING: Cost is missing in response.")

if __name__ == "__main__":
    test_price_history()
    test_event_snapshot()
