from app.repository.CourseRepository import CourseRepository
from app.models.Course import CourseDTO
from app.models.Lead import LeadDTO
from app.models.Subject import SubjectDTO
from datetime import date

class CourseService:
    def __init__(self, repository: CourseRepository):
        self.repository = repository
    
    def register_course_transaction(self, start_date: date, end_date: date, inscription_year: str, lead: LeadDTO, subject: SubjectDTO) -> CourseDTO:
        if not all([start_date, end_date, inscription_year, lead.name, lead.last_name, lead.email, subject.name, subject.career.name]):
            raise ValueError("All fields are required: start_date, end_date, inscription_year, lead.name, lead.last_name, lead.email, subject.name, subject.career.name")

        if start_date > end_date:
            raise ValueError("Start date cannot be after end date")

        try:
            course_dto = CourseDTO(
                start_date=start_date,
                end_date=end_date,
                inscription_year=inscription_year,
                lead=lead,
                subject=subject
            )
            
            return self.repository.add_course_transaction(course_dto)

        except ValueError as e:
            print(f"Validation error occurred: {e}")
            raise e
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise e
