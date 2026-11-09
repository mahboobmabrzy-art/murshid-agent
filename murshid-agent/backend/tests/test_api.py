from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Murshid OS API"}

def test_create_project():
    response = client.post(
        "/projects/",
        json={"name": "Murshid Test", "description": "Checking API creation"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Murshid Test"
    assert "id" in data
