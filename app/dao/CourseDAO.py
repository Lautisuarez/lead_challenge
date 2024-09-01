from app.models.Course import Course
from abc import ABC, abstractmethod
from psycopg2.extras import RealDictCursor
from typing import List


class CourseDAO(ABC):
    @abstractmethod
    def get_course_by_id(self, connection, course_id: str) -> Course:
        pass

    @abstractmethod
    def get_courses(self, connection, skip: int = 0, limit: int = 10) -> List[Course]:
        pass

    @abstractmethod
    def create(self, connection, course: Course) -> Course:
        pass

class CourseDAOPostgresql(CourseDAO):
    def get_course_by_id(self, connection, course_id: str) -> Course:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT * FROM course WHERE id = %s
        """, (course_id,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return Course(**row)
        return None
    
    def get_courses(self, connection, skip: int = 0, limit: int = 10) -> List[Course]:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM course OFFSET %s LIMIT %s", (skip, limit,))
        courses = cursor.fetchall()
        cursor.close()
        if courses:
            return [Course(**course) for course in courses]
        return None

    def create(self, connection, course: Course) -> Course:
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO course (start_date, end_date, inscription_year, lead_id, subject_id)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        """, (course.start_date, course.end_date, course.inscription_year,
                course.lead_id, course.subject_id))
        course.id = cursor.fetchone()[0]
        cursor.close()
        return course