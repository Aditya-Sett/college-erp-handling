from flask import Blueprint, request, jsonify
from app.services.slot_service import SlotService

slot_bp = Blueprint("slot_routes", __name__)


@slot_bp.route("/calculate-slots", methods=["POST"])
def calculate_slots():

    try:
        data = request.get_json()

        start_time = data.get("start_time")
        end_time = data.get("end_time")
        period_duration = data.get("period_duration")
        recess_duration = data.get("recess_duration", 30)

        if not start_time or not end_time or not period_duration:
            return jsonify({
                "success": False,
                "error": "Missing required fields"
            }), 400

        result = SlotService.calculate_slots(
            start_time,
            end_time,
            period_duration,
            recess_duration
        )

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500