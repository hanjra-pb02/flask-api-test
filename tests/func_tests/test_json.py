from jsonschema import validate
import pytest
import requests
import json

user_schema = {
    "type": "object",
    "properties": {
        "user": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "orders": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "order_id": {"type": "string"},
                            "items": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "product_id": {"type": "string"},
                                        "name": {"type": "string"},
                                        "tags": {"type": "array", "items": {"type": "string"}}
                                    },
                                    "required": ["product_id", "name", "tags"]
                                }
                            }
                        },
                        "required": ["order_id", "items"]
                    }
                }
            },
            "required": ["id", "name", "orders"]
        }
    },
    "required": ["user"]
}
BASE_URL = "http://127.0.0.1:5000"
VALID_TOKEN = "secrettoken123"

@pytest.mark.schema
def test_validate_user_data_schema(auth_headers):
    response = requests.get(f"{BASE_URL}/api/v1/data", headers=auth_headers)
    assert response.status_code == 200

    validate(instance=response.json(), schema=user_schema)


@pytest.mark.golden
def test_golden_file_validation(auth_headers):
    response = requests.get(f"{BASE_URL}/api/v1/users", headers=auth_headers)
    actual = response.json()

    expected = load_golden_file('golden_users.json')
    
    assert actual == expected

@pytest.mark.feature
@pytest.mark.parametrize("flag_status", [True, False])
def test_feature_flag_behavior(auth_headers, flag_status):
    headers = auth_headers.copy()
    headers["X-Feature-NewFlow"] = str(flag_status).lower()  # inject custom feature flag header

    response = requests.get(f"{BASE_URL}/api/v1/data", headers=headers)
    assert response.status_code == 200

    data = response.json()

    if flag_status:
        # Validate behavior when feature ON
        assert "new_feature_enabled" in data.get("user", {})
    else:
        # Validate behavior when feature OFF
        assert "new_feature_enabled" not in data.get("user", {})

def save_golden_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, sort_keys=True)

def load_golden_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)