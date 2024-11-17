from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Инициализация базы данных и миграции без привязки к приложению
db = SQLAlchemy()
migrate = Migrate()