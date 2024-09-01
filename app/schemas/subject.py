from pydantic import BaseModel
from typing import Optional
from app.schemas.career import CareerCreate
from app.models.Career import Career

class SubjectBase(BaseModel):
    name: str

class SubjectCreate(SubjectBase):
    career: Optional[CareerCreate]

class Subject(SubjectBase):
    id: int
    career: Optional[Career]