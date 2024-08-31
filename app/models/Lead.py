from pydantic import BaseModel, Field
from typing import Optional


class Lead(BaseModel):
    id: Optional[int] = Field(None)
    name: str
    last_name: str
    email: str
    address: Optional[str] = None
    phone: Optional[str] = None