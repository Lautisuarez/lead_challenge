from app.repository.CourseRepository import CourseRepository
from app.models.Course import Course
from datetime import date

class CourseService:
    def __init__(self, repository: CourseRepository):
        self.repository = repository

    def register_course(self, start_date: date, end_date: date, inscription_year: str, lead_id: int, subject_id: int) -> Course:
        if not start_date or not end_date or not inscription_year or not lead_id or not subject_id:
            raise ValueError("Something fields are required")
        
        return self.repository.add_course(start_date, end_date, inscription_year, lead_id, subject_id)
    
    def get_course_by_id(self, course_id: str) -> Course:
        if not course_id:
            raise ValueError("course_id field is required")

        return self.repository.get_course(course_id)
