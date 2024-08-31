from app.dao.CourseDAO import CourseDAO
from app.models.Course import Course
from datetime import date

class CourseRepository:
    def __init__(self, dao: CourseDAO):
        self.dao = dao

    def get_course(self, course_id: str) -> Course:
        return self.dao.get_course_by_id(course_id)

    def add_course(self, start_date: date, end_date: date, inscription_year: str, lead_id: int, subject_id: int) -> Course:
        return self.dao.create(Course(
            start_date=start_date,
            end_date=end_date,
            inscription_year=inscription_year,
            lead_id=lead_id,
            subject_id=subject_id
        ))
