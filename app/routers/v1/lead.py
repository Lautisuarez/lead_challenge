from typing import List
from fastapi import APIRouter, HTTPException, Query
from app.models.Lead import Lead
from app.services.LeadService import LeadService
from app.repository.LeadRepository import LeadRepository
from app.dao.LeadDAO import LeadDAOPostgresql
from app.utils.config import settings
from app.schemas.lead import LeadCreate

router = APIRouter()
dao = LeadDAOPostgresql(settings.db_manager)
repository = LeadRepository(dao)
service = LeadService(repository)

@router.get("/", response_model=List[Lead])
def read_leads(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1)):
    """ 
    This is used to get all leads. It includes pagination.
    
    **Params**:
    - skip: int => where the search starts from
    - limit: int => number of leads returned
    
    **Return**: A list of leads
    """
    leads = service.get_all_leads(skip, limit)
    if leads:
        return leads
    else: 
        raise HTTPException(status_code=404, detail=f"There are no leads")

@router.get("/{lead_id}", response_model=Lead)
def read_lead(lead_id: int):
    """
    Gets a lead by its ID

    **Params**:
    - lead_id: int => ID of the lead to search for

    **Return**: The lead found
    """
    lead = service.get_lead_by_id(lead_id)
    if lead:
        return lead
    else: 
        raise HTTPException(status_code=404, detail=f"Lead with ID: {lead_id} not found")

@router.post("/", response_model=Lead)
def create_lead(lead: LeadCreate):
    lead = service.register_lead(lead.name, lead.last_name, lead.email, lead.address, lead.phone)
    return lead