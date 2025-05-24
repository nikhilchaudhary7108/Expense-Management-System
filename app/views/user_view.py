# views/user_view.py
from flask import jsonify

class UserView:
    @staticmethod
    def render_user(user):
        return {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "created_at": str(user.created_at)
        }

    @staticmethod
    def render_users(users):
        return [UserView.render_user(user) for user in users]

    @staticmethod
    def render_success(message, user_id=None):
        response = {"message": message}
        if user_id:
            response["user_id"] = user_id
        return response

    @staticmethod
    def render_error(message):
        return {"error": message}
