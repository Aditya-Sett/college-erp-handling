from flask import Blueprint, request, jsonify, send_file
from app.services.report_generate_service import ReportGenerator
from app.utils.excel_generator_utils import generate_excel

report_generate_bp = Blueprint("report_generate", __name__)

@report_generate_bp.route("/report", methods=["POST", "GET"])
def attendance_report():

    if request.method == "POST":
        data = request.json
    else:
        data = {
            "teacherId": request.args.get("teacherId"),
            "department": request.args.get("department"),
            "academicYear": request.args.get("academicYear"),
            "sem": request.args.get("sem"),
            "subject": request.args.get("subject")
        }

    report = ReportGenerator.generate_attendance_report(data)
    print("REPORT:", report)

    # ❌ STOP here if failed
    if not report.get("success"):
        return jsonify(report), 500

    # ✅ SAFE now
    if request.args.get("export") == "excel":
        excel_file = generate_excel(report["data"])
        return send_file(
            excel_file,
            download_name="attendance_report.xlsx",
            as_attachment=True
        )

    return jsonify(report), 200