from flask import Blueprint, request, jsonify
from app.services.curriculum_excel_parser_service import CurriculumExcelParserService

upload_bp = Blueprint("curriculum_upload", __name__)

@upload_bp.route("/upload", methods=["POST"])
def upload_curriculum():
    if "file" not in request.files:
        return jsonify({
            "success": False,
            "error": "Excel file is required"
        }), 400

    file = request.files["file"]

    if not file.filename.endswith(".xlsx"):
        return jsonify({
            "success": False,
            "error": "Only .xlsx files allowed"
        }), 400

    result = CurriculumExcelParserService.parse_and_save(file)

    return jsonify({
        "success": True,
        "data": result
    }), 201
