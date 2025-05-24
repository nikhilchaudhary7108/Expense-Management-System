from flask import Blueprint, render_template, request, jsonify
from flask_cors import CORS
from app.controllers.income_controller import IncomeController

income_bp = Blueprint('income_bp', __name__, url_prefix='/incomes')
CORS(income_bp)

# Route to get all incomes for a user
@income_bp.route('/user/<int:user_id>', methods=['GET'])
def get_all_incomes(user_id):
    return IncomeController.get_all_incomes(user_id)

# Route to get a specific income by ID
@income_bp.route('/<int:income_id>', methods=['GET'])
def get_income(income_id):
    return IncomeController.get_income(income_id)

# Route to create a new income
@income_bp.route('/', methods=['POST'])
def add_income():
    return IncomeController.add_income()

# Route to update a specific income by ID
@income_bp.route('/<int:income_id>', methods=['PUT'])
def update_income(income_id):
    return IncomeController.update_income(income_id)

# Route to delete a specific income by ID
@income_bp.route('/<int:income_id>', methods=['DELETE'])
def delete_income(income_id):
    return IncomeController.delete_income(income_id)
