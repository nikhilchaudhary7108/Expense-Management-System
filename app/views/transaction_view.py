from flask import jsonify

class TransactionView:
    @staticmethod
    def render_transaction(transaction):
        return {
            'transaction_id': transaction.transaction_id,
            'user_id': transaction.user_id,
            'amount': float(transaction.amount),
            'type': transaction.type,
            'category_id': transaction.category_id,
            'date': str(transaction.date),
            'description': transaction.description,
            'created_at': str(transaction.created_at)
        }

    @staticmethod
    def render_transactions(transactions):
        return [TransactionView.render_transaction(txn) for txn in transactions]

    @staticmethod
    def render_success(message, transaction_id=None):
        response = {"message": message}
        if transaction_id is not None:
            response["transaction_id"] = transaction_id
        return response

    @staticmethod
    def render_error(message):
        return {"error": message}
