from app.db.mongo import db

class ViewStudentScheduleService:
    @staticmethod
    def view_student_schedule(department,semester):
        try:
            teacher_schedule_collection = db["teacher_schedule"]
            data = teacher_schedule_collection.find(

            )

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }