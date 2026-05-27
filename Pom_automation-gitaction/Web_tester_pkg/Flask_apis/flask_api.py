import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request

app = Flask(__name__)

# Database configuration (adjust to your local setup)
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "Arvind@123")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

# 1. GET: Retrieve data
@app.route('/api/items', methods=['GET'])
def get_items():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM automation_schema.items ORDER BY id;')
    items = cur.fetchall()
    cur.close()
    conn.close()
    
    # Convert Decimal types to float for JSON serialization
    for item in items:
        item['price'] = float(item['price'])
        
    return jsonify({"items": items}), 200

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM automation_schema.items WHERE id = %s;', (item_id,))
    item = cur.fetchone()
    cur.close()
    conn.close()
    
    if item:
        item['price'] = float(item['price'])
        return jsonify({"item": item}), 200
    return jsonify({"error": "Item not found"}), 404

# 2. POST: Create new data
@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Invalid request, 'name' is required"}), 400
    
    fields = ['name']
    values = [data['name']]
    
    for key in ['description', 'price', 'quantity']:
        if key in data:
            fields.append(key)
            values.append(data[key])
            
    placeholders = ', '.join(['%s'] * len(values))
    query = f"INSERT INTO automation_schema.items ({', '.join(fields)}) VALUES ({placeholders}) RETURNING *;"
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(query, tuple(values))
    new_item = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    
    new_item['price'] = float(new_item['price'])
    return jsonify({"message": "Item created successfully", "item": new_item, "id": new_item['id']}), 201

# 3. PUT: Completely replace/update an existing resource
@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item_put(item_id):
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Invalid request, 'name' is required for a complete PUT update"}), 400
        
    name = data['name']
    description = data.get('description')
    price = data.get('price', 0.00)
    quantity = data.get('quantity', 0)
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        '''
        UPDATE automation_schema.items 
        SET name = %s, description = %s, price = %s, quantity = %s 
        WHERE id = %s RETURNING *;
        ''',
        (name, description, price, quantity, item_id)
    )
    updated_item = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    
    if updated_item:
        updated_item['price'] = float(updated_item['price'])
        return jsonify({"message": "Item completely updated", "item": updated_item}), 200
    return jsonify({"error": "Item not found"}), 404

# 4. PATCH: Partially update an existing resource
@app.route('/api/items/<int:item_id>', methods=['PATCH'])
def update_item_patch(item_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Empty request body"}), 400
        
    fields = []
    values = []
    allowed_fields = ['name', 'description', 'price', 'quantity']
    
    for key in allowed_fields:
        if key in data:
            fields.append(f"{key} = %s")
            values.append(data[key])
            
    if not fields:
        return jsonify({"error": "No valid fields provided for update"}), 400
        
    values.append(item_id)
    query = f"UPDATE automation_schema.items SET {', '.join(fields)} WHERE id = %s RETURNING *;"
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(query, tuple(values))
    updated_item = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    
    if updated_item:
        updated_item['price'] = float(updated_item['price'])
        return jsonify({"message": "Item partially updated", "item": updated_item}), 200
    return jsonify({"error": "Item not found"}), 404

# 5. DELETE: Remove a resource
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM automation_schema.items WHERE id = %s RETURNING id;', (item_id,))
    deleted_id = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    
    if deleted_id:
        return jsonify({"message": "Item deleted successfully"}), 200
    return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)  