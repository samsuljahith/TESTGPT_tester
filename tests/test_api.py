import httpx
import pytest

def test_rockets_123():
    response = httpx.get('http://localhost:8000/rockets/123')
    assert response.status_code == 200
    assert 'id' in response.json()