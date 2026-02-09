from fastapi import FastAPI
from backend.routes import auth_routes, ingestion_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SkillMatch API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(ingestion_routes.router, prefix="/ingestion", tags=["Ingestion"])

@app.get("/")
async def root():
    return {"message": "Welcome to SkillMatch API"}

@app.get("/health")
async def health():
    from backend.database import database
    try:
        await database.command("ping")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}
