from flask import render_template
from app.models import User, Expense, Income, Budget, Transaction, Category

# Assuming you have the user's id (user_id) after login
@app.route('/dashboard')
def dashboard():
    user_id = 'user_id_here'  # Replace with actual user ID after login

    # Get the user's budget
    budget = Budget.query.filter_by(user_id=user_id).all()

    # Get the user's expenses and incomes
    expenses = Expense.query.filter_by(user_id=user_id).all()
    incomes = Income.query.filter_by(user_id=user_id).all()

    # Get the user's transactions (if needed)
    transactions = Transaction.query.filter_by(user_id=user_id).all()

    # Summarize income and expense data
    total_expense = sum(exp.amount for exp in expenses)
    total_income = sum(inc.amount for inc in incomes)

    # You can also calculate budgets here or pass it to the frontend
    budget_data = [{'name': b.name, 'amount': b.amount, 'start_date': b.start_date, 'end_date': b.end_date} for b in budget]

    # Return data to the dashboard template
    return render_template(
        'dashboard.html',
        total_expense=total_expense,
        total_income=total_income,
        budget_data=budget_data,
        transactions=transactions,
        expenses=expenses,
        incomes=incomes
    )
