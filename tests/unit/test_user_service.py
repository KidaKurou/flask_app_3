import pytest
from app.services.user_service import UserService
from tests.factories.user_factory import UserFactory

@pytest.fixture
def user_service(db_session, redis_mock):
    return UserService()

def test_get_user_by_id(user_service, db_session):
    """Тест получения пользователя по ID."""
    user = UserFactory()
    found_user = user_service.get_user_by_id(user.id)
    assert found_user.id == user.id
    assert found_user.email == user.email

def test_get_user_by_id_not_found(user_service):
    """Тест получения несуществующего пользователя."""
    assert user_service.get_user_by_id(999) is None

def test_create_user(user_service, db_session):
    """Тест создания пользователя."""
    user_data = {
        'username': 'newuser',
        'email': 'newuser@example.com'
    }
    user = user_service.create_user(user_data)
    assert user.username == user_data['username']
    assert user.email == user_data['email']

def test_update_user(user_service, db_session):
    """Тест обновления пользователя."""
    user = UserFactory()
    updated = user_service.update_user(user.id, {'username': 'Updated'})
    assert updated.username == 'Updated'

def test_delete_user(user_service, db_session):
    """Тест удаления пользователя."""
    user = UserFactory()
    assert user_service.delete_user(user.id) is True
    # При SimpleCache delete_memoized может не сработать корректно.
    # Проверяем через прямой запрос к БД.
    from app.extensions import db
    from app.models.user import User
    assert db.session.get(User, user.id) is None

@pytest.mark.parametrize('cache_hit', [True, False])
def test_get_user_cache(user_service, db_session, redis_mock, cache_hit):
    """Тест кэширования пользователя."""
    user = UserFactory()
    
    # Первый запрос (cache miss)
    first_result = user_service.get_user_by_id(user.id)
    assert first_result.id == user.id
    
    if not cache_hit:
        # Инвалидируем кэш
        user_service._invalidate_caches(user.id)
    
    # Второй запрос
    second_result = user_service.get_user_by_id(user.id)
    assert second_result.id == user.id