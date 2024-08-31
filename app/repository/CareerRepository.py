from app.dao.CareerDAO import CareerDAO
from app.models.Career import Career

class CareerRepository:
    def __init__(self, dao: CareerDAO):
        self.dao = dao

    def get_career(self, career_id: int) -> Career:
        career = self.dao.get_career_by_id(career_id)
        if career:
            return Career(
                id=career.id,
                name=career.name
            )
        return None

    def add_career(self, name: str) -> Career:
        career = Career(name=name)
        return self.dao.create(career)