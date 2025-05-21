import pytest
import requests

BASE_URL = "http://localhost:5002"

@pytest.mark.api
def test_compute_square():
    headers = {"Authorization": "Bearer secrettoken123"}
    payload = {"action": "square", "value": 5} 
    resp = requests.post(f"{BASE_URL}/api/v2/compute", json=payload, headers=headers)

    assert resp.status_code == 200
    data = resp.json()
    assert data["result"] == 25

@pytest.mark.api
def test_compute_double():
    headers = {"Authorization": "Bearer secrettoken123"}
    payload = {"action": "double", "value": 5}
    resp = requests.post(f"{BASE_URL}/api/v2/compute", json=payload, headers=headers)

    assert resp.status_code == 200
    data = resp.json()
    assert data["result"] == 10

@pytest.mark.api
def test_compute_invalid_action():
    headers = {"Authorization": "Bearer secrettoken123"}
    payload = {"action": "invalid", "value": 5}
    resp = requests.post(f"{BASE_URL}/api/v2/compute", json=payload, headers=headers)

    assert resp.status_code == 400
    data = resp.json()
    assert "error" in data

@pytest.mark.api
def test_compute_missing_value():
    headers = {"Authorization": "Bearer secrettoken123"}
    payload = {"action": "square"}
    resp = requests.post(f"{BASE_URL}/api/v2/compute", json=payload, headers=headers)

    assert resp.status_code == 400
    data = resp.json()
    assert "error" in data