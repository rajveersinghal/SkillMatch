from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import auth, documents
import uvicorn
import os

app = FastAPI(title="SkillMatch API", root_path="/api")

# CORS
frontend_url = os.getenv("FRONTEND_URL", "")
origins = [
    "http://localhost:8501",  # Existing Streamlit
    "http://localhost:5173",  # New React (Vite)
]
if frontend_url:
    origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    # Find the first error message that is readable
    msg = "Invalid data format"
    if errors:
        error = errors[0]
        field = error.get("loc", ["field"])[-1]
        msg = f"Invalid {field}: {error.get('msg', 'Format error')}"
        
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": msg},
    )

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])

@app.get("/")
def read_root():
    return {"message": "SkillMatch API is running 🚀"}

@app.get("/health")
def health_check():
    from backend.database import check_db_connection
    import os
    is_online = check_db_connection()
    db_status = "Online" if is_online else "Offline"
    
    # Check for any keys that contain "MONGO" (case-insensitive)
    env_keys = list(os.environ.keys())
    mongo_keys = [k for k in env_keys if "MONGO" in k.upper()]
    
    return {
        "app_version": "3.0.0-FIX-DEPLOY",
        "status": "Healthy" if is_online else "Degraded",
        "database": db_status,
        "mongo_env_keys": mongo_keys,
        "api": "Online",
        "env_count": len(env_keys)
    }


# Build Salt: 1772300000
if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
