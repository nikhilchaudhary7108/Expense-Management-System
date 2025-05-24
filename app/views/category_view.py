# views/category_view.py
from flask import jsonify

# views/category_view.py
class CategoryView:
    @staticmethod
    def render_category(category):
        return {
            "category_id": category.category_id,
            "name": category.name
        }

    @staticmethod
    def render_categories(categories):
        return [CategoryView.render_category(cat) for cat in categories]

    @staticmethod
    def render_success(message, category_id=None):
        response = {"message": message}
        if category_id:
            response["category_id"] = category_id
        return response

    @staticmethod
    def render_error(message):
        return {"error": message}
