from flask import Blueprint, jsonify, request
from app.services.update_student_enrollment_count_service import UpdateStudentEnrollmentCountService

update_student_enrollment_count_bp = Blueprint('update_student_enrollment_count_routes', __name__)
@update_student_enrollment_count_bp.route('/update-enrollment-counts', methods=['GET'])

def update_enrollment_counts():
    success = UpdateStudentEnrollmentCountService.update_student_enrollment_counts()

    if success:
        return jsonify({
            "success": True,
            "message": "Enrollment counts updated successfully"
        })
    else:
        return jsonify({
            "success": False,
            "message": "Error updating enrollment counts"
        }), 500