from app.repository.SubjectRepository import SubjectRepository
from app.models.Subject import Subject
from typing import List

class SubjectService:
    def __init__(self, repository: SubjectRepository):
        self.repository = repository

    def register_subject(self, name: str, career_id: int) -> Subject:
        if not name or not career_id:
            raise ValueError("Something fields are required")
        
        return self.repository.add_subject(name, career_id)
    
    def get_all_subject(self, skip: int = 0, limit: int = 10) -> List[Subject]:
        return self.repository.get_subjects(skip, limit)
    
    def get_lead_by_id(self, subject_id: int) -> Subject:
        if not subject_id:
            raise ValueError("subject_id field is required")

        return self.repository.get_subject(subject_id)
