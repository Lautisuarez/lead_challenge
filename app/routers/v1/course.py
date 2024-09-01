from fastapi import APIRouter, Depends, HTTPException, status
from app.services.CourseService import CourseService
from app.schemas.course import CourseCreate
from app.models.Course import CourseDTO
from app.routers.dependencies import get_course_service
from typing import List

router = APIRouter()


@router.post("/", response_model=CourseDTO, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, service: CourseService = Depends(get_course_service)):
    """ 
    Allows you to create a transaction for a course registration. 

    **Params**:
    - course: CourseCreate => The course with all the data to be registered.

    **Return**: The course created.
    
    """
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

@router.get("/", response_model=List[CourseDTO], status_code=status.HTTP_200_OK)
def get_courses(skip: int = 0, limit: int = 10, service: CourseService = Depends(get_course_service)):
    """ 
    This is used to get all courses. It includes pagination.
    
    **Params**:
    - skip: int => where the search starts from
    - limit: int => number of courses returned
    
    **Return**: A list of courses.
    """
    try:
        return service.get_courses(skip, limit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error Getting Courses: {e}")
