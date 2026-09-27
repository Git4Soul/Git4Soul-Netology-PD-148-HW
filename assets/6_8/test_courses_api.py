import pytest
from django.urls import reverse
from rest_framework import status

from students.models import Course


@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    """Проверка получения одного курса (retrieve)."""
    course = course_factory()
    url = reverse('courses-detail', args=[course.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == course.id
    assert response.data['name'] == course.name


@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    """Проверка получения списка курсов (list)."""
    courses = course_factory(_quantity=3)
    url = reverse('courses-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == len(courses)
    returned_ids = {item['id'] for item in response.data}
    expected_ids = {course.id for course in courses}
    assert returned_ids == expected_ids


@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    """Проверка фильтрации списка курсов по id."""
    courses = course_factory(_quantity=5)
    target_course = courses[0]
    url = reverse('courses-list')
    response = api_client.get(url, data={'id': target_course.id})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['id'] == target_course.id


@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    """Проверка фильтрации списка курсов по name."""
    course_factory(name='Python')
    course_factory(name='Django')
    course_factory(name='JavaScript')
    url = reverse('courses-list')
    response = api_client.get(url, data={'name': 'Django'})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Django'


@pytest.mark.django_db
def test_create_course(api_client):
    """Тест успешного создания курса."""
    data = {
        'name': 'Новый курс',
    }
    url = reverse('courses-list')
    response = api_client.post(url, data=data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Course.objects.filter(name='Новый курс').exists()


@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    """Тест успешного обновления курса."""
    course = course_factory()
    data = {
        'name': 'Обновлённое имя',
    }
    url = reverse('courses-detail', args=[course.id])
    response = api_client.put(url, data=data, format='json')
    assert response.status_code == status.HTTP_200_OK
    course.refresh_from_db()
    assert course.name == 'Обновлённое имя'


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    """Тест успешного удаления курса."""
    course = course_factory()
    url = reverse('courses-detail', args=[course.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Course.objects.filter(id=course.id).exists()