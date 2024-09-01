import psycopg2
from app.db import DatabaseManager
from app.dao.CourseDAO import CourseDAO
from app.dao.LeadDAO import LeadDAO
from app.dao.SubjectDAO import SubjectDAO
from app.dao.CareerDAO import CareerDAO
from app.models.Course import Course, CourseDTO
from app.models.Lead import Lead, LeadDTO
from app.models.Subject import Subject, SubjectDTO
from app.models.Career import Career, CareerDTO

class CourseRepository:
    def __init__(self, db_manager: DatabaseManager, dao_course: CourseDAO, dao_lead: LeadDAO, dao_subject: SubjectDAO, dao_career: CareerDAO):
        self.db_manager = db_manager
        self.dao_course = dao_course
        self.dao_lead = dao_lead
        self.dao_subject = dao_subject
        self.dao_career = dao_career

    def _check_career(self, connection, career_name: str) -> Career:
        """ Checks that the career doesnt exist in the DB, if it does, it returns it """
        career = self.dao_career.get_career_by_name(connection, career_name)
        if not career:
            return self.dao_career.create(connection, Career(name=career_name))
        return career

    def _check_subject(self, connection, subject_name: str, career_id: int) -> Subject:
        """ Checks that the subject doesnt exist in the DB, if it does, it returns it """
        subject = self.dao_subject.get_by_name(connection, subject_name)
        if not subject:
            return self.dao_subject.create(connection, Subject(name=subject_name, career_id=career_id))
        return subject

    def _check_lead(self, connection, lead_dto: LeadDTO) -> Lead:
        """ Checks that the lead doesnt exist in the DB, if it does, it returns it """
        lead = self.dao_lead.get_lead_by_name(connection, lead_dto.name)
        if not lead:
            return self.dao_lead.create(connection, Lead(
                name=lead_dto.name,
                last_name=lead_dto.last_name,
                email=lead_dto.email,
                address=lead_dto.address,
                phone=lead_dto.phone
            ))
        return lead

    def add_course_transaction(self, course: CourseDTO) -> CourseDTO:
        connection = self.db_manager.connect()
        connection.autocommit = False
        try:
            with connection:
                new_career = self._check_career(connection, course.subject.career.name)
                new_subject = self._check_subject(connection, course.subject.name, new_career.id)
                new_lead = self._check_lead(connection, course.lead)
                new_course = self.dao_course.create(connection, Course(
                    start_date=course.start_date,
                    end_date=course.end_date,
                    inscription_year=course.inscription_year,
                    lead_id=new_lead.id,
                    subject_id=new_subject.id
                ))

                return CourseDTO(
                    id=new_course.id,
                    start_date=new_course.start_date,
                    end_date=new_course.end_date,
                    inscription_year=new_course.inscription_year,
                    lead=LeadDTO(
                        id=new_lead.id,
                        name=new_lead.name,
                        last_name=new_lead.last_name,
                        email=new_lead.email,
                        address=new_lead.address,
                        phone=new_lead.phone
                    ),
                    subject=SubjectDTO(
                        id=new_subject.id,
                        name=new_subject.name,
                        career=CareerDTO(
                            id=new_career.id,
                            name=new_career.name
                        )
                    )
                )
        except (psycopg2.DatabaseError, psycopg2.IntegrityError) as db_error:
            connection.rollback()
            print(f"Database error occurred: {db_error}")
            raise db_error
        except Exception as e:
            connection.rollback()
            print(f"An unexpected error occurred: {e}")
            raise e
        finally:
            self.db_manager.disconnect(connection)