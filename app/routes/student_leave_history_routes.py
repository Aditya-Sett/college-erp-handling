from app.services.student_leave_history_service import get_student_leave_history
from flask import Blueprint, request, jsonify

student_leave_history_bp = Blueprint("student_leave_history", __name__)

@student_leave_history_bp.route("/student-leave-history", methods=["POST"])
def student_leave_history():
    try:
        data = request.json

        studentId = data.get("studentId")

        if not studentId:
            return jsonify({"error": "studentId is required"}), 400

        result = get_student_leave_history(studentId)

        return jsonify({
            "count": len(result),
            "data": result
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500