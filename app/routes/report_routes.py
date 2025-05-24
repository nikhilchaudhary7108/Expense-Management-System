# routes/report_routes.py
from flask import Blueprint, request
from flask_cors import CORS
from app.controllers.report_controller import ReportController

report_bp = Blueprint('report_bp', __name__, url_prefix='/reports')
CORS(report_bp)

# Route to get all reports (admin sees all, user sees their own)
@report_bp.route('/', methods=['GET'])
def get_all_reports():
    user_id = request.args.get('userId', type=int)
    return ReportController.get_all_reports(user_id)

# Route to get a specific report by ID
@report_bp.route('/<int:report_id>', methods=['GET'])
def get_report(report_id):
    return ReportController.get_report(report_id)

# Route to create a new report
@report_bp.route('/', methods=['POST'])
def add_report():
    return ReportController.add_report()

# Route to update a specific report
@report_bp.route('/<int:report_id>', methods=['PUT'])
def update_report(report_id):
    return ReportController.update_report(report_id)

# Route to delete a specific report
@report_bp.route('/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    return ReportController.delete_report(report_id)

# Route to download a report as PDF
@report_bp.route('/<int:report_id>/download', methods=['POST'])
def download_report(report_id):
    return ReportController.download_report(report_id)
