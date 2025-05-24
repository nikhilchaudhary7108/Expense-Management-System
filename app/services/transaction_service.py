# services/transaction_service.py
from app.models.transaction_model import Transaction
from app.shared.utils.db_utils import db
from datetime import datetime
from app.services.user_service import UserService

class TransactionService:
    @staticmethod
    def add_transaction(user_id, amount, txn_type, date, category_id=None, description=None):
        if not UserService.is_valid_user(user_id):
            return None
        
        transaction = Transaction(
            user_id=user_id,
            amount=amount,
            type=txn_type,
            date=date,
            category_id=category_id,
            description=description,
            created_at=datetime.utcnow()
        )
        db.session.add(transaction)
        db.session.commit()
        return transaction

    @staticmethod
    def get_transaction_by_id(transaction_id):
        return Transaction.query.get(transaction_id)

    @staticmethod
    def get_all_transactions_for_user(user_id):
        return Transaction.query.filter_by(user_id=user_id).all()

    @staticmethod
    def update_transaction(transaction_id, amount=None, txn_type=None, date=None, category_id=None, description=None):
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return None

        if amount is not None:
            transaction.amount = amount
        if txn_type is not None:
            transaction.type = txn_type
        if date is not None:
            transaction.date = date
        if category_id is not None:
            transaction.category_id = category_id
        if description is not None:
            transaction.description = description

        db.session.commit()
        return transaction

    @staticmethod
    def delete_transaction(transaction_id):
        transaction = Transaction.query.get(transaction_id)
        if transaction:
            db.session.delete(transaction)
            db.session.commit()
        return transaction
