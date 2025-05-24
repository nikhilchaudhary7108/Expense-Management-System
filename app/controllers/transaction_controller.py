# controllers/transaction_controller.py
from flask import request, jsonify
from app.services.transaction_service import TransactionService
from app.services.user_service import UserService
from app.views.transaction_view import TransactionView

class TransactionController:
    @staticmethod
    def add_transaction():
        data = request.get_json()
        user_id = data.get('user_id')

        if not UserService.is_valid_user(user_id):
            return jsonify(TransactionView.render_error("Unauthorized access")), 403

        amount = data.get('amount')
        txn_type = data.get('type')
        date = data.get('date')
        category_id = data.get('category_id')
        description = data.get('description')

        transaction = TransactionService.add_transaction(user_id, amount, txn_type, date, category_id, description)
        if not transaction:
            return jsonify(TransactionView.render_error("Transaction creation failed")), 400

        return jsonify(TransactionView.render_success("Transaction added successfully", transaction.transaction_id)), 201

    @staticmethod
    def get_transaction(transaction_id):
        transaction = TransactionService.get_transaction_by_id(transaction_id)
        if not transaction:
            return jsonify(TransactionView.render_error("Transaction not found")), 404
        return jsonify(TransactionView.render_transaction(transaction)), 200

    @staticmethod
    def get_all_transactions(user_id):
        if not UserService.is_valid_user(user_id):
            return jsonify(TransactionView.render_error("Unauthorized access")), 403
        transactions = TransactionService.get_all_transactions_for_user(user_id)
        return jsonify(TransactionView.render_transactions(transactions)), 200

    @staticmethod
    def update_transaction(transaction_id):
        data = request.get_json()
        user_id = data.get('user_id')

        if not UserService.is_valid_user(user_id):
            return jsonify(TransactionView.render_error("Unauthorized access")), 403

        amount = data.get('amount')
        txn_type = data.get('type')
        date = data.get('date')
        category_id = data.get('category_id')
        description = data.get('description')

        transaction = TransactionService.update_transaction(transaction_id, amount, txn_type, date, category_id, description)
        if not transaction:
            return jsonify(TransactionView.render_error("Transaction not found")), 404
        return jsonify(TransactionView.render_success("Transaction updated successfully", transaction.transaction_id)), 200

    @staticmethod
    def delete_transaction(transaction_id):
        data = request.get_json()
        user_id = data.get('user_id')

        if not UserService.is_valid_user(user_id):
            return jsonify(TransactionView.render_error("Unauthorized access")), 403

        transaction = TransactionService.delete_transaction(transaction_id)
        if not transaction:
            return jsonify(TransactionView.render_error("Transaction not found")), 404
        return jsonify(TransactionView.render_success("Transaction deleted successfully", transaction.transaction_id)), 200
