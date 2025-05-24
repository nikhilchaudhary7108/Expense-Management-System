# services/user_service.py
from app.models.user_model import User
from app.shared.utils.db_utils import db

class UserService:
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def add_user(username, email, password, role='user'):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def update_user(user_id, username=None, email=None, password=None, role=None):
        user = User.query.get(user_id)
        if not user:
            return None
        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.password = password
        if role:
            user.role = role
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
        return user

    @staticmethod
    def is_admin(user_id):
        user = User.query.get(user_id)
        return user and user.role == 'admin'

    @staticmethod
    def is_user(user_id):
        user = User.query.get(user_id)
        return user and user.role == 'user'
    
    @staticmethod
    def get_user_by_email(email):
         return User.query.filter_by(email=email).first()

