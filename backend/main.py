from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import auth, documents
import uvicorn
import os

app = FastAPI(title="SkillMatch API")

# CORS
frontend_url = os.getenv("FRONTEND_URL", "")
origins = [
    "http://localhost:8501",  # Existing Streamlit
    "http://localhost:5173",  # New React (Vite)
    "https://skill-match-4est.vercel.app", # Vercel Frontend
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

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"DEBUG: Incoming {request.method} {request.url.path}")
    print(f"DEBUG: Headers {dict(request.headers)}")
    response = await call_next(request)
    return response

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    
    # Debug logging for validation errors (SAFE - no body reading)
    print(f"DEBUG: Validation Error for {request.method} {request.url.path}")
    print(f"DEBUG: Errors: {errors}")
    
    # Find the first error message that is readable
    msg = "Invalid data format"
    if errors:
        error = errors[0]
        # Pydantic V2 often uses 'loc' to indicate where the error is
        loc = error.get("loc", [])
        field = loc[-1] if loc else "data"
        msg = f"ValidationError at {loc}: {error.get('msg')}"
        
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": msg, "errors": errors},
    )

# Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])

@app.on_event("startup")
def startup_db_client():
    from backend.database import ensure_indexes
    ensure_indexes()

@app.get("/")
def read_root():
    return {"message": "SkillMatch API is running 🚀"}

@app.get("/health")
def health_check():
    from backend.database import check_db_connection
    import os
    try:
        import python_multipart
        multipart_status = "Available"
    except ImportError:
        multipart_status = "Missing"
        
    is_online = check_db_connection()
    db_status = "Online" if is_online else "Offline"
    
    # Check for any keys that contain "MONGO" (case-insensitive)
    env_keys = list(os.environ.keys())
    mongo_keys = [k for k in env_keys if "MONGO" in k.upper()]
    
    return {
        "app_version": "V4-MANUAL-PARSING",
        "status": "Healthy" if is_online else "Degraded",
        "database": db_status,
        "multipart": multipart_status,
        "mongo_env_keys": mongo_keys,
        "api": "Online",
        "env_count": len(env_keys)
    }


# Build Salt: 1772300000
if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
