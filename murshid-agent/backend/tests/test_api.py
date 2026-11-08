from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Murshid OS API"}

def test_create_and_get_project():
    response = client.post(
        "/projects/",
        json={"name": "Murshid Test Project", "description": "Automated test project"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Murshid Test Project"
    assert "id" in data
    
    project_id = data["id"]
    get_response = client.get(f"/projects/{project_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Murshid Test Project"
