# test_api.py
import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"
VALID_TOKEN = "secrettoken123"

@pytest.fixture
def auth_headers():
    return {"Authorization": f"Bearer {VALID_TOKEN}"}

@pytest.fixture
def invalid_auth_headers():
    return {"Authorization": "Bearer wrongtoken"}

# Test unauthorized access
@pytest.mark.security
def test_unauthorized_access():
    response = requests.get(f"{BASE_URL}/api/v1/data")
    assert response.status_code == 401
    assert "error" in response.json()

# Test valid access
@pytest.mark.api
def test_get_data(auth_headers):
    response = requests.get(f"{BASE_URL}/api/v1/data", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert "user" in data
    assert isinstance(data["user"]["orders"], list)
    assert "items" in data["user"]["orders"][0]

# Test another endpoint with parameterized tests
@pytest.mark.api
@pytest.mark.parametrize("endpoint", [
    "/api/v1/data",
    "/api/v1/users"
])
def test_endpoints_success(auth_headers, endpoint):
    response = requests.get(f"{BASE_URL}{endpoint}", headers=auth_headers)
    assert response.status_code == 200

# Test roles inside users
@pytest.mark.api
def test_user_roles(auth_headers):
    response = requests.get(f"{BASE_URL}/api/v1/users", headers=auth_headers)
    users = response.json()

    for user in users:
        assert "roles" in user
        assert isinstance(user["roles"], list)