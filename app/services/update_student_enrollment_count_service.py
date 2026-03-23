from app.db.mongo import studentEnrollmentCounts_collection
from app.db.mongo import students_collection

class UpdateStudentEnrollmentCountService:
    @staticmethod
    def update_student_enrollment_counts():
        try:
            # Step 1: Aggregate student counts
            pipeline = [
                {
                    "$match": {
                        "role": "ROLE_STUDENT"
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "department": "$department",
                            "academic_year": "$academic_year",
                            "sem": "$sem"
                        },
                        "student_count": {"$sum": 1}
                    }
                }
            ]

            results = list(students_collection.aggregate(pipeline))
            print("Aggregation Result:", results)

            # Step 2: Upsert into studentEnrollmentCounts
            for item in results:
                department = item["_id"]["department"]
                academic_year = item["_id"]["academic_year"]
                sem = item["_id"]["sem"]
                student_count = item["student_count"]

                studentEnrollmentCounts_collection.update_one(
                    {
                        "department": department,
                        "academic_year": academic_year,
                        "sem": sem
                    },
                    {
                        "$set": {
                            "department": department,
                            "academic_year": academic_year,
                            "sem": sem,
                            "student_count": student_count
                        }
                    },
                    upsert=True
                )

            return True

        except Exception as e:
            print("Error:", str(e))
            return False