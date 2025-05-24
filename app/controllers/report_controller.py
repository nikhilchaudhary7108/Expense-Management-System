# controllers/report_controller.py
from flask import request, jsonify, send_file
from app.services.report_service import ReportService
from app.services.user_service import UserService
from app.views.report_view import ReportView

class ReportController:
    @staticmethod
    def add_report():
        data = request.get_json()
        user_id = data.get('userId')
        title = data.get('title')
        content = data.get('content')

        report = ReportService.add_report(user_id, title, content)
        return jsonify(ReportView.render_success("Report added successfully", report.report_id)), 201

    @staticmethod
    def get_report(report_id):
        user_id = request.args.get('userId', type=int)

        report = ReportService.get_report_by_id(report_id)
        if not report:
            return jsonify(ReportView.render_error("Report not found")), 404

        if not UserService.is_admin(user_id) and report.user_id != user_id:
            return jsonify(ReportView.render_error("Unauthorized access")), 403

        return jsonify(ReportView.render_report(report)), 200

    @staticmethod
    def get_all_reports(user_id):
        if not UserService.is_admin(user_id):
            reports = ReportService.get_reports_by_user(user_id)
        else:
            reports = ReportService.get_all_reports()

        return jsonify(ReportView.render_reports(reports)), 200

    @staticmethod
    def update_report(report_id):
        data = request.get_json()
        user_id = data.get('userId')
        title = data.get('title')
        content = data.get('content')

        report = ReportService.get_report_by_id(report_id)
        if not report:
            return jsonify(ReportView.render_error("Report not found")), 404

        if not UserService.is_admin(user_id) and report.user_id != user_id:
            return jsonify(ReportView.render_error("Unauthorized access")), 403

        updated_report = ReportService.update_report(report_id, title, content)
        return jsonify(ReportView.render_success("Report updated successfully", updated_report.report_id)), 200

    @staticmethod
    def delete_report(report_id):
        data = request.get_json()
        user_id = data.get('userId')

        report = ReportService.get_report_by_id(report_id)
        if not report:
            return jsonify(ReportView.render_error("Report not found")), 404

        if not UserService.is_admin(user_id) and report.user_id != user_id:
            return jsonify(ReportView.render_error("Unauthorized access")), 403

        ReportService.delete_report(report_id)
        return jsonify(ReportView.render_success("Report deleted successfully", report_id)), 200

    @staticmethod
    def download_report(report_id):
        data = request.get_json()
        user_id = data.get('userId')

        pdf_path = ReportService.generate_pdf_report(report_id, user_id)
        if pdf_path == 'unauthorized':
            return jsonify(ReportView.render_error("Unauthorized access")), 403
        if not pdf_path:
            return jsonify(ReportView.render_error("Report not found")), 404

        return send_file(pdf_path, as_attachment=True)
