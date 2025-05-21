import requests

def test_sql_injection_on_login():
    url = "https://api.example.com/login"
    payload = {"username": "' OR 1=1 --", "password": "irrelevant"}
    response = requests.post(url, json=payload)
    assert response.status_code in [401, 403]