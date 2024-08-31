from typing import List
from app.db import DatabaseManager, PostgreSQLManager
from app.models.Subject import Subject
from abc import ABC, abstractmethod
from psycopg2.extras import RealDictCursor


class SubjectDAO(ABC):
    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    @abstractmethod
    def create(self, subject: Subject) -> Subject:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 10) -> List[Subject]:
        pass

    @abstractmethod
    def get_by_id(self, subject_id: int) -> Subject:
        pass

class SubjectDAOPostgresql(SubjectDAO):
    def __init__(self, db_manager: PostgreSQLManager) -> None:
        super().__init__(db_manager)

    def create(self, subject: Subject) -> Subject:
        conn = self.db_manager.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO subject (name, career_id)
                VALUES (%s, %s)
                RETURNING id
            """, (subject.name, subject.career_id))
            subject_id = cursor.fetchone()[0]
            conn.commit()
            subject.id = subject_id
            return subject
        except Exception as e:
            conn.rollback()
            print(f"Error creating subject: {e}")
            raise
        finally:
            cursor.close()
            self.db_manager.disconnect(conn)

    def get_by_id(self, subject_id: int) -> Subject:
        conn = self.db_manager.connect()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
            SELECT * FROM subject WHERE id = %s
            """, (subject_id,))
            subject_data = cursor.fetchone()
            if subject_data:
                return Subject(**subject_data)
            return None
        except Exception as e:
            print(f"Error fetching subject with ID {subject_id}: {e}")
            raise
        finally:
            cursor.close()
            self.db_manager.disconnect(conn)
    
    def get_all(self, skip: int = 0, limit: int = 10) -> List[Subject]:
        return super().get_all(skip, limit)