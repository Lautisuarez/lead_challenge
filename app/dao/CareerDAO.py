from app.db import DatabaseManager, PostgreSQLManager
from app.models.Career import Career
from abc import ABC, abstractmethod
from psycopg2.extras import RealDictCursor


class CareerDAO(ABC):
    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    @abstractmethod
    def get_career_by_id(self, career_id: int) -> Career:
        pass

    @abstractmethod
    def create(self, career: Career):
        pass


class CareerDAOPostgresql(CareerDAO):
    def __init__(self, db_manager: PostgreSQLManager) -> None:
        super().__init__(db_manager)

    def create(self, career: Career):
        conn = self.db_manager.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
            INSERT INTO career (name)
            VALUES (%s)
            """, (career.name,))
            conn.commit()
            return career
        except Exception as e:
            conn.rollback()
            print(f"Error creating career: {e}")
            raise
        finally:
            cursor.close()
            self.db_manager.disconnect(conn)

    def get_career_by_id(self, career_id: int) -> Career:
        conn = self.db_manager.connect()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
            SELECT * FROM career WHERE id = %s
            """, (career_id,))
            row = cursor.fetchone()
            if row:
                return Career(**row)
        except Exception as e:
            conn.rollback()
            print(f"Error creating career: {e}")
            raise
        finally:
            cursor.close()
            self.db_manager.disconnect(conn)
