from fastapi import FastAPI
from app.routers import project, task

app = FastAPI(title="Murshid OS API", version="1.0.0")

app.include_router(project.router)
app.include_router(task.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Murshid OS API"}
