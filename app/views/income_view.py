from flask import jsonify

# views/income_view.py
class IncomeView:
    @staticmethod
    def render_income(income):
        return {
            'income_id': income.income_id,
            'user_id': income.user_id,
            'amount': float(income.amount),
            'source': income.source,
            'date': str(income.date),
            'description': income.description,
            'created_at': str(income.created_at)
        }

    @staticmethod
    def render_incomes(incomes):
        return [IncomeView.render_income(income) for income in incomes]

    @staticmethod
    def render_success(message, income_id=None):
        response = {'message': message}
        if income_id:
            response['income_id'] = income_id
        return response

    @staticmethod
    def render_error(message):
        return {'error': message}
