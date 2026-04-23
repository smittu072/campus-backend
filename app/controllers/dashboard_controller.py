from app.database.database import db

timetable = db["timetable"]
assignments = db["assignments"]
attendance = db["attendance"]
notices = db["notices"]


async def get_student_dashboard(user_id: str):

    # ✅ subjects
    tt = timetable.find_one({"user_id": user_id})
    subjects = tt.get("subjects", []) if tt else []

    # ✅ assignments
    assignment_list = list(assignments.find({"user_id": user_id}))

    # ✅ attendance
    att = attendance.find_one({"user_id": user_id})
    attendance_percent = att.get("percentage", 0) if att else 0

    # ✅ notices
    notice_list = list(notices.find({}))

    return {
        "today_classes": len(subjects),
        "attendance": attendance_percent,
        "assignment_list": assignment_list,
        "notice_list": notice_list,
        "subjects": subjects
    }