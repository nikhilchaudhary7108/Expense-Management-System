# views/expense_view.py
from flask import jsonify

# views/expense_view.py
class ExpenseView:
    @staticmethod
    def render_expense(expense):
        return {
            "expense_id": expense.expense_id,
            "user_id": expense.user_id,
            "amount": float(expense.amount),
            "category_id": expense.category_id,
            "date": str(expense.date),
            "description": expense.description,
            "created_at": str(expense.created_at)
        }

    @staticmethod
    def render_expenses(expenses):
        return [ExpenseView.render_expense(expense) for expense in expenses]

    @staticmethod
    def render_success(message, expense_id=None):
        response = {"message": message}
        if expense_id:
            response["expense_id"] = expense_id
        return response

    @staticmethod
    def render_error(message):
        return {"error": message}

