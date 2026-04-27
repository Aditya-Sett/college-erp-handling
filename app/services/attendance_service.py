from datetime import timedelta
from app.db.mongo import db
import requests
from app.connection.connection import BASE_AUTH_URL
from app.utils.report_utils import get_total_students
from app.utils.time_utils import parse_datetime

attendance_codes = db["attendancecodes"]
attendance_records = db["attendancerecords"]

AUTH_SERVICE_URL = BASE_AUTH_URL

class AttendanceService:
    @staticmethod
    def get_attendance_summary_service(teacher_id, generated_at_str):
        try:
            # Convert to datetime
            generated_at = parse_datetime(generated_at_str)

            # STEP 1: Find attendance code
            code_doc = attendance_codes.find_one({
                "teacherId": teacher_id,
                "generatedAt": {
                    "$gte": generated_at,
                    "$lt": generated_at + timedelta(seconds=1)
                }
            })

            if not code_doc:
                return {"error": "Attendance code not found"}, 404

            expires_at = code_doc["expiresAt"]
            department = code_doc["department"]
            academic_year = code_doc["academicYear"]
            sem = code_doc["sem"]
            code = code_doc["code"]

            # STEP 2: Find present students
            records = attendance_records.find({
                "teacherId": teacher_id,
                "department": department,
                "academic_year": academic_year,
                "sem": sem,
                "code": code,
                "timestamp": {
                    "$gte": generated_at,
                    "$lte": expires_at
                }
            })

            start_year, end_suffix = academic_year.split("-")
            century = int(start_year[:2])
            start_yy = int(start_year[2:])
            end_yy = int(end_suffix)

            if end_yy < start_yy:
                end_year = f"{century + 1}{end_suffix}"
            else:
                end_year = f"{century}{end_suffix}"

            expanded_academic_year = f"{start_year}-{end_year}"

            total_students = get_total_students(department, academic_year, sem)

            present_student_ids = {r["studentId"] for r in records}
            print("present_student_ids", present_student_ids)

            # STEP 3: Call external API
            url = f"{AUTH_SERVICE_URL}/api/auth/get-all-students"

            params = {
                "department": department,
                "academicYear": expanded_academic_year,
                "semester": sem.replace("th", ""),
                "page": 0,
                "size": total_students,
                "sort": "collegeRoll"
            }

            response = requests.get(url, params=params)

            if response.status_code != 200:
                return {"error": "Failed to fetch students"}, 500

            students_data = response.json()
            all_students = students_data["data"]["content"]

            # STEP 4: Merge
            final_list = []

            for student in all_students:
                sid = student["studentId"]
                #print("sid", sid)

                final_list.append({
                    "studentId": sid,
                    "collegeRoll": student["collegeRoll"],
                    "username": student["username"],
                    "status": "present" if sid in present_student_ids else "absent"
                })

            return {
                "success": True,
                "data": final_list
            }, 200

        except Exception as e:
            return {"error": str(e)}, 500