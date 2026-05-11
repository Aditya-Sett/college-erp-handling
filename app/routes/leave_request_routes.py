from flask import Blueprint, request, jsonify
from app.services.leave_request_service import create_leave_request

leave_request_bp = Blueprint("leave_request", __name__)

@leave_request_bp.route("/apply-leave", methods=["POST"])
def apply_leave():
    try:
        data = request.form   # because multipart
        file = request.files.get("proof")

        if not file:
            return jsonify({"error": "Proof file is required"}), 400

        leave_id = create_leave_request(data, file)

        return jsonify({
            "message": "Leave request submitted successfully",
            "leaveId": leave_id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500