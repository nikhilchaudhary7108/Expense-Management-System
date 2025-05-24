# controllers/category_controller.py
from flask import request, jsonify
from app.services.category_service import CategoryService
from app.views.category_view import CategoryView

class CategoryController:
    @staticmethod
    def get_all_categories():
        categories = CategoryService.get_all_categories()
        return jsonify(CategoryView.render_categories(categories)), 200

    @staticmethod
    def get_category(category_id):
        category = CategoryService.get_category_by_id(category_id)
        if category:
            return jsonify(CategoryView.render_category(category)), 200
        return jsonify({"error": "Category not found"}), 404

    @staticmethod
    def add_category():
        data = request.get_json()
        user_id = data.get('user_id')
        name = data.get('name')

        if not CategoryService.is_admin(user_id):
            return jsonify({"error": "Unauthorized access"}), 403

        category = CategoryService.add_category(name)
        return jsonify({"message": "Category added successfully", "category_id": category.category_id}), 201

    @staticmethod
    def update_category(category_id):
        data = request.get_json()
        user_id = data.get('user_id')
        name = data.get('name')

        if not CategoryService.is_admin(user_id):
            return jsonify({"error": "Unauthorized access"}), 403

        category = CategoryService.update_category(category_id, name)
        if category:
            return jsonify({"message": "Category updated successfully", "category_id": category.category_id}), 200
        return jsonify({"error": "Category not found"}), 404

    @staticmethod
    def delete_category(category_id):
        data = request.get_json()
        user_id = data.get('user_id')

        if not CategoryService.is_admin(user_id):
            return jsonify({"error": "Unauthorized access"}), 403

        category = CategoryService.delete_category(category_id)
        if category:
            return jsonify({"message": "Category deleted successfully", "category_id": category.category_id}), 200
        return jsonify({"error": "Category not found"}), 404
