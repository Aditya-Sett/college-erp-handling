from flask import Blueprint, request, jsonify
from app.services.report_service import ReportService

reports_bp = Blueprint("reports_routes", __name__)

@reports_bp.route("/department/<department>", methods=["GET"])
def get_department_report(department):
    try:
        data = ReportService.get_department_report_service(department)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500