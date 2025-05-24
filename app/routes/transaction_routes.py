# routes/transaction_routes.py
from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.controllers.transaction_controller import TransactionController

transaction_bp = Blueprint('transaction_bp', __name__, url_prefix='/transactions')
CORS(transaction_bp)

# Route to get all transactions for a specific user
@transaction_bp.route('/user/<int:user_id>', methods=['GET'])
def get_all_transactions(user_id):
    return TransactionController.get_all_transactions(user_id)

# Route to get a specific transaction by ID
@transaction_bp.route('/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    return TransactionController.get_transaction(transaction_id)

# Route to create a new transaction
@transaction_bp.route('/', methods=['POST'])
def add_transaction():
    return TransactionController.add_transaction()

# Route to update a specific transaction by ID
@transaction_bp.route('/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    return TransactionController.update_transaction(transaction_id)

# Route to delete a specific transaction by ID
@transaction_bp.route('/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    return TransactionController.delete_transaction(transaction_id)
