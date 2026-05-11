from datetime import timedelta
from app.db.mongo import db
import requests
from app.utils.report_utils import get_total_students
from app.connection.connection import BASE_AUTH_URL
from datetime import datetime, timedelta

attendancecodes = db["attendancecodes"]
attendancerecords = db["attendancerecords"]
leave_approved_collection = db["leave_approved"]

AUTH_SERVICE_URL = BASE_AUTH_URL

class ReportGenerator:
    @staticmethod
    def generate_attendance_report(data):
        try:
            teacherId = data["teacherId"]
            department = data["department"]
            academicYear = data["academicYear"]
            sem = data["sem"]
            subject = data["subject"]

            start_year, end_suffix = academicYear.split("-")
            century = int(start_year[:2])
            start_yy = int(start_year[2:])
            end_yy = int(end_suffix)

            if end_yy < start_yy:
                end_year = f"{century + 1}{end_suffix}"
            else:
                end_year = f"{century}{end_suffix}"

            expanded_academic_year = f"{start_year}-{end_year}"

            total_students = get_total_students(department, academicYear, sem)

            # STEP 3: Call external API
            url = f"{AUTH_SERVICE_URL}/api/auth/get-all-students"
            print("url:", url)

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
            students = students_data["data"]["content"]
            print("students type:", type(students))


            # 1️⃣ Fetch Students
            #students = fetch_students(department, academicYear, sem)

            # 2️⃣ Fetch Sessions
            codes = list(attendancecodes.find({
                "teacherId": teacherId,
                "department": department,
                "academicYear": academicYear,
                "sem": sem,
                "subject": subject
            }))
            print("codes:", codes)

            session_times = sorted([c["generatedAt"] for c in codes])
            total_sessions = len(session_times)

            if total_sessions == 0:
                return {
                    "success": True,
                    "data": [],
                    "message": "No sessions found"
                }

            # 3️⃣ Fetch ALL attendance records ONCE (⚡ optimization)
            records = list(attendancerecords.find({
                "teacherId": teacherId,
                "department": department,
                "academic_year": academicYear,
                "sem": sem,
                "subject": subject
            }))
            print("records:", records)

            approved_leaves = list(leave_approved_collection.find({
                "department": department,
                "academicYear": academicYear,
                "sem": sem
            }))

            leave_map = {}

            for leave in approved_leaves:
                student_id = leave["studentId"]
                start_date = leave["start_date"]
                end_date = leave["end_date"]
                category = leave["category"]

                # Convert to datetime.date
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

                current = start_date
                while current <= end_date:
                    leave_map[(student_id, current)] = category
                    current += timedelta(days=1)

            # 4️⃣ Build FAST lookup map
            # Key = (studentId, session_time_bucket)
            attendance_map = {}

            for rec in records:
                student_id = rec["studentId"]
                ts = rec["timestamp"]

                # Map each record to nearest session
                for session_time in session_times:
                    if abs((ts - session_time).total_seconds()) <= 60:
                        attendance_map[(student_id, session_time)] = True
                        break

            # 5️⃣ Build Final Report
            report = []

            for student in students:
                student_id = student["studentId"]

                row = {
                    "studentId": student_id,
                    "collegeRoll": student["collegeRoll"],
                    "username": student["username"]
                }

                present_count = 0

                for session_time in session_times:
                    print("session_time", session_time)
                    key = session_time.strftime("%d-%m-%y %H:%M")

                    session_date = session_time.date()

                    if (student_id, session_time) in attendance_map:
                        row[key] = "Present"
                        present_count += 1

                    elif (student_id, session_date) in leave_map:
                        row[key] = leave_map[(student_id, session_date)]  # e.g. "Medical"
                        present_count += 1  #  COUNT AS PRESENT

                    else:
                        row[key] = "Absent"

                percentage = (present_count / total_sessions) * 100

                row["percentage"] = round(percentage, 2)

                report.append(row)

            return {
                "success": True,
                "data": report,
                "totalSessions": total_sessions
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
