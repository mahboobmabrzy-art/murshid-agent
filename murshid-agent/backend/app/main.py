from fastapi import FastAPI
from app.database import engine, Base
from app.routers import projects

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Murshid OS API")

app.include_router(projects.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Murshid OS API"}
