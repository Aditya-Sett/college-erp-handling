import requests
from app.connection.connection import BASE_AUTH_URL

BASE_authURL = BASE_AUTH_URL

def get_total_students(department, academic_year, sem):
    try:
        url = f"{BASE_authURL}/api/auth/get-student-count"

        params = {
            "department": department,
            "academicYear": academic_year,
            "sem": sem
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            return data.get("total_students", 0)
        else:
            return 0

    except Exception as e:
        print("Error calling student count API:", e)
        return 0