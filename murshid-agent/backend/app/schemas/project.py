from typing import Optional
from pydantic import BaseModel, ConfigDict

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectResponse(ProjectCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
