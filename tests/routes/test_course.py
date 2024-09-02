import pytest
from fastapi.testclient import TestClient
from app.routers.dependencies import get_course_service
from app.models.Course import CourseDTO
from app.models.Lead import LeadDTO
from app.models.Subject import SubjectDTO
from app.models.Career import CareerDTO
from app.main import app


class MockCourseService:
    def register_course_transaction(self, start_date, end_date, inscription_year, lead, subject):
        if not all([start_date, end_date, inscription_year, lead, subject]):
            raise ValueError("All fields are required")
        return CourseDTO(
            id="a41e265a-fe0q-1c06-f163-0c392534682b", 
            start_date=start_date, 
            end_date=end_date,
            inscription_year=inscription_year, 
            lead=lead, 
            subject=subject
        )

    def get_courses(self, skip=0, limit=10):
        data = [
            CourseDTO(
                id="b10a365a-be0c-4c04-b168-7c392534685f", 
                start_date="2024-01-01", 
                end_date="2024-06-01", 
                inscription_year="2024", 
                lead=LeadDTO(
                    id=1,
                    name="Maria",
                    last_name="Vega",
                    email="maria@mail.com",
                    address="san martin 123",
                    phone="4444444444"
                ), 
                subject=SubjectDTO(
                    id=1,
                    name="Fisica",
                    career=CareerDTO(
                        id=1,
                        name="Ingenieria quimica"
                    )
                )
            ),
            CourseDTO(
                id="c20b373a-be0d-4c04-b168-7c392534684d", 
                start_date="2024-02-01", 
                end_date="2024-07-01", 
                inscription_year="2024", 
                lead=LeadDTO(
                    id=2,
                    name="Pedro",
                    last_name="Martinez",
                    email="pedro@mail.com",
                    address="roca 123",
                    phone="6666666666"
                ), 
                subject=SubjectDTO(
                    id=2,
                    name="Matematicas",
                    career=CareerDTO(
                        id=2,
                        name="Ingenieria en sistemas"
                    )
                )
            ),
        ]
        return data[skip:limit]

    def get_course_by_id(self, course_id):
        if course_id == "01ff5082-6ebr-2c4e-bb82-g7435bcqc345":
            return None
        if course_id == "invalid-id":
            raise ValueError("Invalid course ID format")
        return CourseDTO(
            id="b10a365a-be0c-4c04-b168-7c392534685f", 
            start_date="2024-01-01", 
            end_date="2024-06-01", 
            inscription_year="2024", 
            lead=LeadDTO(
                id=1,
                name="Maria",
                last_name="Vega",
                email="maria@mail.com",
                address="san martin 123",
                phone="4444444444"
            ), 
            subject=SubjectDTO(
                id=1,
                name="Fisica",
                career=CareerDTO(
                    id=1,
                    name="Ingenieria quimica"
                )
            )
        )


@pytest.fixture
def override_dependency():
    app.dependency_overrides[get_course_service] = lambda: MockCourseService() # If you want to use the real database you must change it to the get_course_service() function
    yield
    app.dependency_overrides.clear()


class TestCourse():
    client = TestClient(app)
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    def test_create_course(self, override_dependency):
        payload = {
            "start_date": "2024-08-02",
            "end_date": "2024-09-02",
            "inscription_year": "2024",
            "lead": {
                "name": "juan",
                "last_name": "pereyra",
                "email": "test@example.com",
                "address": "av colon 123",
                "phone": "555555555"
            },
            "subject": {
                "name": "Ingles",
                "career": {
                    "name": "Arquitectura"
                }
            }
        }
        response = self.client.post("/api/v1/course/", headers=self.headers, json=payload)
        assert response.status_code == 201

    def test_create_course_missing_field(self, override_dependency):
        payload = {
            "start_date": "2024-09-02",
            "end_date": "2024-09-02",
            "inscription_year": "",
            "lead": {
                "name": "testLead",
                "last_name": "testLeadLastName",
                "email": "testLead@example.com",
                "address": "address test",
                "phone": "555555555"
            },
            "subject": {
                "name": "SubjectTest",
                "career": {
                    "name": "CareerTest"
                }
            }
        }
        response = self.client.post("/api/v1/course/", headers=self.headers, json=payload)
        assert response.status_code == 400
        assert "Value Error Creating Course" in response.json()["detail"]

    def test_get_courses(self, override_dependency):
        response = self.client.get("/api/v1/course/?skip=0&limit=1", headers=self.headers)
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_course_by_id(self, override_dependency):
        response = self.client.get("/api/v1/course/b10a365a-be0c-4c04-b168-7c392534685f", headers=self.headers)
        assert response.status_code == 200
        assert response.json()["id"] == "b10a365a-be0c-4c04-b168-7c392534685f"

    def test_get_course_by_id_not_found(self, override_dependency):
        response = self.client.get("/api/v1/course/01ff5082-6ebr-2c4e-bb82-g7435bcqc345", headers=self.headers)
        assert response.status_code == 404
        assert response.json() == {"detail": "Course with ID: 01ff5082-6ebr-2c4e-bb82-g7435bcqc345 not found"}

    def test_get_course_by_id_invalid(self, override_dependency):
        response = self.client.get("/api/v1/course/invalid-id", headers=self.headers)
        assert response.status_code == 422
        assert "Value Error" in response.json()["detail"]
