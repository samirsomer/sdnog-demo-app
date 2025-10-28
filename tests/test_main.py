from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Hello SdNOG 🚀!"


def test_random_endpoint():
    response = client.get("/random")
    assert response.status_code == 200
    data = response.json()
    assert "random_number" in data
    assert 1 <= data["random_number"] <= 100


def test_slow_endpoint():
    response = client.get("/slow")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "This endpoint was slow"


def test_error_endpoint():
    response = client.get("/error")
    assert response.status_code == 500
    data = response.json()
    assert "error" in data
