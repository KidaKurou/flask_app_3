import pytest
from fakeredis import FakeRedis
from flask import Flask
from app import create_app
from app.extensions import db, cache
from app.config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    REDIS_URL = 'redis://localhost:6379/1'
    
@pytest.fixture
def app():
    """Создание тестового приложения."""
    app = create_app(TestConfig)
    
    # Создаем контекст приложения
    with app.app_context():
        # Создаем все таблицы
        db.create_all()
        yield app
        # Очищаем БД после тестов
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Тестовый клиент Flask."""
    return app.test_client()

@pytest.fixture
def redis_mock():
    """Мок Redis для тестов."""
    fake_redis = FakeRedis()
    return fake_redis

@pytest.fixture
def auth_headers():
    """Заголовки для авторизации (если потребуются)."""
    return {'Authorization': 'Bearer test-token'}

@pytest.fixture
def db_session(app):
    """Сессия БД для тестов."""
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        
        # Привязываем сессию к транзакции
        session = db.create_scoped_session()
        db.session = session
        
        yield session
        
        # Откатываем изменения после теста
        transaction.rollback()
        connection.close()
        session.remove()