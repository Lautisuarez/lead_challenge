from pydantic import BaseModel, EmailStr
from typing import Optional

class LeadBase(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    address: Optional[str] = None
    phone: Optional[str] = None

class LeadCreate(LeadBase):
    pass

class Lead(LeadBase):
    id: int