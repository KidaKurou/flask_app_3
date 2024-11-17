from app.extensions import db, cache
from app.models.user import User
from typing import Optional, List
from app.utils.cache_monitoring import CacheMonitor, cache_logger

# Сервис для работы с пользователями
class UserService:
    # @CacheMonitor.monitor_cache_operation('read')
    @cache.cached(timeout=300, key_prefix='all_users')
    def get_all_users(self) -> List[User]:
        return User.query.all()

    # @CacheMonitor.monitor_cache_operation('read')
    @cache.memoize(timeout=300)
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return User.query.get_or_404(user_id)

    def create_user(self, data: dict) -> User:
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        # Инвалидируем кэш после создания нового пользователя
        self._invalidate_caches()
        return user

    def update_user(self, user_id: int, data: dict) -> Optional[User]:
        user = self.get_user_by_id(user_id)
        if user:
            for key, value in data.items():
                setattr(user, key, value)
            db.session.commit()
            # Инвалидируем кэш после обновления пользователя
            self._invalidate_caches(user_id)
            return user
        return None

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            # Инвалидируем кэш после удаления пользователя
            self._invalidate_caches(user_id)
            return True
        return False
    
    # Удаляем кэш для всех пользователей и конкретного пользователя
    def _invalidate_caches(self, user_id: Optional[int] = None):
        cache.delete_memoized(self.get_all_users)
        if user_id:
            cache.delete_memoized(self.get_user_by_id)