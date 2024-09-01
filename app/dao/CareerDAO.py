from app.models.Career import Career
from abc import ABC, abstractmethod
from psycopg2.extras import RealDictCursor


class CareerDAO(ABC):
    @abstractmethod
    def get_career_by_id(self, connection, career_id: int) -> Career:
        pass

    @abstractmethod
    def get_career_by_name(self, connection, name: str) -> Career:
        pass

    @abstractmethod
    def create(self, connection, career: Career) -> Career:
        pass


class CareerDAOPostgresql(CareerDAO):
    def create(self, connection, career: Career) -> Career:
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO career (name)
        VALUES (%s)
        RETURNING id
        """, (career.name,))
        career_id = cursor.fetchone()[0]
        career.id = career_id
        cursor.close()
        return career
    
    def get_career_by_name(self, connection, name: str) -> Career:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
        SELECT * FROM career WHERE name = %s
        """, (name,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return Career(**row)
        return None

    def get_career_by_id(self, connection, career_id: int) -> Career:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
        SELECT * FROM career WHERE id = %s
        """, (career_id,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return Career(**row)
        return None
