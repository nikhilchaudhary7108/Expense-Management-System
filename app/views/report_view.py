# views/report_view.py
from flask import jsonify

class ReportView:
    @staticmethod
    def render_report(report):
        return {
            'report_id': report.report_id,
            'user_id': report.user_id,
            'title': report.title,
            'content': report.content,
            'created_at': report.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    @staticmethod
    def render_reports(reports):
        return [ReportView.render_report(report) for report in reports]

    @staticmethod
    def render_success(message, report_id=None):
        response = {"message": message}
        if report_id:
            response["report_id"] = report_id
        return response

    @staticmethod
    def render_error(message):
        return {"error": message}
