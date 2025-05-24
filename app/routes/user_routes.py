# routes/routes.py
from flask import Blueprint, render_template, request, jsonify
from flask_cors import CORS
from app.controllers.user_controller import UserController

user_bp = Blueprint('user_bp', __name__, url_prefix='/users')
CORS(user_bp)

@user_bp.route('/login', methods=['POST'])
def login_user():
    return UserController.login()

# Route to get all users
@user_bp.route('/', methods=['GET'])
def get_all_users():
    return UserController.get_all_users()

# Route to get a specific user by ID
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return UserController.get_user(user_id)

# Route to create a new user
@user_bp.route('/', methods=['POST'])
def add_user():
    return UserController.add_user()

# Route to update a specific user by ID
@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    return UserController.update_user(user_id)

# Route to delete a specific user by ID
@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return UserController.delete_user(user_id)
