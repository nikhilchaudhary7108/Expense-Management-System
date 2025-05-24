from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random
from app.shared.utils.db_utils import db
from app.models.models import User, Expense, Income, Transaction , Category , Budget
from datetime import datetime, timedelta
from app.controllers.controllers import register_user
from sqlalchemy.orm import joinedload
from sqlalchemy import func  

# from flask import Blueprint, request, jsonify
import smtplib
# import random
from email.message import EmailMessage
# from datetime import datetime, timedelta


main_bp = Blueprint('main', __name__)

@main_bp.route('/register', methods=['POST'])
def register():
    return register_user()



@main_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid user ID or password'}), 401
    return jsonify({'message': 'Login successful', 'user': {
        'username': user.username,
        'email': user.email,
        'user_id': user.user_id,
        'mobile_no' : user.mobile_no
    }})


@main_bp.route('/add-category', methods=['POST'])
def add_category():
    data = request.get_json()
    category_name = data.get('category_name')
    user_id = data.get('user_id') 

    if not category_name or not user_id:
        return jsonify({'error': 'Category name and user ID are required'}), 400

    # Check if the same user already has this category
    existing_category = Category.query.filter_by(name=category_name, user_id=user_id).first()
    if existing_category:
        return jsonify({'error': 'Category already exists for this user'}), 400

    # Add new category
    new_category = Category(name=category_name, user_id=user_id)
    db.session.add(new_category)
    db.session.commit()

    return jsonify({
        'message': 'Category added successfully',
        'category_id': new_category.category_id,
        'name': new_category.name
    }), 201


@main_bp.route('/categories/<user_id>', methods=['GET'])
def get_categories(user_id):
    categories = Category.query.filter((Category.user_id == user_id) | (Category.user_id == None)).all()
    result = [{'category_id': c.category_id, 'name': c.name} for c in categories]
    return jsonify(result)

    # return jsonify({'message': 'Category added successfully', 'category_name': new_category.name}), 201

# ----------- ADD EXPENSE -----------
@main_bp.route('/add-expense', methods=['POST'])
def add_expense():
    data = request.get_json()
    user_id = data.get('user_id')
    amount = data.get('amount')
    category_name = data.get('category_name')  # Use category name instead of category_id
    date = data.get('date')
    description = data.get('description')

    # Find the category by name
    category = Category.query.filter(
    ((Category.user_id == user_id) | (Category.user_id == None)) & 
    (Category.name == category_name)
     ).first()
    if not category:
        return jsonify({'error': 'Category not found'}), 400

    # Create expense with category_id
    expense = Expense(user_id=user_id, amount=amount, category_id=category.category_id,
                      date=date, description=description)

    transaction = Transaction(user_id=user_id, amount=amount, type='expense',
                              category_id=category.category_id, date=date, description=description)

    db.session.add(expense)
    db.session.add(transaction)
    db.session.commit()
    return jsonify({
    'message': 'Expense added successfully',
    'expense': {
        'user_id': user_id,
        'amount': amount,
        'category_name': category.name,
        'description': description,
        'date': date,
        'type': 'expense'
    }
})


# ----------- ADD INCOME -----------
@main_bp.route('/add-income', methods=['POST'])
def add_income():
    data = request.get_json()
    user_id = data.get('user_id')
    amount = data.get('amount')
    source = data.get('source')
    date = data.get('date')
    description = data.get('description')

    income = Income(user_id=user_id, amount=amount, source=source,
                    date=date, description=description)
    transaction = Transaction(user_id=user_id, amount=amount, type='income',
                              category_id=None, date=date, description=description)

    db.session.add(income)
    db.session.add(transaction)
    db.session.commit()
    return jsonify({
    'message': 'Income added successfully',
    'income': {
        'user_id': user_id,
        'amount': amount,
        'source': source,
        'description': description,
        'date': date,
        'type': 'income'
    }
})

from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError


@main_bp.route('/transactions/<user_id>', methods=['GET'])
def view_transactions(user_id):
    transactions = Transaction.query.filter_by(user_id=user_id).options(joinedload(Transaction.category)).order_by(Transaction.date.desc()).all()

    if not transactions:
        return jsonify({"message": "No transactions found for this user"}), 404

    return jsonify([{
        'amount': t.amount,
        'type': t.type,
        'date': t.date.strftime('%Y-%m-%d'),
        'description': t.description,
        'category_name': t.category.name if t.category else 'Unknown'  # Include category name
    } for t in transactions])

