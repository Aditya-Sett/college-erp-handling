from flask import Blueprint, request, jsonify
from app.services.attendance_service import AttendanceService

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/get-attendance-summary', methods=['POST'])
def get_attendance_summary():
    try:
        data = request.json

        teacher_id = data.get("teacherId")
        generated_at = data.get("generatedAt")

        if not teacher_id or not generated_at:
            return jsonify({"error": "Missing teacherId or generatedAt"}), 400

        result, status_code = AttendanceService.get_attendance_summary_service(teacher_id, generated_at)

        return jsonify(result), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500