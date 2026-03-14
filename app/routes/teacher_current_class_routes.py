from flask import Blueprint, jsonify, request
from app.services.teacher_current_class_service import TeacherCurrentClassService
teacher_current_class_bp = Blueprint('teacher_current_class_routes', __name__)
@teacher_current_class_bp.route("/current-class", methods=['GET'])
def get_teacher_current_class():
    try:
        data = request.get_json()

        teacher_id = data.get["teacher_id"]
        day = data.get["day"]
        time = data.get["time"]

        if not teacher_id or not day or not time:
            return jsonify({
                "success": False,
                "message": "teacherId, day and time are required"
            }), 400

        result = TeacherCurrentClassService.get_teacher_current_class(teacher_id, day, time)

        if not result["success"]:
            return jsonify(result), 500

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500