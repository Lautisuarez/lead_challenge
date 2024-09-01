from typing import List
from app.models.Subject import Subject
from abc import ABC, abstractmethod
from psycopg2.extras import RealDictCursor


class SubjectDAO(ABC):
    @abstractmethod
    def create(self, connection, subject: Subject) -> Subject:
        pass

    @abstractmethod
    def get_by_name(self, connection, name: str) -> Subject:
        pass

class SubjectDAOPostgresql(SubjectDAO):
    def create(self, connection, subject: Subject) -> Subject:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO subject (name, career_id)
            VALUES (%s, %s)
            RETURNING id
        """, (subject.name, subject.career_id))
        subject_id = cursor.fetchone()[0]
        subject.id = subject_id
        cursor.close()
        return subject

    def get_by_name(self, connection, name: str) -> Subject:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
        SELECT * FROM subject WHERE name = %s
        """, (name,))
        subject_data = cursor.fetchone()
        cursor.close()
        if subject_data:
            return Subject(**subject_data)
        return None
        