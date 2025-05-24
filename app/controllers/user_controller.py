# controllers/user_controller.py
from flask import request, jsonify
from app.services.user_service import UserService
from app.views.user_view import UserView

class UserController:
    @staticmethod
    def get_user(user_id):
        user = UserService.get_user_by_id(user_id)
        if user:
            return jsonify(UserView.render_success('User fetched successfully', UserView.render_user(user))), 200
        return jsonify(UserView.render_error('User not found')), 404

    @staticmethod
    def get_all_users():
        users = UserService.get_all_users()
        return jsonify(UserView.render_success('Users fetched successfully', UserView.render_users(users))), 200

    @staticmethod
    def add_user():
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')  # In real applications, hash passwords
        role = data.get('role', 'user')

        user = UserService.add_user(username, email, password, role)
        return jsonify(UserView.render_success('User added successfully', {'user_id': user.user_id})), 201

    @staticmethod
    def update_user(user_id):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        user = UserService.update_user(user_id, username, email, password, role)
        if user:
            return jsonify(UserView.render_success('User updated successfully', {'user_id': user.user_id})), 200
        return jsonify(UserView.render_error('User not found')), 404

    @staticmethod
    def delete_user(user_id):
        user = UserService.delete_user(user_id)
        if user:
            return jsonify(UserView.render_success('User deleted successfully', {'user_id': user.user_id})), 200
        return jsonify(UserView.render_error('User not found')), 404
    
    @staticmethod
    def login():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = UserService.get_user_by_email(email)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return jsonify({'error': 'Invalid password'}), 401

        payload = {
            'user_id': user.user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'message': 'Login successful', 'token': token}), 200
