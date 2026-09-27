import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture
def api_client():
    """Фикстура для тестового клиента DRF."""
    return APIClient()


@pytest.fixture
def course_factory():
    """Фикстура-фабрика для создания курсов через model_bakery."""
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    """Фикстура-фабрика для создания студентов через model_bakery."""
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory