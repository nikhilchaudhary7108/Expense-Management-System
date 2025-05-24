from flask import Blueprint, render_template, request, jsonify
from flask_cors import CORS
from app.controllers.budget_controller import BudgetController

budget_bp = Blueprint('budget_bp', __name__, url_prefix='/budgets')
CORS(budget_bp)

# Route to add a new budget (Admin only)
@budget_bp.route('/', methods=['POST'])
def add_budget():
    return BudgetController.add_budget()

# Route to get a specific budget by ID
@budget_bp.route('/<int:budget_id>', methods=['GET'])
def get_budget(budget_id):
    return BudgetController.get_budget(budget_id)

# Route to get all budgets for a specific user
@budget_bp.route('/user/<int:user_id>', methods=['GET'])
def get_all_budgets(user_id):
    return BudgetController.get_all_budgets(user_id)

# Route to update a specific budget (Admin only)
@budget_bp.route('/<int:budget_id>', methods=['PUT'])
def update_budget(budget_id):
    return BudgetController.update_budget(budget_id)

# Route to delete a specific budget (Admin only)
@budget_bp.route('/<int:budget_id>', methods=['DELETE'])
def delete_budget(budget_id):
    return BudgetController.delete_budget(budget_id)
