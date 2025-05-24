# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS

# db = SQLAlchemy()

# def create_app():
#     app = Flask(__name__)

#     app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:ar123@localhost/expense_tracker"
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['SECRET_KEY'] = 'your_secret_key'

#     db.init_app(app)
#     CORS(app)

#     from app.models import  auth_model,budget_model,category_model,expense_model,income_model,report_model,transaction_model,user_model # Ensure models are loaded

#     with app.app_context():
#         db.create_all()

#     return app
