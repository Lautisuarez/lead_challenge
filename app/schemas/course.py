from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.schemas.subject import SubjectCreate
from app.schemas.lead import LeadCreate


class CourseBase(BaseModel):
    start_date: date
    end_date: date
    inscription_year: str
    lead: Optional[LeadCreate]
    subject: Optional[SubjectCreate]

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int

