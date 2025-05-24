from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets
import random
from app.shared.utils.db_utils import db
import re


from app.models.models import db, User, Expense, Income, Transaction
# controllers.py
# from app.shared.utils.db_utils import generate_unique_user_id




import re
import random
from flask import request, jsonify
from werkzeug.security import generate_password_hash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Store OTPs temporarily (You should ideally use a database or cache)
otp_store = {}

# @main_bp.route('/register', methods=['POST'])
from datetime import datetime, timedelta
import random
import smtplib
from email.message import EmailMessage
from flask import request, jsonify
from werkzeug.security import generate_password_hash

# Temporary OTP storage
otp_store = {}  # { email: { 'otp': '123456', 'expires': datetime_obj } }

# Email credentials (use environment variables ideally)
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"

# @main_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    full_name = data.get('full_name')
    mobile_no = data.get('mobile_no')
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    user_otp = data.get('otp')  # Get OTP entered by user

    if not all([full_name, mobile_no, email, password, username]):
        return jsonify({'error': 'All fields are required'}), 400

    # Step 1: Check if the email already exists in the database
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'Email already exists'}), 400

    # Step 2: Validate OTP
    # record = otp_store.get(email)
    # if not record:
    #     return jsonify({'error': 'No OTP found for this email'}), 400

    # if datetime.now() > record['expires']:
    #     del otp_store[email]
    #     return jsonify({'error': 'OTP has expired'}), 400

    # if user_otp != record['otp']:
    #     return jsonify({'error': 'Incorrect OTP'}), 400

    # del otp_store[email]  # OTP verification successful

    # Step 3: Proceed with the rest of the registration logic (after OTP verification)
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long'}), 400

    existing_username = User.query.filter_by(username=username).first()
    if existing_username:
        return jsonify({'error': 'Username already taken'}), 400

    # Email format validation
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, email):
        return jsonify({'error': 'Invalid email format'}), 400

    # Generate user_id based on full_name
    prefix = full_name.split()[0].lower()
    suffix = str(random.randint(10, 9999))
    user_id = prefix + suffix

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create new user
    new_user = User(
        user_id=user_id,
        username=username,
        full_name=full_name,
        email=email,
        mobile_no=mobile_no,
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully, please login', 'user_id': user_id}), 201

# ------------------ Registration ------------------
# def register_user():
#     data = request.get_json()
#     full_name = data.get('full_name')  # this is fine if frontend sends 'name'
#     mobile_no = data.get('mobile_no')
#     email = data.get('email')
#     password = data.get('password')
#     username = data.get('username')

#     if not all([full_name, mobile_no, email, password, username]):
#         return jsonify({'error': 'All fields are required'}), 400

#     if len(password) < 6:
#         return jsonify({'error': 'Password must be at least 6 characters long'}), 400

#     if not otp_store.get(email):  # Make sure OTP was sent and verified
#         return jsonify({'error': 'Please verify your email with OTP first'}), 400

#     # Check if email already exists
#     existing_user = User.query.filter_by(email=email).first()
#     if existing_user:
#         return jsonify({'error': 'Email already exists'}), 400
    
#     existing_username = User.query.filter_by(username=username).first()
#     if existing_username:
#         return jsonify({'error': 'Username already taken'}), 400
    
#     email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
#     if not re.match(email_regex, email):
#         return jsonify({'error': 'Invalid email format'}), 400

#     # Generate user_id based on full_name (can add more complexity if needed)
#     prefix = full_name.split()[0].lower()

#     suffix =  str(random.randint(10, 9898))
#     user_id = prefix + suffix
# # datetime.now().strftime('%d%m%H%M')
#     # Hash the password
#     hashed_password = generate_password_hash(password)

#     # Create new user
#     new_user = User(
#         user_id=user_id,
#         username=username,
#         full_name=full_name,  # Match your database column
#         email=email,
#         mobile_no=mobile_no,
#         password=hashed_password
#     )
#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({'message': 'User registered successfully, please login', 'user_id': user_id}), 201



# ------------------ Login ------------------
def login_user():
    data = request.get_json()
    user_id = data.get('user_id')
    password = data.get('password')

    if not all([user_id, password]):
        return jsonify({'error': 'User ID and Password required'}), 400

    user = User.query.filter_by(user_id=user_id).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful', 'user_id': user.user_id, 'username': user.username}), 200

# ------------------ Add Expense ------------------
def add_expense():
    data = request.get_json()
    user_id = data.get('user_id')
    amount = data.get('amount')
    category_id = data.get('category_id')
    date = data.get('date')
    description = data.get('description')

    if not all([user_id, amount, category_id, date]):
        return jsonify({'error': 'Missing required fields'}), 400

    expense = Expense(
        user_id=user_id,
        amount=amount,
        category_id=category_id,
        date=date,
        description=description
    )
    db.session.add(expense)
    db.session.commit()

    transaction = Transaction(
        user_id=user_id,
        amount=amount,
        type='expense',
        category_id=category_id,
        date=date,
        description=description
    )
    db.session.add(transaction)
    db.session.commit()

    return jsonify({'message': 'Expense added successfully'}), 201

# ------------------ Add Income ------------------
def add_income():
    data = request.get_json()
    user_id = data.get('user_id')
    amount = data.get('amount')
    source = data.get('source')
    date = data.get('date')
    description = data.get('description')

    if not all([user_id, amount, date]):
        return jsonify({'error': 'Missing required fields'}), 400

    income = Income(
        user_id=user_id,
        amount=amount,
        source=source,
        date=date,
        description=description
    )
    db.session.add(income)
    db.session.commit()

    transaction = Transaction(
        user_id=user_id,
        amount=amount,
        type='income',
        category_id=None,
        date=date,
        description=description
    )
    db.session.add(transaction)
    db.session.commit()

    return jsonify({'message': 'Income added successfully'}), 201

# ------------------ Get All Transactions ------------------
def get_transactions(user_id):
    transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.date.desc()).all()
    result = []
    for t in transactions:
        result.append({
            'id': t.transaction_id,
            'amount': t.amount,
            'type': t.type,
            'date': t.date.strftime('%Y-%m-%d'),
            'description': t.description
        })
    return jsonify(result)

# ------------------ Budget Analysis ------------------
def get_budget_analysis(user_id, period):
    today = datetime.today().date()
    if period == '7days':
        start_date = today - timedelta(days=7)
    elif period == 'month':
        start_date = today.replace(day=1)
    else:
        return jsonify({'error': 'Invalid period'}), 400

    expenses = db.session.query(Transaction).filter_by(user_id=user_id, type='expense').filter(Transaction.date >= start_date).all()
    incomes = db.session.query(Transaction).filter_by(user_id=user_id, type='income').filter(Transaction.date >= start_date).all()

    total_expense = sum(e.amount for e in expenses)
    total_income = sum(i.amount for i in incomes)

    return jsonify({
        'total_expense': total_expense,
        'total_income': total_income,
        'net_balance': total_income - total_expense
    })
