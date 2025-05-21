# tests/conftest.py
import pytest
import requests
import json
from deepdiff import DeepDiff
from tenacity import retry, stop_after_attempt, wait_fixed
import os

BASE_URL = "http://localhost:5002"
VALID_TOKEN = "secrettoken123"
AUTO_REGENERATE_GOLDEN = False  # Set to True to regenerate golden if mismatch

@pytest.fixture(scope="session", autouse=True)
@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def wait_for_server():
    try:
        resp = requests.get(BASE_URL)
        assert resp.status_code in [200, 404]
    except Exception as e:
        pytest.fail(f"Server not ready: {str(e)}")

@pytest.fixture
def auth_headers():
    return {"Authorization": f"Bearer {VALID_TOKEN}"}

@pytest.fixture
def invalid_auth_headers():
    return {"Authorization": "Bearer wrongtoken"}

@pytest.fixture
def session_login():
    s = requests.Session()
    payload = {"username": "admin", "password": "adminpass"}
    resp = s.post(f"{BASE_URL}/login", json=payload)
    assert resp.status_code == 200
    return s

def load_golden_file(filename):
    with open(f'golden/{filename}', 'r') as f:
        return json.load(f)

def save_golden_file(content, filename):
    with open(f'golden/{filename}', 'w') as f:
        json.dump(content, f, indent=2, sort_keys=True)

def compare_json(expected, actual, ignore_keys=None):
    if ignore_keys is None:
        ignore_keys = []
    diff = DeepDiff(
        expected,
        actual,
        ignore_order=True,
        exclude_regex_paths=[f"root['{key}']" for key in ignore_keys],
        significant_digits=2
    )
    return diff