@main_bp.route('/budget-analysis/<user_id>', methods=['GET'])
def budget_analysis(user_id):
    last_7_days = datetime.now() - timedelta(days=7)
    transactions = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.date >= last_7_days
    ).all()

    income = sum(t.amount for t in transactions if t.type == 'income')
    expense = sum(t.amount for t in transactions if t.type == 'expense')

    return jsonify({
        'last_7_days_income': income,
        'last_7_days_expense': expense,
        'balance': income - expense
    })

@main_bp.route('/add-budget', methods=['POST'])
def add_budget():
    data = request.get_json()
    user_id = data.get('user_id')
    name = data.get('name')
    amount = data.get('amount')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    category_name = data.get('category_name')

    # Validate required fields
    if not all([user_id, name, amount, start_date, end_date, category_name]):
        return jsonify({'error': 'Missing required fields'}), 400

    # Look up category by name
    category = Category.query.filter_by(name=category_name).first()
    if not category:
        return jsonify({'error': 'Category not found'}), 400
    
    existing_budget = Budget.query.filter_by(user_id=user_id, name=name, category_id=category.category_id).first()
    if existing_budget:
        return jsonify({'error': 'Budget with this name already exists for this category'}), 409


    # Create new budget
    budget = Budget(
        user_id=user_id,
        name=name,
        amount=amount,
        start_date=start_date,
        end_date=end_date,
        category_id=category.category_id
    )

    db.session.add(budget)
    db.session.commit()

    return jsonify({
        'message': 'Budget created successfully',
        'budget': {
            'user_id': user_id,
            'name': name,
            'amount': amount,
            'start_date': start_date,
            'end_date': end_date,
            'category_name': category.name
        }
    }), 201
@main_bp.route('/budget-summary/<user_id>', methods=['GET'])
def budget_summary(user_id):
    budgets = Budget.query.filter_by(user_id=user_id).all()
    summary = []

    for budget in budgets:
        expenses = Expense.query.join(Category).filter(
            Expense.user_id == user_id,
            Category.category_id == budget.category_id,
            Expense.date >= budget.start_date,
            Expense.date <= budget.end_date
        ).all()

        total_spent = sum(e.amount for e in expenses)
        remaining = float(budget.amount) - total_spent

        # Fetch category using category_id
        category = Category.query.filter_by(category_id=budget.category_id).first()

        summary.append({
            'budget_name': budget.name,
            'category_name': category.name if category else 'Unknown',  # Handle missing category
            'budget_amount': float(budget.amount),
            'total_spent': total_spent,
            'remaining': remaining,
            'start_date': budget.start_date.strftime('%Y-%m-%d'),
            'end_date': budget.end_date.strftime('%Y-%m-%d')
        })

    return jsonify(summary), 200





# Email credentials (use env vars ideally)
EMAIL_ADDRESS = "sujaniannikhil68@gmail.com"
EMAIL_PASSWORD = "eotw klkg ktda rqac"

# Temporary OTP storage
otp_store = {}  # { email: { 'otp': '123456', 'expires': datetime_obj } }

# --- SEND OTP ---
@main_bp.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    otp = str(random.randint(100000, 999999))
    expiration = datetime.now() + timedelta(minutes=5)

    otp_store[email] = {'otp': otp, 'expires': expiration}

    msg = EmailMessage()
    msg['Subject'] = 'Your OTP Code'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg.set_content(
    f"""
🎉 Hey there!

Your one-time password (OTP) is: **{otp}**

Use this magical number to complete your registration journey. But be quick! 🕐
This OTP self-destructs (not literally) in 5 minutes. 💣⏳

If you didn’t request this, either someone really wants to be you 😎 or it was a mistake — just ignore this message.

Stay awesome! 🚀

- Your Friendly Expense Tracker Manager 🤖
"""
)


    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        return jsonify({'message': 'OTP sent successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to send OTP'}), 500

# --- VERIFY OTP ---
@main_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email')
    user_otp = data.get('otp')

    if not email or not user_otp:
        return jsonify({'error': 'Email and OTP are required'}), 400

    record = otp_store.get(email)
    if not record:
        return jsonify({'error': 'No OTP found for this email'}), 400

    if datetime.now() > record['expires']:
        del otp_store[email]
        return jsonify({'error': 'OTP has expired'}), 400

    if user_otp != record['otp']:
        return jsonify({'error': 'Incorrect OTP'}), 400

    del otp_store[email]
    return jsonify({'message': 'OTP verified successfully'}), 200

