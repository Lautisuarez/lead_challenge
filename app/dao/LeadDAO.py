from typing import List
from app.db import DatabaseManager, PostgreSQLManager
from app.models.Lead import Lead
from abc import ABC, abstractmethod
from psycopg2.extras import RealDictCursor


class LeadDAO(ABC):
    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db_manager = db_manager

    @abstractmethod
    def create(self, lead: Lead) -> Lead:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 10) -> List[Lead]:
        pass

    @abstractmethod
    def get_lead_by_id(self, lead_id: int) -> Lead:
        pass


class LeadDAOPostgresql(LeadDAO):
    def __init__(self, db_manager: PostgreSQLManager) -> None:
        super().__init__(db_manager)

    def create(self, lead: Lead) -> Lead:
        conn = self.db_manager.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO lead (name, last_name, email, address, phone)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (lead.name, lead.last_name, lead.email, lead.address, lead.phone))
            lead_id = cursor.fetchone()[0]
            conn.commit()
            lead.id = lead_id
            return lead
        except Exception as e:
            conn.rollback()
            print(f"Error creating lead: {e}")
            raise
        finally:
            cursor.close()
            self.db_manager.disconnect(conn)

    def get_all(self, skip: int = 0, limit: int = 10) -> List[Lead]:
        conn = self.db_manager.connect()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("SELECT * FROM lead OFFSET %s LIMIT %s", (skip, limit,))
            leads_data = cursor.fetchall()
            if leads_data:
                return [Lead(**lead) for lead in leads_data]
            return None
        except Exception as e:
            print(f"Error fetching leads: {e}")
            raise
        finally:
            cursor.close()
            self.db_manager.disconnect(conn)

    def get_lead_by_id(self, lead_id: int) -> Lead:
        conn = self.db_manager.connect()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
            SELECT * FROM lead WHERE id = %s
            """, (lead_id,))
            lead_data = cursor.fetchone()
            if lead_data:
                return Lead(**lead_data)
            return None
        except Exception as e:
            print(f"Error fetching lead: {e}")
            raise
        finally:
            cursor.close()
            self.db_manager.disconnect(conn)