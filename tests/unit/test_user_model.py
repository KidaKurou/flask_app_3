import pytest
from app.models.user import User
from tests.factories.user_factory import UserFactory

def test_user_creation(db_session):
    """Тест создания пользователя."""
    user = UserFactory()
    assert user.id is not None
    assert '@' in user.email
    
def test_user_representation(db_session):
    """Тест строкового представления пользователя."""
    user = UserFactory(username='testuser')
    assert str(user) == 'testuser'
    
def test_user_to_dict(db_session):
    """Тест метода to_dict."""
    user = UserFactory()
    user_dict = user.to_dict()
    assert user_dict['id'] == user.id
    assert user_dict['email'] == user.email
    
@pytest.mark.parametrize('email', [
    'invalid_email',
    '@example.com',
    'user@',
    'user@.com'
])
def test_invalid_email(db_session, email):
    """Тест валидации email."""
    with pytest.raises(ValueError):
        UserFactory(email=email)