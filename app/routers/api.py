from fastapi import APIRouter
from app.routers.v1 import lead

router_v1 = APIRouter(
    prefix="/api/v1"
)

router_v1.include_router(lead.router,  prefix='/lead', tags=["Lead"])