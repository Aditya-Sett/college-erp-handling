from app.db.mongo import db

class Academic_TimeTable_Format_Finder_Service:
    @staticmethod
    def get_academic_timetable(college_name):

        try:
            collection = db["Academic_timetable"]

            timetable = list(collection.find(
                {"college_name": college_name},
                {"_id": 0}
            ))

            if not timetable:
                return {
                    "success": False,
                    "error": "No timetable found for this college"
                }

            return {
                "success": True,
                "data": timetable
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }