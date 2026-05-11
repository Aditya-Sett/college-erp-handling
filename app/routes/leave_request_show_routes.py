from app.services.leave_request_show_service import get_leave_requests_by_teacher
from flask import Blueprint, request, jsonify

leave_request_show_bp = Blueprint("leave_request_show", __name__)

@leave_request_show_bp.route("/teacher-show-leave-requests", methods=["POST"])
def teacher_leave_requests():
    try:
        data = request.json

        teacherId = data.get("teacherId")

        if not teacherId:
            return jsonify({"error": "teacherId is required"}), 400

        leave_requests = get_leave_requests_by_teacher(teacherId)

        return jsonify({
            "count": len(leave_requests),
            "data": leave_requests
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500