from pydantic import BaseModel
from typing import Optional

class CareerBase(BaseModel):
    name: str

class CareerCreate(CareerBase):
    pass

class Career(CareerBase):
    id: Optional[int]