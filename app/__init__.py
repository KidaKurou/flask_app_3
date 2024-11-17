from flask import Flask, jsonify
from app.extensions import db, migrate, cache
from app.config import config
import logging

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Загрузка конфигурации
    app.config.from_object(config[config_name])
    
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)

    # Регистрация blueprints
    from app.api.routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    @app.route('/')
    def hello_world():
        app.logger.info('Получен запрос к корневому маршруту')
        return 'Hello, Docker!'
    
    @app.route('/data')
    @cache.cached(timeout=60)
    def get_data():
        # Эмуляция долгого запроса
        app.logger.info('Получен запрос к маршруту /data')
        return jsonify({'data': 'This is some data!'})

    return app