@main_bp.route('/check-email', methods=['POST'])
def check_email():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'exists': True}), 200
    return jsonify({'exists': False}), 200

@main_bp.route('/transactions/graph/<string:user_id>', methods=['GET'])
def view_transaction_graph(user_id):
    transactions = Transaction.query.filter_by(user_id=user_id).options(joinedload(Transaction.category)).all()

    if not transactions:
        return jsonify([]), 200  # Return an empty array instead of an error


    # Process transactions and group by category to calculate total spent
    category_totals = {}
    for t in transactions:
        category_name = t.category.name if t.category else 'Unknown'
        if category_name in category_totals:
            category_totals[category_name] += t.amount
        else:
            category_totals[category_name] = t.amount

    # Format the data to send back
    data = [{'category_name': category, 'total_spent': amount} for category, amount in category_totals.items()]

    return jsonify(data), 200



@main_bp.route('/graphical/category-expenditure/<string:user_id>', methods=['GET'])
def category_expenditure(user_id):
    """
    Returns total expenditure for each category for a given user.
    """
    try:
        category_expenses = db.session.query(
            Category.name.label('category_name'),
            func.sum(Expense.amount).label('total_amount')
        ).join(Expense, Expense.category_id == Category.category_id).filter(
            Expense.user_id == user_id
        ).group_by(Category.name).all()

        result = [{'category_name': ce.category_name, 'total_amount': float(ce.total_amount) if ce.total_amount else 0.0} for ce in category_expenses]
        return jsonify(result), 200

    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500


# @main_bp.route('/graphical/transactions/<string:user_id>', methods=['GET'])
# def get_transactions_by_duration(user_id):
#     """
#     Returns transactions for a given user within a specified time duration (7 or 30 days).
#     """
#     duration = request.args.get('duration', type=int)  # Get duration from query parameter
#     if not duration or duration not in [7, 30]:
#         return jsonify({'error': 'Invalid duration. Must be 7 or 30'}), 400

#     end_date = datetime.now()
#     start_date = end_date - timedelta(days=duration)

#     try:
#         transactions = Transaction.query.filter(
#             Transaction.user_id == user_id,
#             Transaction.date >= start_date,
#             Transaction.date <= end_date
#         ).order_by(Transaction.date).all()

#         result = [{
#             'date': t.date.strftime('%Y-%m-%d'),
#             'amount': float(t.amount),
#             'type': t.type
#         } for t in transactions]
#         return jsonify(result), 200

#     except SQLAlchemyError as e:
#         print(f"Database error: {e}")
#         return jsonify({'error': 'Database error occurred'}), 500
#     except Exception as e:
#         print(f"Unexpected error: {e}")
#         return jsonify({'error': 'An unexpected error occurred'}), 500


@main_bp.route('/graphical/balance/<string:user_id>', methods=['GET'])
def get_balance(user_id):
    """
    Returns the average and current balance for a given user.
    Note: For simplicity, the average balance is calculated as the average of the current balance over time.
    A more sophisticated average calculation might be needed based on specific requirements.
    """
    try:
        all_transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.date).all()

        if not all_transactions:
            return jsonify({'average_balance': 0.0, 'current_balance': 0.0}), 200

        total_income = sum(t.amount for t in all_transactions if t.type == 'income')
        total_expense = sum(t.amount for t in all_transactions if t.type == 'expense')
        current_balance = total_income - total_expense

        # Simple average balance calculation (can be improved)
        if all_transactions:
            average_balance = current_balance / len(all_transactions)
        else:
            average_balance = 0.0

        return jsonify({
            'average_balance': float(average_balance),
            'current_balance': float(current_balance)
        }), 200

    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500


@main_bp.route('/graphical/transactions/<string:user_id>', methods=['GET'])
def get_all_transactions(user_id):
    """
    Returns all transactions for a given user.
    """
    try:
        transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.date).all()

        result = [{
            'date': t.date.strftime('%Y-%m-%d'),
            'amount': float(t.amount),
            'type': t.type
        } for t in transactions]
        return jsonify(result), 200

    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500
