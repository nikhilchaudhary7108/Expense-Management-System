from flask import Blueprint, render_template, request, jsonify
from flask_cors import CORS
from app.controllers.expense_controller import ExpenseController

expense_bp = Blueprint('expense_bp', __name__, url_prefix='/expenses')
CORS(expense_bp)

# Route to add a new expense
@expense_bp.route('/', methods=['POST'])
def add_expense():
    return ExpenseController.add_expense()

# Route to get a specific expense by ID
@expense_bp.route('/<int:expense_id>', methods=['GET'])
def get_expense(expense_id):
    return ExpenseController.get_expense(expense_id)

# Route to get all expenses for a user
@expense_bp.route('/', methods=['GET'])
def get_all_expenses():
    return ExpenseController.get_all_expenses()

# Route to update a specific expense by ID
@expense_bp.route('/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    return ExpenseController.update_expense(expense_id)

# Route to delete a specific expense by ID
@expense_bp.route('/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    return ExpenseController.delete_expense(expense_id)
