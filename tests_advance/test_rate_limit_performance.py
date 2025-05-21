# tests/test_rate_limit_performance.py
import pytest
import requests
import time

BASE_URL = "http://localhost:5002"

@pytest.mark.performance
def test_profile_response_time(auth_headers):
    start_time = time.time()
    resp = requests.get(f"{BASE_URL}/api/v2/profile", headers=auth_headers)
    elapsed = (time.time() - start_time) * 1000  # milliseconds
    assert resp.status_code == 200, f"Expected 200 OK but got {resp.status_code}"
    assert elapsed < 300, f"API response too slow: {elapsed:.2f}ms"

@pytest.mark.rate_limit
def test_rate_limit_exceeded(auth_headers):
    success_count = 0
    too_many_requests_count = 0

    for _ in range(1):
        resp = requests.get(f"{BASE_URL}/api/v2/profile", headers=auth_headers)
        if resp.status_code == 200:
            success_count += 1
        elif resp.status_code == 429:
            too_many_requests_count += 1
            break  # As soon as we see 429, we can stop.
    
    assert success_count > 0, "Did not receive any successful responses"
    assert too_many_requests_count > 0, "Did not hit rate limit even after 100 requests"
    print(f"Hit rate limit after {success_count} successful requests")