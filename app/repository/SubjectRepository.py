from app.dao.SubjectDAO import SubjectDAO
from app.models.Subject import Subject
from typing import List

class SubjectRepository:
    def __init__(self, dao: SubjectDAO):
        self.dao = dao

    def get_subjects(self, skip: int = 0, limit: int = 10) -> List[Subject]:
        return self.dao.get_all(skip, limit)

    def get_subject(self, subject_id: int) -> Subject:
        return self.dao.get_by_id(subject_id)

    def add_subject(self, name: str, career_id: int) -> Subject:
        return self.dao.create(Subject(
            name=name,
            career_id=career_id
        ))