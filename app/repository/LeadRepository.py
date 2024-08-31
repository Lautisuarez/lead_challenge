from app.dao.LeadDAO import LeadDAO
from app.models.Lead import Lead
from typing import List, Optional

class LeadRepository:
    def __init__(self, dao: LeadDAO):
        self.dao = dao

    def get_leads(self, skip: int = 0, limit: int = 10) -> List[Lead]:
        return self.dao.get_all(skip, limit)

    def get_lead(self, lead_id: int) -> Lead:
        return self.dao.get_lead_by_id(lead_id)

    def add_lead(self, name: str, last_name: str, email: str, address: Optional[str] = None, phone: Optional[str] = None) -> Lead:
        return self.dao.create(Lead(
            name=name,
            last_name=last_name,
            email=email,
            address=address,
            phone=phone
        ))