from fastapi.testclient import TestClient
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Murshid OS API"}

@app.post("/projects/")
def create_project(project: dict):
    return {"id": 1, "name": project.get("name"), "description": project.get("description")}

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
