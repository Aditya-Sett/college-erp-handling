from flask import Blueprint, request, jsonify
from app.services.slot_save_service import SlotSaveService

slot_save_bp = Blueprint("slot_save_routes", __name__)

@slot_save_bp.route("/slots-saver", methods=["POST"])
def save_time_slots():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "Request body is empty"
            }), 400

        result = SlotSaveService.save_time_slots(data)

        if not result["success"]:
            return jsonify(result), 500

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500