from flask import Blueprint, request, jsonify
from app.services.teacher_schedule_service import TeacherScheduleService

teacher_schedule_bp = Blueprint('teacher_schedule_routes', __name__)
@teacher_schedule_bp.route("/schedule", methods=["POST"])
def create_teacher_schedule():
    try:
        data = request.get_json()

        teacher_id = data.get("teacherId")
        schedule = data.get("schedule")

        if not teacher_id or not schedule:
            return jsonify({
                "success": False,
                "message": "teacherId and schedule are required"
            }), 400

        result = TeacherScheduleService.create_teacher_schedule(teacher_id, schedule)

        if not result["success"]:
            return jsonify(result), 500

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500