from datetime import datetime, timedelta, timezone
from app.db.mongo import db

class GetAttendanceByTeacherAndDateService:
    @staticmethod
    def get_attendance_by_teacher_and_date(teacher_id, date_str):
        try:
            print("db.name:", db.name)
            print("db.list_collection_names:", db.list_collection_names())
            attendancecodes_collection = db["attendancecodes"]
            print("attendancecodes_collection_count_documents:", attendancecodes_collection.count_documents({}))
            # Convert date string
            start_date = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            end_date = start_date + timedelta(days=1)
            print("start date:", start_date)
            print("end date:", end_date)
            print("attendancecodes_collection.find_one:", attendancecodes_collection.find_one())

            results = attendancecodes_collection.find(
                {
                    "teacherId": teacher_id,
                    "generatedAt": {
                        "$gte": start_date,
                        "$lt": end_date
                    }
                },
                {
                    "_id": 0,
                    "wifiFingerprint": 0,
                    "bluetoothUuid": 0
                }
            )

            print("results:", results)
            data_list = list(results)

            return {
                "success": True,
                "count": len(data_list),
                "data": data_list
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }