import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@db:5432/flask_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'

    # REDIS_URL = 'redis://redis:6379/0'
    # Настройки кэширования
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = f'redis://{CACHE_REDIS_HOST}:{CACHE_REDIS_PORT}/{CACHE_REDIS_DB}'
    CACHE_DEFAULT_TIMEOUT = 300

    # Настройки логирования
    LOGGING_CONFIG = {
        'version': 1,
        'formatters': {
            'detailed': {
                'format': '%(asctime)s %(levelname)s [%(name)s] %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'detailed',
                'level': 'INFO'
            },
            'file': {
                'class': 'logging.FileHandler',
                'filename': 'cache.log',
                'formatter': 'detailed',
                'level': 'INFO'
            }
        },
        'loggers': {
            'cache_monitoring': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False
            }
        }
    }

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}