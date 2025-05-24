# models/auth_model.py
from app.shared.utils.db_utils import db
from datetime import datetime

class AuthToken(db.Model):
    __tablename__ = 'auth_tokens'

    token_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    token = db.Column(db.String(512), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
