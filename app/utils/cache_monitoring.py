import logging
import time
from functools import wraps
from flask import current_app
from app.extensions import cache
from typing import Dict, Any, Optional

# Настраиваем специальный логгер для кэша
cache_logger = logging.getLogger('cache_monitoring')
cache_logger.setLevel(logging.INFO)

class CacheMonitor:
    @staticmethod
    def get_redis_stats() -> Dict[str, Any]:
        """Получение статистики Redis."""
        try:
            redis_client = cache.get_redis_connection()
            info = redis_client.info()
            
            return {
                'used_memory_human': info['used_memory_human'],
                'connected_clients': info['connected_clients'],
                'uptime_in_seconds': info['uptime_in_seconds'],
                'hits': info['keyspace_hits'],
                'misses': info['keyspace_misses'],
                'hit_ratio': info['keyspace_hits'] / (info['keyspace_hits'] + info['keyspace_misses'] + 0.000001) * 100,
                'total_connections_received': info['total_connections_received'],
                'total_commands_processed': info['total_commands_processed']
            }
        except Exception as e:
            cache_logger.error(f"Error getting Redis stats: {str(e)}")
            return {}

    @staticmethod
    def get_cache_keys(pattern: str = '*') -> list:
        """Получение списка всех ключей в кэше по паттерну."""
        try:
            redis_client = cache.get_redis_connection()
            return [key.decode() for key in redis_client.keys(pattern)]
        except Exception as e:
            cache_logger.error(f"Error getting cache keys: {str(e)}")
            return []

    @staticmethod
    def get_key_info(key: str) -> Dict[str, Any]:
        """Получение информации о конкретном ключе."""
        try:
            redis_client = cache.get_redis_connection()
            ttl = redis_client.ttl(key)
            key_type = redis_client.type(key).decode()
            size = redis_client.memory_usage(key)
            
            return {
                'type': key_type,
                'ttl': ttl,
                'memory_usage': size
            }
        except Exception as e:
            cache_logger.error(f"Error getting key info: {str(e)}")
            return {}

    @staticmethod
    def monitor_cache_operation(operation: str):
        """Декоратор для мониторинга операций с кэшем."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    
                    # Логируем успешную операцию
                    cache_logger.info(
                        f"Cache {operation} - Function: {func.__name__} "
                        f"Args: {args} KwArgs: {kwargs} "
                        f"Execution time: {execution_time:.4f}s"
                    )
                    return result
                except Exception as e:
                    # Логируем ошибку
                    cache_logger.error(
                        f"Cache {operation} error - Function: {func.__name__} "
                        f"Args: {args} KwArgs: {kwargs} "
                        f"Error: {str(e)}"
                    )
                    raise
            return wrapper
        return decorator

# Создаем функцию для периодической проверки состояния кэша
def check_cache_health() -> Dict[str, Any]:
    """Проверка здоровья кэша."""
    stats = CacheMonitor.get_redis_stats()
    
    health_status = {
        'status': 'healthy',
        'issues': []
    }

    # Проверяем различные метрики
    if stats:
        # Проверяем hit ratio
        if stats.get('hit_ratio', 0) < 50:
            health_status['issues'].append('Low cache hit ratio')
        
        # Проверяем использование памяти
        memory_used = stats.get('used_memory_human', '0B')
        if memory_used.endswith('G'):  # если больше 1GB
            health_status['issues'].append('High memory usage')
            
        # Проверяем количество подключений
        if stats.get('connected_clients', 0) > 1000:
            health_status['issues'].append('High number of connections')

    if health_status['issues']:
        health_status['status'] = 'warning'
        
    return health_status