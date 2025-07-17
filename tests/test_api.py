import httpx
import pytest

def test_rockets():
    response = httpx.get("http://localhost:4000/rockets/123")
    assert response.status_code == 200
    assert 'id' in response.json()