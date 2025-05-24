# services/budget_service.py

from app.models.budget_model import Budget
from app.shared.utils.db_utils import db
from datetime import datetime
from app.services.user_service import UserService

class BudgetService:
    @staticmethod
    def add_budget(user_id, name, amount, start_date, end_date, category_id=None):
        if not UserService.is_admin(user_id):
            return None  # Unauthorized

        budget = Budget(
            user_id=user_id,
            name=name,
            amount=amount,
            start_date=start_date,
            end_date=end_date,
            category_id=category_id,
            created_at=datetime.utcnow()
        )
        db.session.add(budget)
        db.session.commit()
        return budget

    @staticmethod
    def get_budget_by_id(budget_id):
        return Budget.query.get(budget_id)

    @staticmethod
    def get_all_budgets_for_user(user_id):
        return Budget.query.filter_by(user_id=user_id).all()

    @staticmethod
    def update_budget(user_id, budget_id, name=None, amount=None, start_date=None, end_date=None, category_id=None):
        if not UserService.is_admin(user_id):
            return None

        budget = Budget.query.get(budget_id)
        if not budget:
            return None

        if name is not None:
            budget.name = name
        if amount is not None:
            budget.amount = amount
        if start_date is not None:
            budget.start_date = start_date
        if end_date is not None:
            budget.end_date = end_date
        if category_id is not None:
            budget.category_id = category_id

        budget.updated_at = datetime.utcnow()
        db.session.commit()
        return budget

    @staticmethod
    def delete_budget(user_id, budget_id):
        if not UserService.is_admin(user_id):
            return None

        budget = Budget.query.get(budget_id)
        if not budget:
            return None

        db.session.delete(budget)
        db.session.commit()
        return budget
