from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)


# Function to get a database connection
def get_db_connection():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "database.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # This makes rows dictionary-like
    # conn = sqlite3.connect('./database.db')
    # conn.row_factory = sqlite3.Row
    # db_filename = './database.db'
    # absolute_path = os.path.abspath(db_filename)
    # print("Connecting to database at:", absolute_path)
    # conn = sqlite3.connect(absolute_path)
    return conn

# GET endpoint to fetch items
@app.route('/items', methods=['GET'])
def get_items():
    print("GET /items")
    conn = get_db_connection()
    cursor = conn.cursor()
    items = cursor.execute('SELECT * FROM customers').fetchall()
    conn.close()
    # Convert rows to dictionaries
    return jsonify([dict(item) for item in items])

# POST endpoint to add a new item
# @app.route('/items', methods=['POST'])
# def add_item():
#     new_item = request.json.get('name')
#     if not new_item:
#         return jsonify({'error': 'No item name provided'}), 400

#     conn = get_db_connection()
#     conn.execute('INSERT INTO items (name) VALUES (?)', (new_item,))
#     conn.commit()
#     conn.close()
#     return jsonify({'message': 'Item added'}), 201


if __name__ == '__main__':
    # Listen on all interfaces so that Docker can expose the port
    app.run(host='0.0.0.0', port=5000)
