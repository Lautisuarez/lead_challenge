from pydantic import BaseModel, Field
from typing import Optional
from app.models.Career import CareerDTO

class Subject(BaseModel):
    id: Optional[int] = Field(None)
    name: str
    career_id: int

class SubjectDTO(BaseModel):
    id: Optional[int] = Field(None)
    name: str
    career: CareerDTO