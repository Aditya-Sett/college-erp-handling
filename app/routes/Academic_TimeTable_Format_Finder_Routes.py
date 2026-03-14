from flask import Blueprint, request, jsonify
from app.services.Academic_TimeTable_Format_Finder_Service import Academic_TimeTable_Format_Finder_Service

Academic_TimeTable_Format_Finder_bp = Blueprint("Academic_TimeTable_Format_Finder_Routes", __name__)

@Academic_TimeTable_Format_Finder_bp.route("/slots-finder", methods=["POST"])
def get_academic_timetable():

    try:
        data = request.get_json()

        college_name = data.get("college_name")

        if not college_name:
            return jsonify({
                "success": False,
                "error": "college_name is required"
            }), 400

        result = Academic_TimeTable_Format_Finder_Service.get_academic_timetable(college_name)

        if not result["success"]:
            return jsonify(result), 404

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500