from app.db import DatabaseManager, PostgreSQLManager
from app.models.Course import Course
from abc import ABC, abstractmethod
from psycopg2.extras import RealDictCursor


class CourseDAO(ABC):
    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    @abstractmethod
    def get_course_by_id(self, course_id: str) -> Course:
        pass

    @abstractmethod
    def create(self, course: Course) -> Course:
        pass

class CourseDAOPostgresql(CourseDAO):
    def __init__(self, db_manager: PostgreSQLManager) -> None:
        super().__init__(db_manager)

    def get_course_by_id(self, course_id: str) -> Course:
        conn = self.db_manager.connect()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT * FROM course WHERE id = %s
            """, (course_id,))
            row = cursor.fetchone()
            if row:
                return Course(**row)
            return None
        except Exception as e:
            conn.rollback()
            print(f"Error getting course by ID: {e}")
            raise
        finally:
            cursor.close()
            self.db_manager.disconnect(conn)

    def create(self, course: Course) -> Course:
        conn = self.db_manager.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
            INSERT INTO course (start_date, end_date, inscription_year, lead_id, subject_id)
            VALUES (%s, %s, %s, %s, %s)
            """, (course.start_date, course.end_date, course.inscription_year,
                  course.lead_id, course.subject_id))
            conn.commit()
            return course
        except Exception as e:
            conn.rollback()
            print(f"Error creating course: {e}")
            raise
        finally:
            cursor.close()
            self.db_manager.disconnect(conn)