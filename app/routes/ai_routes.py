from fastapi import APIRouter, Request
from app.database.database import db
from app.utils.jwt import verify_token

router = APIRouter()

attendance = db["attendance"]
assignments = db["assignments"]


def get_user_id(request: Request):
    auth = request.headers.get("Authorization")

    if not auth:
        return None

    try:
        token = auth.split(" ")[1]
    except:
        return None

    payload = verify_token(token)
    return payload.get("id") if payload else None


@router.post("/chat")
async def chat(data: dict, request: Request):
    user_id = get_user_id(request)
    msg = data.get("message", "").lower()

    if not user_id:
        return {"reply": "Unauthorized"}

    # 🔥 SMART RESPONSES
    if "attendance" in msg:
        att = attendance.find_one({"user_id": user_id})
        percent = att.get("percentage", 0) if att else 0
        return {"reply": f"Your attendance is {percent}% 📊"}

    if "assignment" in msg:
        count = assignments.count_documents({"user_id": user_id})
        return {"reply": f"You have {count} assignments 📝"}

    if "hello" in msg or "hi" in msg:
        return {"reply": "Hey! How can I help you? 😊"}

    return {"reply": "I can help with attendance and assignments for now 🤖"}