from app.extensions import db
from app.models.user import User

# Сервис для работы с пользователями
class UserService:
    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get_or_404(user_id)

    @staticmethod
    def create_user(username, email):
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update_user(user_id, username, email):
        user = User.query.get_or_404(user_id)
        user.username = username
        user.email = email
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()