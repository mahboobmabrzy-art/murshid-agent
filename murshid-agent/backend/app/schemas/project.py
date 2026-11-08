from typing import Optional
from pydantic import BaseModel

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectResponse(ProjectCreate):
    id: int

    class Config:
        from_attributes = True
