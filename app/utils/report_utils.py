import requests
from app.connection.connection import BASE_AUTH_URL

BASE_authURL = BASE_AUTH_URL

def get_total_students(department, academic_year, sem):
    try:
        url = f"{BASE_authURL}/api/auth/get-student-count"
        print(f"url: {url}")

        start_year, end_suffix = academic_year.split("-")
        century = int(start_year[:2])
        start_yy = int(start_year[2:])
        end_yy = int(end_suffix)

        if end_yy < start_yy:
            end_year = f"{century + 1}{end_suffix}"
        else:
            end_year = f"{century}{end_suffix}"

        expanded_academic_year = f"{start_year}-{end_year}"
        print(f"expanded_academic_year: {expanded_academic_year}")

        splitted_sem = sem[:1]
        print(f"splitted_sem: {splitted_sem}")

        params = {
            "department": department,
            "academicYear": expanded_academic_year,
            "semester": splitted_sem
        }

        print(f"params: {params}")

        response = requests.get(url, params=params)
        print(f"response: {response.status_code}")

        if response.status_code == 200:
            data_response = response.json()
            print(f"data_response: {data_response}")
            return data_response.get("data", 0)
        else:
            return 6

    except Exception as e:
        print("Error calling student count API:", e)
        return 0