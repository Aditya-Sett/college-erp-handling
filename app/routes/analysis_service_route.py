from flask import Blueprint, jsonify

health_check_bp = Blueprint("analysis_service_routes", __name__)

@health_check_bp.route("/health-check", methods=["GET"])
def health_check():
    try:
        return jsonify({
            "success": True,
            "message": "Server runnin"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Server is Dow n"
        }), 500