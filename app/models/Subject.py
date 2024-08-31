from pydantic import BaseModel, Field
from typing import Optional


class Subject(BaseModel):
    id: Optional[str] = Field(None)
    name: str
    career_id: int
