from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import auth, documents
import uvicorn
import os

app = FastAPI(title="SkillMatch API", root_path="/api")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",  # Existing Streamlit
        "http://localhost:5173",  # New React (Vite)
    ],
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
    from backend.database import check_db_connection, get_db
    is_online = check_db_connection()
    db_status = "Online" if is_online else "Offline"
    
    # Check if MONGO_URI or MONGODB_URI is missing (safely)
    mongo_config = "Set" if (os.getenv("MONGO_URI") or os.getenv("MONGODB_URI")) else "Missing"
    
    return {
        "status": "Healthy" if is_online else "Degraded",
        "database": db_status,
        "mongo_config": mongo_config,
        "api": "Online"
    }


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
