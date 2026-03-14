from app.db.mongo import db
from datetime import datetime

class SlotSaveService:
    @staticmethod
    def save_time_slots(data):

        try:
            collection = db["Academic_timetable_slots"]

            document = {
                "college_name": data.get("college_name"),
                "start_time": data.get("start_time"),
                "end_time": data.get("end_time"),
                "period_duration": data.get("period_duration"),
                "recess_duration": data.get("recess_duration"),
                "slots": data.get("slots"),
                "created_at": datetime.utcnow()
            }

            result = collection.insert_one(document)

            return {
                "success": True,
                "message": "Time slot schedule saved successfully",
                "schedule_id": str(result.inserted_id)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }