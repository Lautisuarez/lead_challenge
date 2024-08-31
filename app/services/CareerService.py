from app.repository.CareerRepository import CareerRepository
from app.models.Career import Career

class CareerService:
    def __init__(self, repository: CareerRepository):
        self.repository = repository

    def register_career(self, name: str) -> Career:
        if not name:
            raise ValueError("name are required")
        
        new_career = self.repository.add_career(name)
        return new_career
