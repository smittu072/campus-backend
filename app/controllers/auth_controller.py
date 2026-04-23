from fastapi import HTTPException
from app.database.database import db
from app.utils.jwt import create_token
import bcrypt

users = db["users"]

# ================= SIGNUP =================
async def signup(data: dict):
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")
    enrollment_no = data.get("enrollment_no")

    # validation
    if not name or not email or not password or not role:
        raise HTTPException(status_code=400, detail="Missing fields")

    if role == "student" and not enrollment_no:
        raise HTTPException(status_code=400, detail="Enrollment required")

    # duplicate check
    if users.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    if role == "student" and users.find_one({"enrollment_no": enrollment_no}):
        raise HTTPException(status_code=400, detail="Enrollment already exists")

    # password hash (store as bytes)
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    users.insert_one({
        "name": name,
        "email": email,
        "password": hashed_password,
        "role": role,
        "enrollment_no": enrollment_no
    })

    return {
        "msg": "Signup successful"
    }


# ================= LOGIN =================
async def login(data: dict):
    identifier = data.get("identifier")
    password = data.get("password")

    if not identifier or not password:
        raise HTTPException(status_code=400, detail="Missing credentials")

    # detect user
    if identifier.isdigit() and len(identifier) == 12:
        user = users.find_one({"enrollment_no": identifier})
    else:
        user = users.find_one({"email": identifier})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # password check (IMPORTANT: ensure bytes)
    if not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        raise HTTPException(status_code=401, detail="Wrong password")

    # create token
    token = create_token({
        "id": str(user["_id"]),
        "role": user["role"]
    })

    # ✅ FINAL RESPONSE (name included)
    return {
        "msg": "Login successful",
        "token": token,
        "role": user["role"],
        "name": user.get("name", "User")   # fallback safe
    }