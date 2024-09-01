from typing import List
from app.models.Lead import Lead
from abc import ABC, abstractmethod
from psycopg2.extras import RealDictCursor


class LeadDAO(ABC):
    @abstractmethod
    def create(self, connection, lead: Lead) -> Lead:
        pass

    @abstractmethod
    def get_lead_by_name(self, connection, name: str) -> Lead:
        pass

    @abstractmethod
    def get_lead_by_id(self, connection, lead_id:int) -> Lead:
        pass


class LeadDAOPostgresql(LeadDAO):
    def create(self, connection, lead: Lead) -> Lead:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO lead (name, last_name, email, address, phone)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (lead.name, lead.last_name, lead.email, lead.address, lead.phone))
        lead_id = cursor.fetchone()[0]
        lead.id = lead_id
        cursor.close()
        return lead

    def get_lead_by_name(self, connection, name: str) -> Lead:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
        SELECT * FROM lead WHERE name = %s
        """, (name,))
        lead_data = cursor.fetchone()
        cursor.close()
        if lead_data:
            return Lead(**lead_data)
        return None
    
    def get_lead_by_id(self, connection, lead_id: int) -> Lead:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
        SELECT * FROM lead WHERE id = %s
        """, (lead_id,))
        lead_data = cursor.fetchone()
        cursor.close()
        if lead_data:
            return Lead(**lead_data)
        return None