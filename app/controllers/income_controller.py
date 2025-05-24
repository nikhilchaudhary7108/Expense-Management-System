# controllers/income_controller.py
from flask import request, jsonify
from app.services.income_service import IncomeService
from app.services.user_service import UserService
from app.views.income_view import IncomeView

class IncomeController:
    @staticmethod
    def add_income():
        data = request.get_json()
        user_id = data.get('user_id')
        amount = data.get('amount')
        source = data.get('source')
        date = data.get('date')
        description = data.get('description')

        income = IncomeService.add_income(user_id, amount, source, date, description)
        return jsonify(IncomeView.render_success("Income added successfully", income.income_id)), 201

    @staticmethod
    def get_income(income_id):
        income = IncomeService.get_income_by_id(income_id)
        if income:
            return jsonify(IncomeView.render_income(income)), 200
        return jsonify(IncomeView.render_error("Income not found")), 404

    @staticmethod
    def get_all_incomes(user_id):
        incomes = IncomeService.get_all_incomes_for_user(user_id)
        return jsonify(IncomeView.render_incomes(incomes)), 200

    @staticmethod
    def update_income(income_id):
        data = request.get_json()
        user_id = data.get('user_id')
        amount = data.get('amount')
        source = data.get('source')
        date = data.get('date')
        description = data.get('description')

        income = IncomeService.update_income(income_id, user_id, amount, source, date, description)

        if income == "unauthorized":
            return jsonify(IncomeView.render_error("Unauthorized access")), 403
        elif income:
            return jsonify(IncomeView.render_success("Income updated successfully", income.income_id)), 200
        else:
            return jsonify(IncomeView.render_error("Income not found")), 404

    @staticmethod
    def delete_income(income_id):
        data = request.get_json()
        user_id = data.get('user_id')

        income = IncomeService.delete_income(income_id, user_id)

        if income == "unauthorized":
            return jsonify(IncomeView.render_error("Unauthorized access")), 403
        elif income:
            return jsonify(IncomeView.render_success("Income deleted successfully", income.income_id)), 200
        else:
            return jsonify(IncomeView.render_error("Income not found")), 404
