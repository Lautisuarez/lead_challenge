from fastapi import APIRouter
from app.routers.v1 import course

router_v1 = APIRouter(
    prefix="/api/v1"
)

router_v1.include_router(course.router,  prefix='/course', tags=["Course"])