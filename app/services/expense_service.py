# services/expense_service.py
from app.models.expense_model import Expense
from app.shared.utils.db_utils import db
from datetime import datetime
from app.services.user_service import UserService

class ExpenseService:
    @staticmethod
    def add_expense(user_id, amount, category_id, date, description):
        expense = Expense(
            user_id=user_id,
            amount=amount,
            category_id=category_id,
            date=date,
            description=description,
            created_at=datetime.utcnow()
        )
        db.session.add(expense)
        db.session.commit()
        return expense

    @staticmethod
    def get_expense_by_id(expense_id, requesting_user_id):
        expense = Expense.query.get(expense_id)
        if not expense:
            return None
        if expense.user_id != requesting_user_id and not UserService.is_admin(requesting_user_id):
            return None
        return expense

    @staticmethod
    def get_all_expenses(user_id):
        if UserService.is_admin(user_id):
            return Expense.query.all()
        return Expense.query.filter_by(user_id=user_id).all()

    @staticmethod
    def update_expense(expense_id, user_id, amount=None, category_id=None, date=None, description=None):
        expense = ExpenseService.get_expense_by_id(expense_id, user_id)
        if not expense:
            return None
        if amount is not None:
            expense.amount = amount
        if category_id is not None:
            expense.category_id = category_id
        if date is not None:
            expense.date = date
        if description is not None:
            expense.description = description
        db.session.commit()
        return expense

    @staticmethod
    def delete_expense(expense_id, user_id):
        expense = ExpenseService.get_expense_by_id(expense_id, user_id)
        if not expense:
            return None
        db.session.delete(expense)
        db.session.commit()
        return expense
