from app.db.mongo import db

class TeacherScheduleService:
    @staticmethod
    def create_teacher_schedule(teacher_id, schedule):
        try:
            collection = db["teacher_schedule"]
            document = {
                "teacher_id": teacher_id,
                "schedule": schedule,
            }

            result = collection.insert_one(document)

            return {
                "success": True,
                "message": "Schedule stored successfully",
                "id": str(result.inserted_id)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }