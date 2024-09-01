from pydantic import BaseModel, Field
from typing import Optional


class Career(BaseModel):
    id: Optional[int] = Field(None)
    name: str


class CareerDTO(BaseModel):
    id: Optional[int] = Field(None)
    name: str