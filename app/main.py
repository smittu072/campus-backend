from fastapi import FastAPI
from fastapi import WebSocket


from fastapi.middleware.cors import CORSMiddleware

# ✅ Correct imports
from app.routes import dashboard_routes
from app.routes import student_routes
from app.routes import auth_routes
from app.routes import assignment_routes
from app.routes import notice_routes
from app.routes import attendance_routes
from app.websocket import dashboard_ws

from app.routes import ai_routes


app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ROUTES
app.include_router(dashboard_routes.router, prefix="/api/dashboard")
app.include_router(student_routes.router, prefix="/api/student")
app.include_router(auth_routes.router, prefix="/api/auth")

app.include_router(assignment_routes.router, prefix="/api/assignment")
app.include_router(notice_routes.router, prefix="/api/notice")
app.include_router(attendance_routes.router, prefix="/api/attendance")

app.include_router(dashboard_ws.router)

app.include_router(ai_routes.router, prefix="/api/ai")