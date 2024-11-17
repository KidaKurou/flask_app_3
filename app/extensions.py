from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache

# Инициализация базы данных и миграции без привязки к приложению
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
