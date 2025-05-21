# tests/test_profile_schema_golden.py
import pytest
import requests
from jsonschema import validate
from conftest import load_golden_file, compare_json

BASE_URL = "http://localhost:5002"

schema_profile = {
    "type": "object",
    "properties": {
        "profile": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "preferences": {"type": "object"},
                "activities": {"type": "array"}
            }
        }
    },
    "required": ["profile"]
}

@pytest.mark.schema
def test_profile_schema_valid(auth_headers):
    resp = requests.get(f"{BASE_URL}/api/v2/profile", headers=auth_headers)
    assert resp.status_code == 200
    validate(instance=resp.json(), schema=schema_profile)

@pytest.mark.golden
def test_profile_golden_match(auth_headers):
    resp = requests.get(f"{BASE_URL}/api/v2/profile", headers=auth_headers)
    actual = resp.json()
    expected = load_golden_file('golden_profile.json')
    diff = compare_json(expected, actual, ignore_keys=["tracking_id", "uptime", "events"])
    assert not diff, f"Mismatch found: {diff}"