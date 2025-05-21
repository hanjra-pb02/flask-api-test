# tests/test_profile_schema_golden.py
import pytest
import requests
from conftest import load_golden_file, compare_json, save_golden_file, BASE_URL, AUTO_REGENERATE_GOLDEN

@pytest.mark.golden
def test_profile_request_response_match(auth_headers):
    golden = load_golden_file('golden_profile.json')
    req = golden["request"]
    expected_response = golden["expected_response"]

    headers = auth_headers.copy()
    if "headers" in req:
        headers.update(req["headers"])

    url = BASE_URL + req["url"]
    method = req.get("method", "GET").upper()

    if method == "GET":
        resp = requests.get(url, headers=headers)
    elif method == "POST":
        resp = requests.post(url, json=req.get("body", {}), headers=headers)
    else:
        pytest.fail(f"Unsupported HTTP method {method}")

    assert resp.status_code == 200
    actual_response = resp.json()

    diff = compare_json(expected_response, actual_response, ignore_keys=["tracking_id", "uptime", "events"])

    if diff and AUTO_REGENERATE_GOLDEN:
        # Regenerate golden automatically if allowed
        print("[AUTO] Golden file updated due to diff!")
        golden["expected_response"] = actual_response
        save_golden_file(golden, 'golden_profile.json')

    assert not diff, f"Differences found: {diff}"