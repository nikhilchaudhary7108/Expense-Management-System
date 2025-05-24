# services/category_service.py
from app.shared.utils.db_utils import db
from app.models.category_model import Category
from app.services.user_service import UserService

class CategoryService:
    @staticmethod
    def add_category(user_id, name):
        if not UserService.is_admin(user_id):
            return None  # Unauthorized to add

        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    def get_all_categories():
        return Category.query.all()

    @staticmethod
    def get_category_by_id(category_id):
        return Category.query.get(category_id)

    @staticmethod
    def update_category(user_id, category_id, name):
        if not UserService.is_admin(user_id):
            return None  # Unauthorized to update

        category = Category.query.get(category_id)
        if not category:
            return None
        category.name = name
        db.session.commit()
        return category

    @staticmethod
    def delete_category(user_id, category_id):
        if not UserService.is_admin(user_id):
            return None  # Unauthorized to delete

        category = Category.query.get(category_id)
        if category:
            db.session.delete(category)
            db.session.commit()
        return category
