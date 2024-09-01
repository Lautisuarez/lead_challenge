from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from app.models.Lead import LeadDTO
from app.models.Subject import SubjectDTO


class Course(BaseModel):
    id: Optional[str] = Field(None)
    start_date: date
    end_date: date
    inscription_year: str
    lead_id: int
    subject_id: int


class CourseDTO(BaseModel):
    id: Optional[str] = Field(None)
    start_date: date
    end_date: date
    inscription_year: str
    lead: LeadDTO
    subject: SubjectDTO