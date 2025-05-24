# services/income_service.py
from app.models.income_model import Income
from app.shared.utils.db_utils import db
from datetime import datetime
from app.services.user_service import UserService

class IncomeService:
    @staticmethod
    def add_income(user_id, amount, source, date, description):
        income = Income(
            user_id=user_id,
            amount=amount,
            source=source,
            date=date,
            description=description,
            created_at=datetime.utcnow()
        )
        db.session.add(income)
        db.session.commit()
        return income

    @staticmethod
    def get_income_by_id(income_id):
        return Income.query.get(income_id)

    @staticmethod
    def get_all_incomes_for_user(user_id):
        return Income.query.filter_by(user_id=user_id).all()

    @staticmethod
    def update_income(income_id, user_id, amount=None, source=None, date=None, description=None):
        income = Income.query.get(income_id)
        if not income:
            return None
        if not UserService.is_admin(user_id) and income.user_id != user_id:
            return "unauthorized"

        if amount is not None:
            income.amount = amount
        if source is not None:
            income.source = source
        if date is not None:
            income.date = date
        if description is not None:
            income.description = description

        db.session.commit()
        return income

    @staticmethod
    def delete_income(income_id, user_id):
        income = Income.query.get(income_id)
        if not income:
            return None
        if not UserService.is_admin(user_id) and income.user_id != user_id:
            return "unauthorized"

        db.session.delete(income)
        db.session.commit()
        return income
