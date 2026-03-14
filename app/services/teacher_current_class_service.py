from app.db.mongo import db

class TeacherCurrentClassService:
    @staticmethod
    def get_teacher_current_class(teacher_id, day, time):
        try:
            collection = db["teacher_schedule"]
            teacher = collection.find_one({"teacherId": teacher_id})

            if not teacher:
                return {
                    "success": False,
                    "message": "Teacher schedule not found"
                }
            day_schedule = teacher["schedule"].get(day, [])

            for slot in day_schedule:
                if slot["start_time"] <= time <= slot["end_time"]:
                    subject = slot["subject"]
                    department = slot["department"]
                    # Extract semester from subject code
                    sem = None
                    for ch in subject:
                        if ch.isdigit():
                            sem = int(ch)
                            break

                    return {
                        "success": True,
                        "department": department,
                        "subject": subject,
                        "semester": sem
                    }

            return {
                "success": False,
                "message": "No class found at this time"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }