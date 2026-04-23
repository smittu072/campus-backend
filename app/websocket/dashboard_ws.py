from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.utils.jwt import verify_token
from app.database.database import db
import asyncio

router = APIRouter()

@router.websocket("/ws/dashboard")
async def dashboard_ws(websocket: WebSocket):
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close()
        return

    payload = verify_token(token)
    if not payload:
        await websocket.close()
        return

    user_id = payload.get("id")
    role = payload.get("role")

    await websocket.accept()
    print("✅ WebSocket Connected")

    try:
        while True:
            if role == "student":
                att = db["attendance"].find_one({"user_id": user_id}) or {}

                data = {
                    "attendance": att.get("percentage", 0),
                    "assignments": db["assignments"].count_documents({"user_id": user_id}),
                    "role": "student"
                }

            elif role == "faculty":
                data = {
                    "students": db["users"].count_documents({"role": "student"}),
                    "assignments": db["assignments"].count_documents({}),
                    "role": "faculty"
                }

            await websocket.send_json(data)
            await asyncio.sleep(2)

    except WebSocketDisconnect:
        print("❌ Client disconnected")