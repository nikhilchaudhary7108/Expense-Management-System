from flask import Blueprint, request, jsonify
from app.models.user_model import User
from app.shared.utils.db_utils import db
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = data.get('user_id')
    password = data.get('password')

    user = User.query.filter_by(user_id=user_id).first()

    if not user or check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    return jsonify({
        'message': 'Login successful',
        'user_id': user.user_id,
        'name': user.name
        # add other fields as needed
    })
