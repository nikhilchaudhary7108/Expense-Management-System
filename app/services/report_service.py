# # services/report_service.py
# from app.models.expense_model import Expense
# from app.models.income_model import Income
# from app.models.user_model import User
# from app import db
# from sqlalchemy import func
# from matplotlib import pyplot as plt
# from fpdf import FPDF
# import os

# class ReportService:
#     @staticmethod
#     def get_expense_summary(user_id):
#         total_expense = db.session.query(func.sum(Expense.amount)).filter_by(userId=user_id).scalar() or 0
#         category_summary = db.session.query(
#             Expense.categoryId,
#             func.sum(Expense.amount)
#         ).filter_by(userId=user_id).group_by(Expense.categoryId).all()

#         return {
#             'total_expense': total_expense,
#             'category_summary': [
#                 {'category_id': cid, 'total': total}
#                 for cid, total in category_summary
#             ]
#         }

#     @staticmethod
#     def get_income_summary(user_id):
#         total_income = db.session.query(func.sum(Income.amount)).filter_by(userId=user_id).scalar() or 0
#         source_summary = db.session.query(
#             Income.source,
#             func.sum(Income.amount)
#         ).filter_by(userId=user_id).group_by(Income.source).all()

#         return {
#             'total_income': total_income,
#             'source_summary': [
#                 {'source': source, 'total': total}
#                 for source, total in source_summary
#             ]
#         }

#     @staticmethod
#     def get_net_savings(user_id):
#         total_expense = db.session.query(func.sum(Expense.amount)).filter_by(userId=user_id).scalar() or 0
#         total_income = db.session.query(func.sum(Income.amount)).filter_by(userId=user_id).scalar() or 0
#         return total_income - total_expense

#     @staticmethod
#     def generate_visualization(user_id):
#         summary = ReportService.get_expense_summary(user_id)
#         labels = [f"Category {item['category_id']}" for item in summary['category_summary']]
#         sizes = [item['total'] for item in summary['category_summary']]

#         plt.figure(figsize=(6, 6))
#         plt.pie(sizes, labels=labels, autopct='%1.1f%%')
#         plt.title('Expense Distribution by Category')
#         chart_path = f'static/expense_pie_{user_id}.png'
#         plt.savefig(chart_path)
#         plt.close()
#         return chart_path

#     @staticmethod
#     def generate_pdf_report(user_id):
#         income_summary = ReportService.get_income_summary(user_id)
#         expense_summary = ReportService.get_expense_summary(user_id)
#         net_savings = ReportService.get_net_savings(user_id)
#         chart_path = ReportService.generate_visualization(user_id)

#         pdf = FPDF()
#         pdf.add_page()
#         pdf.set_font("Arial", size=12)
#         pdf.cell(200, 10, txt="Expense Tracker Report", ln=True, align='C')

#         pdf.cell(200, 10, txt=f"Total Income: ₹{income_summary['total_income']}", ln=True)
#         pdf.cell(200, 10, txt=f"Total Expense: ₹{expense_summary['total_expense']}", ln=True)
#         pdf.cell(200, 10, txt=f"Net Savings: ₹{net_savings}", ln=True)

#         pdf.ln(10)
#         pdf.cell(200, 10, txt="Income Breakdown:", ln=True)
#         for item in income_summary['source_summary']:
#             pdf.cell(200, 10, txt=f"- {item['source']}: ₹{item['total']}", ln=True)

#         pdf.ln(5)
#         pdf.cell(200, 10, txt="Expense Breakdown:", ln=True)
#         for item in expense_summary['category_summary']:
#             pdf.cell(200, 10, txt=f"- Category {item['category_id']}: ₹{item['total']}", ln=True)

#         if os.path.exists(chart_path):
#             pdf.image(chart_path, x=30, y=pdf.get_y() + 10, w=150)

#         pdf_path = f'static/report_user_{user_id}.pdf'
#         pdf.output(pdf_path)
#         return pdf_path

#     @staticmethod
#     def is_admin(user_id):
#         user = User.query.get(user_id)
#         return user and user.role == 'admin'


# services/report_service.py
from app.models.report_model import Report
from app.shared.utils.db_utils import db
from datetime import datetime
from app.services.user_service import UserService
from weasyprint import HTML
import os

class ReportService:
    @staticmethod
    def create_report(user_id, title, content):
        report = Report(
            user_id=user_id,
            title=title,
            content=content,
            created_at=datetime.utcnow()
        )
        db.session.add(report)
        db.session.commit()
        return report

    @staticmethod
    def generate_pdf_report(report_id, user_id):
        report = Report.query.get(report_id)
        if not report:
            return None

        # Ensure user is either admin or owner of the report
        if not UserService.is_admin(user_id) and report.user_id != user_id:
            return 'unauthorized'

        # Generate PDF
        html = HTML(string=report.content)
        pdf_path = f'static/reports/report_{report_id}.pdf'
        html.write_pdf(pdf_path)
        return pdf_path
    
    
import matplotlib.pyplot as plt

def generate_expense_pie_chart(data_dict, output_path='static/charts/pie_chart.png'):
    labels = list(data_dict.keys())
    sizes = list(data_dict.values())

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Expenses by Category')
    plt.savefig(output_path)
    plt.close()
    return output_path
