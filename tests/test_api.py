import httpx

def test_get_rocket():
    url = "http://localhost:4000/rockets/123"
    response = httpx.get(url)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["id"] == 123