import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from myapp.models import Task, User
from django.utils import timezone
from rest_framework import status


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpass')


@pytest.fixture
def task(user):
    return Task.objects.create(
        title='Test Task',
        description='Test description',
        status='pending',
        user=user,
        due_date=timezone.now() + timezone.timedelta(days=1)
    )


@pytest.mark.django_db
def test_create_task(api_client, user):
    api_client.force_authenticate(user=user)

    url = reverse('task-list')
    data = {
        'title': 'New Task',
        'description': 'Test task description',
        'status': 'pending',
        'user': "1",
        'due_date': (timezone.now() + timezone.timedelta(days=1)).isoformat(),
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert Task.objects.count() == 1
    assert Task.objects.get().title == 'New Task'


@pytest.mark.django_db
def test_list_tasks(api_client, user, task):
    api_client.force_authenticate(user=user)

    url = reverse('task-list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['title'] == 'Test Task'


@pytest.mark.django_db
def test_update_task(api_client, user, task):
    api_client.force_authenticate(user=user)

    url = reverse('task-detail', args=[task.id])
    data = {
        'title': 'Updated Task',
        'description': 'Updated description',
        'status': 'in_progress',
        'user': user.id,
        'due_date': task.due_date.isoformat(),
    }
    response = api_client.put(url, data, format='json')
    print(response.data)

    assert response.status_code == status.HTTP_200_OK
    task.refresh_from_db()
    assert task.title == 'Updated Task'
    assert task.status == 'in_progress'


@pytest.mark.django_db
def test_delete_task(api_client, user, task):
    api_client.force_authenticate(user=user)

    url = reverse('task-detail', args=[task.id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Task.objects.count() == 0


@pytest.mark.django_db
def test_filter_tasks_by_status(api_client, user, task):
    api_client.force_authenticate(user=user)

    Task.objects.create(
        title='Completed Task',
        description='Another description',
        status='completed',
        user=user,
        due_date=timezone.now() - timezone.timedelta(days=1)
    )

    url = reverse('task-list') + '?status=pending'
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['title'] == 'Test Task'
