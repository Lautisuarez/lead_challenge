from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class Course(BaseModel):
    id: Optional[str] = Field(None)
    start_date: date
    end_date: date
    inscription_year: str
    lead_id: int
    subject_id: int