# fake_api.py
from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy auth token
VALID_TOKEN = "secrettoken123"

# Authentication check decorator
def require_auth(f):
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token != f"Bearer {VALID_TOKEN}":
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Endpoint 1: Nested JSON
@app.route('/api/v1/data', methods=['GET'])
@require_auth
def get_data():
    response = {
        "user": {
            "id": 123,
            "name": "John Doe",
            "orders": [
                {
                    "order_id": "A100",
                    "items": [
                        {"product_id": "P1", "name": "Book", "tags": ["education", "reading"]},
                        {"product_id": "P2", "name": "Laptop", "tags": ["electronics", "work"]}
                    ]
                },
                {
                    "order_id": "A101",
                    "items": [
                        {"product_id": "P3", "name": "Desk", "tags": ["furniture", "office"]}
                    ]
                }
            ]
        }
    }
    return jsonify(response)

# Endpoint 2: List of users
@app.route('/api/v1/users', methods=['GET'])
@require_auth
def list_users():
    response = [
        {"id": 1, "name": "Alice", "roles": ["admin", "editor"]},
        {"id": 2, "name": "Bob", "roles": ["viewer"]},
        {"id": 3, "name": "Charlie", "roles": ["editor", "contributor", "reviewer"]}
    ]
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)