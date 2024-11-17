from flask import Blueprint, jsonify
from app.utils.cache_monitoring import CacheMonitor, check_cache_health
from http import HTTPStatus

bp = Blueprint('cache', __name__)

@bp.route('/cache/stats', methods=['GET'])
def get_cache_stats():
    """Получение статистики кэша."""
    stats = CacheMonitor.get_redis_stats()
    return jsonify(stats), HTTPStatus.OK

@bp.route('/cache/keys', methods=['GET'])
def get_cache_keys():
    """Получение списка всех ключей в кэше."""
    keys = CacheMonitor.get_cache_keys()
    return jsonify(keys), HTTPStatus.OK

@bp.route('/cache/keys/<key>', methods=['GET'])
def get_key_info(key):
    """Получение информации о конкретном ключе."""
    info = CacheMonitor.get_key_info(key)
    return jsonify(info), HTTPStatus.OK

@bp.route('/cache/health', methods=['GET'])
def get_cache_health():
    """Получение статуса здоровья кэша."""
    health = check_cache_health()
    status_code = HTTPStatus.OK if health['status'] == 'healthy' else HTTPStatus.WARNING
    return jsonify(health), status_code