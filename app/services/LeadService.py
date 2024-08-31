from app.repository.LeadRepository import LeadRepository
from app.models.Lead import Lead
from typing import List, Optional

class LeadService:
    def __init__(self, repository: LeadRepository):
        self.repository = repository

    def register_lead(self, name: str, last_name: str, email: str, address: Optional[str] = None, phone: Optional[str] = None) -> Lead:
        if not name or not last_name or not email:
            raise ValueError("Something fields are required")
        
        new_lead = self.repository.add_lead(name, last_name, email, address, phone)
        return new_lead
    
    def get_all_leads(self, skip: int = 0, limit: int = 10) -> List[Lead]:
        return self.repository.get_leads(skip, limit)
    
    def get_lead_by_id(self, lead_id: int) -> Lead:
        if not lead_id:
            raise ValueError("lead_id field is required")

        return self.repository.get_lead(lead_id)
