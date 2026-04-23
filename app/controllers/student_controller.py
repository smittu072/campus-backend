from app.database.database import db

# 📅 SAVE TIMETABLE
def save_timetable(user_id, subjects):
    db["timetable"].update_one(
        {"studentId": user_id},
        {"$set": {"subjects": subjects}},
        upsert=True
    )
    return {"msg": "Timetable saved"}


# 📝 ADD ASSIGNMENT
def add_assignment(user_id, title):
    db["assignments"].insert_one({
        "studentId": user_id,
        "title": title,
        "status": "pending"
    })
    return {"msg": "Assignment added"}


# 📊 UPDATE ATTENDANCE
def update_attendance(user_id, percentage):
    db["attendance"].update_one(
        {"studentId": user_id},
        {
            "$set": {"percentage": percentage},
            "$push": {"history": percentage}
        },
        upsert=True
    )
    return {"msg": "Attendance updated"}