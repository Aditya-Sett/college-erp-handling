from app.db.mongo import db
from bson import ObjectId
from datetime import datetime

leave_request_collection = db["leave_request"]
leave_approved_collection = db["leave_approved"]
leave_denied_collection = db["leave_denied"]

def process_leave_decision(data):
    leave_id = data.get("_id")
    teacherId = data.get("teacherId")
    decision = data.get("status")  # APPROVED or DENIED

    if not leave_id or not teacherId or not decision:
        raise Exception("_id, teacherId and status are required")

    if decision not in ["APPROVED", "DENIED"]:
        raise Exception("Invalid status. Must be APPROVED or DENIED")

    # 1. Fetch existing leave request
    leave_doc = leave_request_collection.find_one({"_id": ObjectId(leave_id)})

    if not leave_doc:
        raise Exception("Leave request not found")

    # 2. OPTIONAL: allow teacher to update fields
    updatable_fields = ["start_date", "end_date", "category"]

    for field in updatable_fields:
        if field in data:
            leave_doc[field] = data[field]

    # Remove old _id to avoid duplication conflict
    leave_doc.pop("_id")

    # 3. Process decision
    if decision == "APPROVED":
        leave_doc["status"] = "APPROVED"
        leave_doc["approved_by"] = teacherId
        leave_doc["approved_timestamp"] = datetime.utcnow()

        # Save to approved collection
        result = leave_approved_collection.insert_one(leave_doc)

    else:  # DENIED
        denied_reason = data.get("denied_reason")

        if not denied_reason:
            raise Exception("denied_reason is required when status is DENIED")

        leave_doc["status"] = "DENIED"
        leave_doc["denied_by"] = teacherId
        leave_doc["denied_reason"] = denied_reason
        leave_doc["denied_timestamp"] = datetime.utcnow()

        # Save to denied collection
        result = leave_denied_collection.insert_one(leave_doc)

    # 4. Delete from original collection
    leave_request_collection.delete_one({"_id": ObjectId(leave_id)})

    return str(result.inserted_id), decision