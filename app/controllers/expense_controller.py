# controllers/expense_controller.py
from flask import request, jsonify
from app.services.expense_service import ExpenseService
from app.services.user_service import UserService
from app.views.expense_view import ExpenseView

class ExpenseController:
    @staticmethod
    def add_expense():
        data = request.get_json()
        user_id = data.get('user_id')

        if not UserService.is_valid_user(user_id):
            return jsonify(ExpenseView.render_error('Invalid user')), 400

        amount = data.get('amount')
        category_id = data.get('category_id')
        date = data.get('date')
        description = data.get('description')

        expense = ExpenseService.add_expense(user_id, amount, category_id, date, description)
        return jsonify(ExpenseView.render_success('Expense added successfully', expense.expense_id)), 201

    @staticmethod
    def get_expense(expense_id):
        requesting_user_id = request.args.get('user_id', type=int)

        expense = ExpenseService.get_expense_by_id(expense_id, requesting_user_id)
        if not expense:
            return jsonify(ExpenseView.render_error('Expense not found or access denied')), 404

        return jsonify(ExpenseView.render_expense(expense)), 200

    @staticmethod
    def get_all_expenses():
        user_id = request.args.get('user_id', type=int)

        if not UserService.is_valid_user(user_id):
            return jsonify(ExpenseView.render_error('Invalid user')), 400

        expenses = ExpenseService.get_all_expenses(user_id)
        return jsonify(ExpenseView.render_expenses(expenses)), 200

    @staticmethod
    def update_expense(expense_id):
        data = request.get_json()
        user_id = data.get('user_id')

        amount = data.get('amount')
        category_id = data.get('category_id')
        date = data.get('date')
        description = data.get('description')

        expense = ExpenseService.update_expense(expense_id, user_id, amount, category_id, date, description)
        if not expense:
            return jsonify(ExpenseView.render_error('Expense not found or access denied')), 404

        return jsonify(ExpenseView.render_success('Expense updated successfully', expense.expense_id)), 200

    @staticmethod
    def delete_expense(expense_id):
        data = request.get_json()
        user_id = data.get('user_id')

        expense = ExpenseService.delete_expense(expense_id, user_id)
        if not expense:
            return jsonify(ExpenseView.render_error('Expense not found or access denied')), 404

        return jsonify(ExpenseView.render_success('Expense deleted successfully', expense.expense_id)), 200
