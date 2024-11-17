from flask import Blueprint, jsonify, request
from app.services.user_service import UserService
from app.extensions import cache

# Маршруты для работы с пользователями
user_bp = Blueprint('user', __name__)
user_service = UserService()

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = user_service.get_all_users()
    return jsonify([user.to_dict() for user in users]), 200

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    user = user_service.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        user = user_service.create_user(data)
        return jsonify(user.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id: int):
    data = request.get_json()
    user = user_service.update_user(user_id, data)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int):
    if user_service.delete_user(user_id):
        return jsonify({'message': 'User deleted'}), 200
    return jsonify({'message': 'User not found'}), 404

@user_bp.route('/users/cache/clear', methods=['POST'])
def clear_cache():
    # Ручная очистка кэша (для тестирования)
    cache.clear()
    return jsonify({'message': 'Cache cleared'}), 200

@user_bp.route('/users/cache/clear/<int:user_id>', methods=['POST'])
def clear_user_cache(user_id: int):
    # Ручная очистка кэша конкретного пользователя (для тестирования)
    user_service._invalidate_caches(user_id)
    return jsonify({'message': 'User cache cleared'}), 200