from app.services.leave_approval_unapproval_service import process_leave_decision
from flask import Blueprint, request, jsonify

leave_approval_unapproval_bp = Blueprint("leave_approval_unapproval", __name__)

@leave_approval_unapproval_bp.route("/approval-unapproval-process-leave", methods=["POST"])
def process_leave():
    try:
        data = request.json

        leave_id, decision = process_leave_decision(data)

        return jsonify({
            "message": f"Leave request {decision.lower()} successfully",
            "newId": leave_id
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500