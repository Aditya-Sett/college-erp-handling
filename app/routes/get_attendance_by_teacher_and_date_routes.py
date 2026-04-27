from flask import Blueprint, request, jsonify
from app.services.get_attendance_by_teacher_and_date_service import GetAttendanceByTeacherAndDateService

get_attendance_by_teacher_and_date_bp = Blueprint('get_attendance_by_teacher_and_date', __name__)

@get_attendance_by_teacher_and_date_bp.route("/by-teacher-date", methods=["POST"])
def fetch_attendance():
    data = request.get_json()

    teacher_id = data.get("teacherId")
    date_str = data.get("date")

    if not teacher_id or not date_str:
        return jsonify({"error": "teacherId and date are required"}), 400

    result = GetAttendanceByTeacherAndDateService.get_attendance_by_teacher_and_date(teacher_id, date_str)

    if result.get("success"):
        return jsonify(result), 200
    else:
        return jsonify(result), 500