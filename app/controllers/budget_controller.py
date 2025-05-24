# controllers/budget_controller.py

from flask import request, jsonify
from app.services.budget_service import BudgetService
from app.services.user_service import UserService
from app.views.budget_view import BudgetView

class BudgetController:
    @staticmethod
    def add_budget():
        data = request.get_json()
        user_id = data.get('user_id')

        if not UserService.is_admin(user_id):
            return jsonify(BudgetView.render_error('Unauthorized access')), 403

        name = data.get('name')
        amount = data.get('amount')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        category_id = data.get('category_id')

        budget = BudgetService.add_budget(user_id, name, amount, start_date, end_date, category_id)
        if budget:
            return jsonify(BudgetView.render_success('Budget added successfully', budget.budget_id)), 201
        return jsonify(BudgetView.render_error('Failed to add budget')), 400

    @staticmethod
    def get_budget(budget_id):
        budget = BudgetService.get_budget_by_id(budget_id)
        if budget:
            return jsonify(BudgetView.render_budget(budget)), 200
        return jsonify(BudgetView.render_error('Budget not found')), 404

    @staticmethod
    def get_all_budgets(user_id):
        budgets = BudgetService.get_all_budgets_for_user(user_id)
        return jsonify(BudgetView.render_budgets(budgets)), 200

    @staticmethod
    def update_budget(budget_id):
        data = request.get_json()
        user_id = data.get('user_id')

        if not UserService.is_admin(user_id):
            return jsonify(BudgetView.render_error('Unauthorized access')), 403

        name = data.get('name')
        amount = data.get('amount')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        category_id = data.get('category_id')

        budget = BudgetService.update_budget(user_id, budget_id, name, amount, start_date, end_date, category_id)
        if budget:
            return jsonify(BudgetView.render_success('Budget updated successfully', budget.budget_id)), 200
        return jsonify(BudgetView.render_error('Budget not found or update failed')), 404

    @staticmethod
    def delete_budget(budget_id):
        data = request.get_json()
        user_id = data.get('user_id')

        if not UserService.is_admin(user_id):
            return jsonify(BudgetView.render_error('Unauthorized access')), 403

        budget = BudgetService.delete_budget(user_id, budget_id)
        if budget:
            return jsonify(BudgetView.render_success('Budget deleted successfully', budget.budget_id)), 200
        return jsonify(BudgetView.render_error('Budget not found or delete failed')), 404
