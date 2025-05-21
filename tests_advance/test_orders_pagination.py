# tests/test_orders_pagination.py
import pytest
import requests
from conftest import load_golden_file, compare_json
import logging
logger = logging.getLogger("api_tests")
logging.basicConfig(level=logging.INFO)

BASE_URL = "http://localhost:5002"

@pytest.mark.api
def test_orders_pagination_first_page(auth_headers):
    resp = requests.get(f"{BASE_URL}/api/v2/orders?page=1&page_size=2", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "orders" in data
    assert data["page"] == 1
    assert data["next_page"] == 2

    expected = load_golden_file('golden_orders_page1.json')
    diff = compare_json(expected, data, ignore_keys=[])
    assert not diff

@pytest.mark.api
def test_orders_pagination_second_page(auth_headers):
    resp = requests.get(f"{BASE_URL}/api/v2/orders?page=2&page_size=2", headers=auth_headers)
    logger.info(auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "orders" in data
    assert data["page"] == 2
    assert data["previous_page"] == 1

    expected = load_golden_file('golden_orders_page2.json')
    diff = compare_json(expected, data, ignore_keys=[])
    assert not diff

@pytest.mark.api
def test_orders_pagination_second_page(auth_headers):
    resp = requests.get(f"{BASE_URL}/api/v2/orders?page=2&page_size=2", headers=auth_headers)
    logger.info(auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "orders" in data
    assert data["page"] == 2
    assert data["previous_page"] == 1

    expected = load_golden_file('golden_orders_page2.json')
    diff = compare_json(expected, data, ignore_keys=[])
    assert not diff

