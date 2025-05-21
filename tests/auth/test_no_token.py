import requests

def test_authentication_without_token():
    url = "https://api.example.com/protected-endpoint"
    response = requests.get(url)
    assert response.status_code == 401