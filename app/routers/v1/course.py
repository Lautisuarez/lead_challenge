from fastapi import APIRouter, Depends, HTTPException, status
from app.services.CourseService import CourseService
from app.schemas.course import CourseCreate
from app.models.Course import CourseDTO
from app.routers.dependencies import get_course_service

router = APIRouter()


@router.post("/", response_model=CourseDTO, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, service: CourseService = Depends(get_course_service)):
    try:
        return service.register_course_transaction(
            start_date=course.start_date,
            end_date=course.end_date,
            inscription_year=course.inscription_year,
            lead=course.lead,
            subject=course.subject
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Value Error Creating Course: {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error Creating Course: {e}")
