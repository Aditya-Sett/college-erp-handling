from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, send_file, jsonify
from app.services.curriculum_excel_service import CurriculumExcelService
import io

curriculum_bp = Blueprint("curriculum", __name__)

@curriculum_bp.route("/excel", methods=["POST"])
def generate_curriculum_excel():
    try:
        data = request.get_json()

        classname = data.get("classname")
        department = data.get("department")
        total_semesters = int(data.get("totalSemesters"))
        effective_year = data.get("effectiveYear")

        wb = CurriculumExcelService.generate_excel(
            classname,
            department,
            total_semesters,
            effective_year
        )

        file_stream = io.BytesIO()
        wb.save(file_stream)
        file_stream.seek(0)

        filename = f"{classname}_{department}_Curriculum.xlsx"

        return send_file(
            file_stream,
            as_attachment=True,
            download_name=filename,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500