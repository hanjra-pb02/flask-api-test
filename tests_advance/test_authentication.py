# tests/test_authentication.py
import pytest
import requests
import logging
logger = logging.getLogger("security_tests")

BASE_URL = "http://localhost:5002"

@pytest.mark.security
def test_invalid_token_rejected(invalid_auth_headers):
    resp = requests.get(f"{BASE_URL}/api/v2/profile", headers=invalid_auth_headers)
    assert resp.status_code == 401

@pytest.mark.security
def test_valid_token_rejected(auth_headers):
    resp = requests.get(f"{BASE_URL}/api/v2/profile", headers=auth_headers)
    assert resp.status_code == 200

@pytest.mark.security
def test_missing_token_rejected():
    resp = requests.get(f"{BASE_URL}/api/v2/profile")
    assert resp.status_code == 401

@pytest.mark.security
def test_invalid_session_rejected():
    s = requests.Session()
    resp = s.get(f"{BASE_URL}/api/v2/admin-data")
    assert resp.status_code == 401

@pytest.mark.security
def test_admin_session_access(session_login):
    resp = session_login.get(f"{BASE_URL}/api/v2/admin-data")
    assert resp.status_code == 200
    assert "system" in resp.json()
    logger.info(f"Response Headers: {resp.headers}")