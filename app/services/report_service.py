from app.db.mongo import db
from app.utils.report_utils import get_total_students

class ReportService:
    @staticmethod
    def get_department_report_service(department):
        response = {
            "department": department,
            "academic_years": []
        }

        # 1. Get all academic years
        academic_years = db.attendancecodes.distinct(
            "academicYear",
            {"department": department}
        )

        for year in academic_years:

            year_data = {
                "year": year,
                "semesters": []
            }

            # 2. Get semesters
            semesters = db.attendancecodes.distinct(
                "sem",
                {"department": department, "academicYear": year}
            )

            for sem in semesters:

                sem_data = {
                    "semester": sem,
                    "overall_percentage": 0,
                    "subjects": []
                }

                # 3. Get subjects
                subjects = db.attendancecodes.distinct(
                    "subject",
                    {
                        "department": department,
                        "academicYear": year,
                        "sem": sem
                    }
                )

                subject_percentages = []

                for subject in subjects:

                    # 4. Get counts
                    total_students = get_total_students(department,year,sem)

                    total_classes = db.attendancecodes.count_documents({
                        "department": department,
                        "academicYear": year,
                        "sem": sem,
                        "subject": subject
                    })

                    total_attendance = db.attendancerecords.count_documents({
                        "department": department,
                        "academic_year": year,
                        "sem": sem,
                        "subject": subject
                    })

                    # 5. Calculate %
                    if total_students > 0 and total_classes > 0:
                        percentage = (total_attendance / (total_students * total_classes)) * 100
                    else:
                        percentage = 0

                    subject_percentages.append(percentage)

                    sem_data["subjects"].append({
                        "subject": subject,
                        "percentage": round(percentage, 2)
                    })

                # 6. Semester overall %
                if subject_percentages:
                    sem_data["overall_percentage"] = round(
                        sum(subject_percentages) / len(subject_percentages), 2
                    )

                year_data["semesters"].append(sem_data)

            response["academic_years"].append(year_data)

        return response