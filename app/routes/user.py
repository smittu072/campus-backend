from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
def login(data: dict):
    email = data.get("email")
    password = data.get("password")

    # dummy check
    if email == "test@gmail.com" and password == "1234":
        return {
            "status": "success",
            "user": {
                "name": "Rahul Sharma",
                "role": "student"
            }
        }

    return {"status": "error", "message": "Invalid credentials"}