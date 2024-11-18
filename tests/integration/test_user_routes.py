import json
import pytest
from http import HTTPStatus
from tests.factories.user_factory import UserFactory

def test_get_users(client, db_session):
    """Тест получения списка пользователей."""
    # Создаем тестовых пользователей
    users = [UserFactory() for _ in range(3)]
    
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    
    data = json.loads(response.data)
    assert len(data) == 3
    assert data[0]['id'] == users[0].id

def test_get_user(client, db_session):
    """Тест получения конкретного пользователя."""
    user = UserFactory()
    
    response = client.get(f'/users/{user.id}')
    assert response.status_code == HTTPStatus.OK
    
    data = json.loads(response.data)
    assert data['id'] == user.id
    assert data['email'] == user.email

def test_create_user(client, db_session):
    """Тест создания пользователя через API."""
    user_data = {
        'username': 'newuser',
        'email': 'newuser@example.com'
    }
    
    response = client.post(
        '/users',
        data=json.dumps(user_data),
        content_type='application/json'
    )
    assert response.status_code == HTTPStatus.CREATED
    
    data = json.loads(response.data)
    assert data['username'] == user_data['username']
    assert data['email'] == user_data['email']

def test_update_user(client, db_session):
    """Тест обновления пользователя через API."""
    user = UserFactory()
    update_data = {'username': 'Updated'}
    
    response = client.put(
        f'/users/{user.id}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    assert response.status_code == HTTPStatus.OK
    
    data = json.loads(response.data)
    assert data['username'] == update_data['username']

def test_delete_user(client, db_session):
    """Тест удаления пользователя через API."""
    user = UserFactory()
    
    response = client.delete(f'/users/{user.id}')
    assert response.status_code == HTTPStatus.NO_CONTENT
    
    # Проверяем, что пользователь действительно удален
    response = client.get(f'/users/{user.id}')
    assert response.status_code == HTTPStatus.NOT_FOUND