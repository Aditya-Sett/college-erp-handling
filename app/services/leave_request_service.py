import requests
from datetime import datetime
from app.db.mongo import db
from werkzeug.utils import secure_filename
import os
from app.connection.connection import BASE_AUTH_URL

AUTH_API_URL = f"{BASE_AUTH_URL}/api/auth/get-hod-coordinator"

leave_request_collection = db["leave_request"]

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        return filepath
    else:
        raise Exception("Invalid file type")


def get_approvers(Department, sem, academicYear):
    payload = {
        "department": Department,
        "semester": sem,
        "academicYear": academicYear
    }
    print("payload", payload)

    response = requests.post(AUTH_API_URL, json=payload)

    print("response_json",response.json())

    if response.status_code != 200:
        raise Exception("Failed to fetch approvers")

    data = response.json()

    inside_data = data.get("data")
    print("inside_data",inside_data)

    return inside_data.get("coordinatorId"), inside_data.get("hodId")


def create_leave_request(data, file):
    # Extract fields
    studentId = data.get("studentId")
    Department = data.get("Department")
    sem = data.get("sem")
    academicYear = data.get("academicYear")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    category = data.get("category")
    reason = data.get("reason")

    # Validate required fields
    if not all([studentId, Department, sem, academicYear, start_date, end_date, category, reason]):
        raise Exception("Missing required fields")

    # Save file
    proof_path = save_file(file)

    # Call external API
    classCoordinatorId, HODId = get_approvers(Department, sem, academicYear)

    if not classCoordinatorId or not HODId:
        raise Exception("Invalid approver data")

    # Create document
    leave_doc = {
        "studentId": studentId,
        "Department": Department,
        "sem": sem,
        "academicYear": academicYear,
        "start_date": start_date,
        "end_date": end_date,
        "category": category,
        "reason": reason,
        "proof": proof_path,
        "classCoordinatorId": classCoordinatorId,
        "HODId": HODId,
        "status": "PENDING",
        "timestamp": datetime.utcnow()
    }

    result = leave_request_collection.insert_one(leave_doc)

    return str(result.inserted_id)