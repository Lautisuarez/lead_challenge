from app.utils.config import settings
from app.dao import CourseDAO, CareerDAO, LeadDAO, SubjectDAO
from app.repository.CourseRepository import CourseRepository
from app.services.CourseService import CourseService


def get_course_service() -> CourseService:
    dao_course = CourseDAO.CourseDAOPostgresql()
    dao_lead = LeadDAO.LeadDAOPostgresql()
    dao_subject = SubjectDAO.SubjectDAOPostgresql()
    dao_career = CareerDAO.CareerDAOPostgresql()
    repository = CourseRepository(settings.db_manager, dao_course, dao_lead, dao_subject, dao_career)
    return CourseService(repository)