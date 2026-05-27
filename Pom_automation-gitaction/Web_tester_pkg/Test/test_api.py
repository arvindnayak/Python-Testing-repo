import pytest
import requests
import uuid
import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Dynamically get the API URL, falling back to localhost for local testing
BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:5000/api/items")

# Database configuration mirroring your Flask app
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "Arvind@123")

@pytest.fixture
def db_cursor():
    """Fixture to provide a database cursor for direct database assertions."""
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    yield cur
    cur.close()
    conn.close()

@pytest.fixture
def test_item_id():
    """
    Fixture to create a temporary item in the database before a test runs,
    yield its ID to the test, and automatically clean it up (delete it) afterwards.
    """
    payload = {
        "name": f"Test Item {uuid.uuid4()}",
        "description": "Created for automated testing",
        "price": 9.99,
        "quantity": 10
    }
    response = requests.post(BASE_URL, json=payload)
    item_id = response.json().get("id")
    
    yield item_id
    
    # Teardown / Cleanup
    requests.delete(f"{BASE_URL}/{item_id}")

# ==========================================
# GET /api/items Tests
# ==========================================

def test_get_all_items_status_200():
    response = requests.get(BASE_URL)
    assert response.status_code == 200

def test_get_all_items_contains_items_list():
    response = requests.get(BASE_URL)
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)

# ==========================================
# POST /api/items Tests
# ==========================================

def test_create_item_success(db_cursor):
    payload = {"name": "New Item", "price": 15.00, "quantity": 2}
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 201
    
    item_id = response.json().get("id")
    
    # DB Check: Verify it was actually inserted
    db_cursor.execute("SELECT * FROM automation_schema.items WHERE id = %s;", (item_id,))
    db_item = db_cursor.fetchone()
    assert db_item is not None
    assert db_item["name"] == "New Item"
    assert float(db_item["price"]) == 15.00
    assert db_item["quantity"] == 2

    # Cleanup the manually created item
    if item_id:
        requests.delete(f"{BASE_URL}/{item_id}")

def test_create_item_response_data():
    payload = {"name": "Data Match Item", "description": "Testing data", "price": 25.50, "quantity": 1}
    response = requests.post(BASE_URL, json=payload)
    data = response.json()
    
    assert data["message"] == "Item created successfully"
    assert data["item"]["name"] == "Data Match Item"
    assert data["item"]["price"] == 25.50
    
    requests.delete(f"{BASE_URL}/{data['id']}") 

def test_create_item_missing_name_returns_400():
    payload = {"description": "No name", "price": 10.0}
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 400
    assert "error" in response.json()

def test_create_item_empty_payload_returns_400():
    response = requests.post(BASE_URL, json={})
    assert response.status_code == 400

# ==========================================
# GET /api/items/<id> Tests
# ==========================================

def test_get_item_by_id_success(test_item_id):
    response = requests.get(f"{BASE_URL}/{test_item_id}")
    assert response.status_code == 200
    assert response.json()["item"]["id"] == test_item_id

def test_get_item_by_id_not_found():
    response = requests.get(f"{BASE_URL}/99999999")
    assert response.status_code == 404
    assert response.json()["error"] == "Item not found"

def test_get_item_invalid_id_format():
    # Flask routing '<int:item_id>' will automatically reject string IDs
    response = requests.get(f"{BASE_URL}/invalid_id")
    assert response.status_code == 404

# ==========================================
# PUT /api/items/<id> Tests
# ==========================================

def test_put_update_success(test_item_id, db_cursor):
    payload = {"name": "Updated Name PUT", "description": "Updated Desc", "price": 100.0, "quantity": 50}
    response = requests.put(f"{BASE_URL}/{test_item_id}", json=payload)
    assert response.status_code == 200
    assert response.json()["item"]["name"] == "Updated Name PUT"
    
    # DB Check: Verify the database record was completely updated
    db_cursor.execute("SELECT * FROM automation_schema.items WHERE id = %s;", (test_item_id,))
    db_item = db_cursor.fetchone()
    assert db_item["name"] == "Updated Name PUT"
    assert db_item["description"] == "Updated Desc"
    assert float(db_item["price"]) == 100.0
    assert db_item["quantity"] == 50

def test_put_update_missing_name(test_item_id):
    payload = {"description": "Missing name update"}
    response = requests.put(f"{BASE_URL}/{test_item_id}", json=payload)
    assert response.status_code == 400

def test_put_update_not_found():
    payload = {"name": "Doesn't exist"}
    response = requests.put(f"{BASE_URL}/99999999", json=payload)
    assert response.status_code == 404

# ==========================================
# PATCH /api/items/<id> Tests
# ==========================================

def test_patch_update_success(test_item_id, db_cursor):
    payload = {"name": "Patched Name", "quantity": 99}
    response = requests.patch(f"{BASE_URL}/{test_item_id}", json=payload)
    assert response.status_code == 200
    assert response.json()["item"]["name"] == "Patched Name"
    assert response.json()["item"]["quantity"] == 99
    
    # DB Check: Verify only the provided fields were modified
    db_cursor.execute("SELECT * FROM automation_schema.items WHERE id = %s;", (test_item_id,))
    db_item = db_cursor.fetchone()
    assert db_item["name"] == "Patched Name"
    assert db_item["quantity"] == 99

def test_patch_update_price_only(test_item_id):
    payload = {"price": 999.99}
    response = requests.patch(f"{BASE_URL}/{test_item_id}", json=payload)
    assert response.status_code == 200
    assert response.json()["item"]["price"] == 999.99

def test_patch_update_empty_payload(test_item_id):
    response = requests.patch(f"{BASE_URL}/{test_item_id}", json={})
    assert response.status_code == 400

def test_patch_update_not_found():
    response = requests.patch(f"{BASE_URL}/99999999", json={"price": 50.0})
    assert response.status_code == 404

# ==========================================
# DELETE /api/items/<id> Tests
# ==========================================

def test_delete_item_success(test_item_id, db_cursor):
    response = requests.delete(f"{BASE_URL}/{test_item_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Item deleted successfully"
    
    # DB Check: Verify the record is actually gone from the database
    db_cursor.execute("SELECT * FROM automation_schema.items WHERE id = %s;", (test_item_id,))
    db_item = db_cursor.fetchone()
    assert db_item is None

def test_delete_item_not_found():
    response = requests.delete(f"{BASE_URL}/99999999")
    assert response.status_code == 404

def test_get_item_after_delete(test_item_id):
    requests.delete(f"{BASE_URL}/{test_item_id}") # Delete first
    response = requests.get(f"{BASE_URL}/{test_item_id}") # Then try to get
    assert response.status_code == 404

# ==========================================
# EDGE CASE / METHOD VERIFICATION
# ==========================================

def test_post_to_specific_item_returns_405(test_item_id):
    # The endpoint /api/items/<id> only accepts GET, PUT, PATCH, DELETE
    response = requests.post(f"{BASE_URL}/{test_item_id}", json={"name": "test"})
    assert response.status_code == 405