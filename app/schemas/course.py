from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.models.Lead import LeadDTO
from app.models.Subject import SubjectDTO


class CourseBase(BaseModel):
    start_date: date
    end_date: date
    inscription_year: str
    lead: Optional[LeadDTO]
    subject: Optional[SubjectDTO]

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int

