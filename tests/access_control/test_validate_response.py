import requests
from utils.common import validate_response

def test_response_with_ignored_fields():
    url = "https://api.example.com/profile"
    expected = {
        "user_id": 123,
        "name": "John Doe",
        "last_login": "ignore_this"
    }

    response = requests.get(url, headers={"Authorization": "Bearer <token>"})
    actual = response.json()

    assert validate_response(expected, actual, ignore_keys=["last_login"])