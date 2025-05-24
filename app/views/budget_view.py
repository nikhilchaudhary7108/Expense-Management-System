# views/budget_view.py
from flask import jsonify

# views/budget_view.py

class BudgetView:
    @staticmethod
    def render_budget(budget):
        return {
            "budget_id": budget.budget_id,
            "user_id": budget.user_id,
            "name": budget.name,
            "amount": float(budget.amount),
            "start_date": str(budget.start_date),
            "end_date": str(budget.end_date),
            "category_id": budget.category_id,
            "created_at": str(budget.created_at) if budget.created_at else None,
            "updated_at": str(budget.updated_at) if budget.updated_at else None
        }

    @staticmethod
    def render_budgets(budgets):
        return [BudgetView.render_budget(budget) for budget in budgets]

    @staticmethod
    def render_success(message, budget_id=None):
        response = {"message": message}
        if budget_id:
            response["budget_id"] = budget_id
        return response

    @staticmethod
    def render_error(message):
        return {"error": message}

