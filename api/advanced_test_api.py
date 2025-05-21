# fake_api_advanced_v3.py
from flask import Flask, jsonify, request, session
import random
import string
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Hardcoded token
VALID_TOKEN = "secrettoken123"

# User database simulation
USERS = {
    "admin": {"role": "admin", "password": "adminpass"},
    "user": {"role": "user", "password": "userpass"}
}

# Simulate rate-limiting
RATE_LIMIT = 50
request_counters = {}

# ---------------- Authentication ----------------

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if username in USERS and USERS[username]["password"] == password:
        session['username'] = username
        return jsonify({"message": "Login successful", "session_active": True})
    return jsonify({"error": "Unauthorized"}), 401

def token_required(f):
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token != f"Bearer {VALID_TOKEN}":
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

def session_required(f):
    def decorated(*args, **kwargs):
        if 'username' not in session:
            return jsonify({"error": "Session Unauthorized"}), 401
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

# ---------------- Utilities ----------------

def generate_tracking_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

def current_time():
    return int(time.time())

def check_rate_limit(ip):
    count = request_counters.get(ip, 0)
    if count >= RATE_LIMIT:
        return False
    request_counters[ip] = count + 1
    return True

# ---------------- APIs ----------------

@app.route('/api/v2/profile', methods=['GET'])
@token_required
def get_profile_v3():
    # ip = request.remote_addr
    # if not check_rate_limit(ip):
    #     return jsonify({"error": "Rate Limit Exceeded"}), 429

    enable_tracking = request.headers.get('X-Feature-Tracking', 'false') == 'true'
    new_flow = request.headers.get('X-Feature-NewFlow', 'false') == 'true'

    profile_data = {
        "profile": {
            "id": 101,
            "name": "John Doe",
            "preferences": {
                "notifications": True,
                "categories": [
                    {"main": "technology", "sub": ["ai", "cloud"]},
                    {"main": "books", "sub": ["fiction", "non-fiction"]}
                ]
            },
            "activities": [
                {
                    "activity": "login",
                    "events": [
                        {"timestamp": "2024-04-01T12:00:00Z", "device": "web"},
                        {"timestamp": "2024-04-02T14:00:00Z", "device": "mobile"}
                    ]
                }
            ]
        }
    }

    if enable_tracking:
        profile_data["profile"]["tracking_id"] = generate_tracking_id()

    if new_flow:
        profile_data["profile"]["preferences"]["beta_features"] = ["dark_mode", "quick_search"]

    return jsonify(profile_data)

@app.route('/api/v2/admin-data', methods=['GET'])
@session_required
def get_admin_data_v3():
    username = session.get('username')
    user = USERS.get(username)
    if user and user["role"] == "admin":
        return jsonify({
            "system": {
                "health": "good",
                "services": [
                    {"name": "auth", "status": "running", "uptime": current_time()},
                    {"name": "db", "status": "running", "uptime": current_time()}
                ]
            }
        })
    return jsonify({"error": "Forbidden"}), 403

@app.route('/api/v2/orders', methods=['GET'])
@token_required
def get_orders():
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 2))
    
    all_orders = [
        {"order_id": "A100", "amount": 250.50, "status": "shipped"},
        {"order_id": "A101", "amount": 540.00, "status": "processing"},
        {"order_id": "A102", "amount": 99.99, "status": "shipped"},
        {"order_id": "A103", "amount": 120.75, "status": "cancelled"}
    ]

    start = (page - 1) * page_size
    end = start + page_size
    paginated_orders = all_orders[start:end]

    next_page = page + 1 if end < len(all_orders) else None
    previous_page = page - 1 if page > 1 else None

    response = {
        "orders": paginated_orders,
        "page": page,
        "page_size": page_size,
        "next_page": next_page,
        "previous_page": previous_page,
        "total_orders": len(all_orders)
    }

    return jsonify(response)

@app.route('/api/v2/fault', methods=['POST'])
def fault_injection():
    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400
    data = request.json
    if "expected_field" not in data:
        return jsonify({"error": "Missing expected_field"}), 400
    return jsonify({"message": "OK"})

# Healthcheck
@app.route('/', methods=['GET'])
def healthcheck():
    return jsonify({"status": "API Running"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5002)

@app.route('/api/v2/compute', methods=['POST'])
@token_required
def compute_value():
    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400

    data = request.json
    action = data.get("action")
    value = data.get("value")

    if action == "square" and isinstance(value, (int, float)):
        result = value * value
        return jsonify({"action": action, "input": value, "result": result})
    
    elif action == "double" and isinstance(value, (int, float)):
        result = value * 2
        return jsonify({"action": action, "input": value, "result": result})
    
    else:
        return jsonify({"error": "Invalid action or value"}), 400